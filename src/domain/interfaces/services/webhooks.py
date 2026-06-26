from abc import ABC, abstractmethod
from typing import Any, Dict


class IWebhookService(ABC):
    """Интерфейс сервиса для работы с вебхуками"""

    @abstractmethod
    async def send(self, url: str, payload: Dict[str, Any]) -> bool:
        """Отправка вебхука"""

    @abstractmethod
    async def processing(self, payload: Dict[str, Any]) -> dict:
        """Обработка вебхука"""
