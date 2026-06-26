from typing import Any, Dict, List, Optional
from uuid import UUID

from src.domain.entities.payments import PaymentEntity
from src.domain.interfaces.services import IPaymentService

from .base import BaseService


class PaymentService(BaseService, IPaymentService):
    """Сервис для работы с платежами"""

    async def create(self, data: Dict[str, Any]) -> PaymentEntity:
        """Создание нового платежа"""
        return await super().create(data)

    async def retrieve(self, entity_id: int | str) -> Optional[PaymentEntity]:
        """Получение данных платежа"""
        return await super().retrieve(entity_id)

    async def list(self, limit: Optional[int] = None, offset: int = 0) -> List[PaymentEntity]:
        """Получение списка платежей с пагинацией"""
        return await super().list(limit, offset)

    async def update(self, entity_id: int | str, data: Dict[str, Any]) -> Optional[PaymentEntity]:
        """Изменение данных платежа"""
        return await super().update(entity_id, data)

    async def delete(self, entity_id: UUID) -> bool:
        """Удаление платежа"""
        return await super().delete(entity_id)
