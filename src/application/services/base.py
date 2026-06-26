from typing import Any, Dict, List, Optional, Type

from src.domain.entities import BaseEntity
from src.domain.interfaces.repositories import IBaseRepository
from src.domain.interfaces.services import IBaseService


class BaseService(IBaseService):
    """Базовый сервис"""

    def __init__(self, repository: IBaseRepository, entity_class: Type[BaseEntity]):
        self._repository = repository
        self._entity_class = entity_class

    def get_repository(self) -> IBaseRepository:
        """Получение экземпляра репозитория"""
        return self._repository

    async def create(self, data: Dict[str, Any]) -> BaseEntity:
        """Создание нового объекта"""
        if not data:
            raise ValueError(f"{self._entity_class.__class__.__name__} data cannot be empty")

        try:
            entity = self._entity_class(**data)
            return await self._repository.save(entity)
        except Exception as e:
            raise ValueError(f"Failed to create entity: {e}")

    async def retrieve(self, entity_id: int | str) -> Optional[BaseEntity]:
        """Получение данных объекта"""
        if not entity_id:
            raise ValueError(f"{self._entity_class.__class__.__name__} ID cannot be empty")

        return await self._repository.get_by_id(entity_id)

    async def list(self, limit: Optional[int] = None, offset: int = 0) -> List[BaseEntity]:
        """Получение списка объектов с пагинацией"""
        return await self._repository.list_all(limit=limit, offset=offset)

    async def update(self, entity_id: int | str, data: Dict[str, Any]) -> Optional[BaseEntity]:
        """Изменение данных объекта"""
        if not entity_id:
            raise ValueError(f"{self._entity_class.__class__.__name__} ID cannot be empty")

        if not data:
            raise ValueError("Update data cannot be empty")

        entity = await self._repository.get_by_id(entity_id)
        if entity:
            try:
                for key, value in data.items():
                    if hasattr(entity, key):
                        setattr(entity, key, value)
                return await self._repository.save(entity)
            except Exception as e:
                raise ValueError(f"Failed to update entity: {e}")
        return None

    async def delete(self, entity_id: int | str) -> bool:
        """Удаление объекта"""
        if not entity_id:
            raise ValueError(f"{self._entity_class.__class__.__name__} ID cannot be empty")

        return await self._repository.delete(entity_id)
