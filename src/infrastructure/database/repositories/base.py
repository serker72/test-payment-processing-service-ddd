from dataclasses import asdict
from typing import List, Optional, Type
from uuid import uuid4

from sqlalchemy import delete, select
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities import BaseEntity
from src.domain.interfaces.repositories import IBaseRepository
from src.infrastructure.database.models import BaseModel


class SQLAlchemyBaseRepository(IBaseRepository):
    """Репозиторий SQLAlchemy для платежей"""

    def __init__(self, session: AsyncSession, model_class: Type[BaseModel], entity_class: Type[BaseEntity]):
        self._session = session
        self._model_class = model_class
        self._entity_class = entity_class

    def get_session(self) -> AsyncSession:
        """Получение экземпляра репозитория"""
        return self._session

    async def list_all(self, limit: Optional[int] = None, offset: int = 0) -> List[BaseEntity]:
        """Получение списка объектов с пагинацией"""
        statement = select(self._model_class).limit(limit).offset(offset)
        statement_result = await self._session.execute(statement)
        return [model.to_entity(self._entity_class) for model in statement_result.scalars().all()]

    async def get_by_id(self, entity_id: str) -> Optional[BaseEntity]:
        """Получение данных объекта по ID"""
        statement = select(self._model_class).where(self._model_class.id == entity_id)
        statement_result = await self._session.execute(statement)
        model = statement_result.scalar()

        return model.to_entity(self._entity_class) if model else None

    async def save(self, entity: BaseEntity) -> BaseEntity:
        """Сохранение объекта"""
        if entity.id:
            statement = select(self._model_class).where(self._model_class.id == entity.id)
            statement_result = await self._session.execute(statement)
            model = statement_result.scalar()

            if model:
                for key, value in asdict(entity).items():
                    if hasattr(model, key) and key != "id":
                        setattr(model, key, value)
            else:
                model = self._model_class.from_entity(entity)
                self._session.add(model)
        else:
            if isinstance(self._model_class.id.type, postgresql.UUID):
                entity.id = uuid4()

            model = self._model_class.from_entity(entity)
            self._session.add(model)

        if self._session.in_transaction():
            await self._session.flush([model])
        else:
            await self._session.commit()

        await self._session.refresh(model)

        return model.to_entity(self._entity_class)

    async def delete(self, entity_id: str) -> bool:
        """Удаление объекта"""
        statement = delete(self._model_class).where(self._model_class.id == entity_id).returning(self._model_class.id)
        statement_result = await self._session.execute(statement)
        model_id = statement_result.scalar()

        if model_id:
            if self._session.in_transaction():
                await self._session.flush()
            else:
                await self._session.commit()

            return True

        return False
