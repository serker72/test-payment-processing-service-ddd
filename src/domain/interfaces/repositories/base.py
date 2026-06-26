from abc import ABC, abstractmethod
from typing import Generic, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.base import BaseEntityType


class IBaseRepository(Generic[BaseEntityType], ABC):
    @abstractmethod
    def get_session(self) -> AsyncSession:
        """Получение экземпляра репозитория"""

    @abstractmethod
    async def list_all(self, limit: Optional[int] = None, offset: int = 0) -> List[BaseEntityType]:
        """Получение списка объектов с пагинацией"""

    @abstractmethod
    async def get_by_id(self, entity_id: int | str) -> BaseEntityType | None:
        """Получение данных объекта по ID"""

    @abstractmethod
    async def save(self, entity: BaseEntityType) -> BaseEntityType:
        """Сохранение объекта"""

    @abstractmethod
    async def delete(self, entity_id: int | str) -> bool:
        """Удаление объекта"""
