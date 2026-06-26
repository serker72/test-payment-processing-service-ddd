import asyncio
import json
import random
from typing import Any, Dict

import httpx
from loguru import logger

from src.domain.exceptions import WebhookDeliveryError
from src.domain.interfaces.services import IWebhookService
from src.infrastructure.config.settings import settings
from src.presentation.utils.helpers import custom_json


class WebhookService(IWebhookService):
    """Сервис для работы с вебхуками"""

    async def send(self, url: str, payload: Dict[str, Any]) -> bool:
        """Отправка вебхука"""
        webhook_responses = {}

        for attempt in range(settings.backend_webhook_retry_attempts):
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.post(
                        url, json=custom_json.loads(custom_json.custom_json_serializer(payload))
                    )
                    response.raise_for_status()
                    logger.info(f"Webhook for payment successfully sent to URL {url}")
                    data = response.json()
                    webhook_responses[f"attempt-{attempt + 1}"] = data
                    return True
            except Exception as e:
                if isinstance(e, json.JSONDecodeError):
                    webhook_responses[f"attempt-{attempt + 1}"] = response.text
                    return True
                elif isinstance(e, (httpx.HTTPStatusError, httpx.RequestError)):
                    logger.warning(f"Webhook for payment send error: {str(e)}")
                else:
                    logger.error(f"Webhook for payment send unexpected error: {str(e)}")

                webhook_responses[f"attempt-{attempt + 1}"] = str(e)

                if attempt < settings.backend_webhook_retry_attempts - 1:
                    delay = settings.backend_webhook_retry_delay_base * (2**attempt)
                    await asyncio.sleep(delay)

        logger.error("Attempts to send a webhook for payment have been exhausted")
        raise WebhookDeliveryError()

    async def processing(self, payload: Dict[str, Any]) -> dict:
        """Обработка вебхука"""
        return {"status": "error" if random.random() >= settings.backend_payment_success_rate else "success"}
