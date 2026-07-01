import asyncio
import random
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any, Dict

from dishka import Provider, Scope, make_async_container, provide
from dishka_faststream import FastStreamProvider, FromDishka, setup_dishka
from faststream.middlewares.acknowledgement.config import AckPolicy
from faststream.rabbit import ExchangeType, QueueType, RabbitBroker, RabbitExchange, RabbitQueue
from faststream.rabbit.annotations import RabbitMessage
from loguru import logger

from src.domain.entities import PaymentEntity, PaymentStatuses
from src.domain.exceptions import WebhookDeliveryError
from src.domain.interfaces.services import IPaymentService, IWebhookService
from src.infrastructure.config.settings import settings
from src.infrastructure.ioc import (
    DatabaseProvider,
    PaymentRepositoryProvider,
    PaymentServiceProvider,
    WebhookServiceProvider,
)


class PaymentsConsumer:
    """Класс обработчика событий по платежам"""

    async def payment_new_processing(
        self, message: Dict[str, Any], payment_service: IPaymentService, webhook_service: IWebhookService
    ) -> None:
        """Обработка события создания нового платежа"""
        try:
            if not message.get("payment_id"):
                logger.debug(f"Invalid message: missing payment_id: {repr(message)}")
                return

            entity: PaymentEntity | None = await payment_service.retrieve(message["payment_id"])
            if not entity:
                logger.debug(f"Payment not found by ID {message['payment_id']}")
                return
            elif entity.status != PaymentStatuses.pending.name:
                logger.debug(f"Payment status is not equal to '{PaymentStatuses.pending.name}'")
                return

            error_messages = [
                "Insufficient funds",
                "Incorrect card/wallet number",
                "Payment declined by the bank",
                "Suspected fraud",
                "Processing time expired",
            ]

            dt = datetime.now(timezone.utc)

            delay = random.uniform(settings.backend_payment_min_delay, settings.backend_payment_max_delay)
            await asyncio.sleep(delay)

            entity.updated_at = dt
            if entity.expired_at and entity.expired_at < dt:
                entity.status = PaymentStatuses.failed.name
                entity.processing_error_message = error_messages[-1]
            elif random.random() >= settings.backend_payment_success_rate:
                entity.processing_error_message = random.choice(error_messages)
                entity.status = PaymentStatuses.failed.name
            else:
                entity.status = PaymentStatuses.succeeded

            entity_dict = asdict(entity)
            if entity.status != PaymentStatuses.failed.name and entity.webhook_url:
                await webhook_service.send(entity.webhook_url, entity_dict)

            await payment_service.update(str(entity.id), entity_dict)
        except WebhookDeliveryError:
            raise


class PaymentsConsumerProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def provide_payment_consumer(self) -> PaymentsConsumer:
        return PaymentsConsumer()


broker = RabbitBroker(settings.get_rabbitmq_url())

container = make_async_container(
    DatabaseProvider(),
    PaymentRepositoryProvider(),
    PaymentServiceProvider(),
    WebhookServiceProvider(),
    PaymentsConsumerProvider(),
    FastStreamProvider(),
)
setup_dishka(container, broker=broker, auto_inject=True)

payment_exchange = RabbitExchange(settings.consumer_exchange_name, type=ExchangeType.TOPIC, durable=True)
dlx_exchange = RabbitExchange(settings.consumer_dlx_exchange_name, type=ExchangeType.FANOUT, durable=True)

payment_queue = RabbitQueue(
    settings.consumer_queue_name,
    queue_type=QueueType.QUORUM,
    durable=True,
    routing_key=settings.consumer_payment_routing_key,
    arguments={
        "x-queue-type": "quorum",
        "x-overflow": "reject-publish",
        "x-dead-letter-exchange": settings.consumer_dlx_exchange_name,
        "x-dead-letter-routing-key": settings.consumer_dead_letter_routing_key,
        "x-delivery-limit": settings.consumer_queue_delivery_limit,
        "x-dead-letter-strategy": "at-least-once",
    },
)

dlq_queue = RabbitQueue(
    settings.consumer_dlq_queue_name,
    durable=True,
    queue_type=QueueType.QUORUM,
    routing_key=settings.consumer_dead_letter_routing_key,
    arguments={
        "x-queue-type": "quorum",
        "x-message-ttl": settings.consumer_dlq_queue_message_ttl,
    },
)


@broker.subscriber(queue=payment_queue, exchange=payment_exchange, ack_policy=AckPolicy.NACK_ON_ERROR)
async def payment_new_handler(
    message: Dict[str, Any],
    raw_message: RabbitMessage,
    payments_consumer: FromDishka[PaymentsConsumer],
    payment_service: FromDishka[IPaymentService],
    webhook_service: FromDishka[IWebhookService],
) -> None:
    """Обработка события в очереди RabbitMQ `payments.new`"""
    return await payments_consumer.payment_new_processing(message, payment_service, webhook_service)


@broker.subscriber(queue=dlq_queue, exchange=dlx_exchange)
async def payment_new_dlq_handler(message: Dict[str, Any], raw_message: RabbitMessage) -> None:
    """Обработка события в очереди RabbitMQ `payments.new.dlq`"""
    logger.debug(f"Message: {raw_message.message_id}\n{repr(raw_message.headers)}\n{repr(message)}")


async def run_consumer() -> None:
    """Запуск потребителя"""
    logger.info("Consumer starting...")
    await broker.start()
    logger.info("Consumer started")

    try:
        await asyncio.Future()
    except KeyboardInterrupt:
        logger.info("Main task keyboard interrupt")
    finally:
        logger.info("Consumer shutdowning...")
        await broker.stop()
        logger.info("Consumer stopped")


if __name__ == "__main__":
    asyncio.run(run_consumer())
