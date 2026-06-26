from fastapi import Depends

from src.application.services import PaymentService, WebhookService
from src.domain.entities import PaymentEntity
from src.domain.interfaces.repositories import IPaymentRepository
from src.domain.interfaces.services import IPaymentService, IWebhookService
from src.infrastructure.ioc.repositories import get_payment_repository


def get_payment_service(
    repository: IPaymentRepository = Depends(get_payment_repository),
) -> IPaymentService:
    return PaymentService(repository, PaymentEntity)


def get_webhook_service() -> IWebhookService:
    return WebhookService()
