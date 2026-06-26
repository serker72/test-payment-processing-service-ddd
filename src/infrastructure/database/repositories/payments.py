from typing import List, Optional

from src.domain.entities import PaymentEntity
from src.domain.interfaces.repositories import IPaymentRepository
from src.infrastructure.database.repositories import SQLAlchemyBaseRepository


class SQLAlchemyPaymentRepository(SQLAlchemyBaseRepository, IPaymentRepository):
    """Репозиторий SQLAlchemy для платежей"""

    async def list_all(self, limit: Optional[int] = None, offset: int = 0) -> List[PaymentEntity]:
        """Получение списка платежей с пагинацией"""
        return await super().list_all(limit, offset)

    async def get_by_id(self, entity_id: str) -> Optional[PaymentEntity]:
        """Получение данных платежа по ID"""
        return await super().get_by_id(entity_id)

    async def save(self, entity: PaymentEntity) -> PaymentEntity:
        """Сохранение платежа"""
        return await super().save(entity)

    async def delete(self, entity_id: str) -> bool:
        """Удаление платежа"""
        return await super().delete(entity_id)
