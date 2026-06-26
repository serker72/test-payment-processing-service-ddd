from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from src.domain.entities.payments import PaymentEntity
from src.domain.interfaces.repositories import IPaymentRepository
from src.domain.interfaces.services import IBaseService


class IPaymentService(IBaseService[PaymentEntity], ABC):
    """Интерфейс сервиса для работы с платежами"""

    @abstractmethod
    def get_repository(self) -> IPaymentRepository:
        """Получение экземпляра репозитория"""

    @abstractmethod
    async def create(self, data: Dict[str, Any]) -> PaymentEntity:
        """Создание платежа"""

    @abstractmethod
    async def retrieve(self, entity_id: int | str) -> PaymentEntity | None:
        """Получение данных платежа по ID"""

    @abstractmethod
    async def list(self, limit: Optional[int] = None, offset: int = 0) -> List[PaymentEntity]:
        """Получение списка платежей с пагинацией"""

    @abstractmethod
    async def update(self, entity_id: int | str, data: Dict[str, Any]) -> PaymentEntity:
        """Изменение данных платежа"""

    @abstractmethod
    async def delete(self, entity_id: int | str) -> bool:
        """Удаление платежа"""
