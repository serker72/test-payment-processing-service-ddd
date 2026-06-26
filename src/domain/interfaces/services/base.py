from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional

from src.domain.entities import BaseEntity, BaseEntityType
from src.domain.interfaces.repositories import IBaseRepository


class IBaseService(Generic[BaseEntityType], ABC):
    """Интерфейс базового сервиса"""

    @abstractmethod
    def get_repository(self) -> IBaseRepository:
        """Получение экземпляра репозитория"""

    @abstractmethod
    async def create(self, data: Dict[str, Any]) -> BaseEntity:
        """Создание объекта"""

    @abstractmethod
    async def retrieve(self, entity_id: int | str) -> BaseEntity | None:
        """Получение данных объекта по ID"""

    @abstractmethod
    async def list(self, limit: Optional[int] = None, offset: int = 0) -> List[BaseEntity]:
        """Получение списка объектов с пагинацией"""

    @abstractmethod
    async def update(self, entity_id: int | str, data: Dict[str, Any]) -> BaseEntity:
        """Изменение данных объекта"""

    @abstractmethod
    async def delete(self, entity_id: int | str) -> bool:
        """Удаление объекта"""
