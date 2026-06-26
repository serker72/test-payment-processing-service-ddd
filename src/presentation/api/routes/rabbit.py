from faststream.rabbit.fastapi import RabbitRouter

from src.infrastructure.config.settings import settings

rabbit_router = RabbitRouter(settings.get_rabbitmq_url())
