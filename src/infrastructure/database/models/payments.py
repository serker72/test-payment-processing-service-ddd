from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import DECIMAL, DateTime, Enum, SmallInteger, String
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_serializer import SerializerMixin

from src.domain.entities.payments import PaymentCurrencies, PaymentStatuses

from .base import BaseModel


class PaymentModel(BaseModel, SerializerMixin):
    __tablename__ = "payments"

    id: Mapped[UUID] = mapped_column(postgresql.UUID(as_uuid=True), nullable=False, default=uuid4, primary_key=True)
    amount: Mapped[Decimal] = mapped_column(DECIMAL(16, 2), nullable=False)
    currency: Mapped[PaymentCurrencies] = mapped_column(
        Enum(PaymentCurrencies, name="type_payment_currencies"),
        nullable=False,
        default=PaymentCurrencies.RUB,
    )
    description: Mapped[str] = mapped_column(String(), nullable=False)
    meta_data: Mapped[postgresql.JSONB] = mapped_column(postgresql.JSONB(none_as_null=True), nullable=False, default={})
    status: Mapped[PaymentStatuses] = mapped_column(
        Enum(PaymentStatuses, name="type_payment_statuses"),
        nullable=False,
        default=PaymentStatuses.pending,
    )
    idempotency_key: Mapped[str] = mapped_column(String(), nullable=False)
    webhook_url: Mapped[str] = mapped_column(String(), nullable=True)
    expired_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    processing_error_message: Mapped[str] = mapped_column(String(), nullable=True)
