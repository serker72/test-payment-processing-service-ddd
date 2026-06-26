from dataclasses import asdict
from datetime import datetime
from typing import Type, TypeVar

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy_serializer import SerializerMixin

from src.domain.entities import BaseEntity


class BaseModel(DeclarativeBase, SerializerMixin):
    """Базовый класс модели"""

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now, onupdate=func.now)

    def to_entity(self, entity_class: Type[BaseEntity]) -> BaseEntity:
        """Convert model to domain entity."""
        return entity_class(**{k: v for k, v in self.__dict__.items() if not k.startswith("_")})

    @classmethod
    def from_entity(cls, entity: BaseEntity):
        """Create model from domain entity."""
        return cls(**asdict(entity))


BaseModelType = TypeVar("BaseModelType", bound=BaseModel)
