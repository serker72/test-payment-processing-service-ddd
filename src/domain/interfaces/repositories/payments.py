from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities.payments import PaymentEntity
from src.domain.interfaces.repositories.base import IBaseRepository


class IPaymentRepository(IBaseRepository[PaymentEntity], ABC):
    @abstractmethod
    async def list_all(self, limit: Optional[int] = None, offset: int = 0) -> List[PaymentEntity]:
        """Получение списка платежей с пагинацией"""

    @abstractmethod
    async def get_by_id(self, entity_id: str) -> PaymentEntity | None:
        """Получение данных платежа по ID"""

    @abstractmethod
    async def save(self, entity: PaymentEntity) -> PaymentEntity:
        """Сохранение платежа"""

    @abstractmethod
    async def delete(self, entity_id: str) -> bool:
        """Удаление платежа"""
