from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Optional
from uuid import UUID, uuid4

from .base import BaseEntity


class PaymentStatuses(StrEnum):
    pending = "pending"
    succeeded = "succeeded"
    failed = "failed"


class PaymentCurrencies(StrEnum):
    RUB = "RUB"
    USD = "USD"
    EUR = "EUR"


@dataclass
class PaymentMetaData:
    address: str
    fio: str
    exp_date: Optional[str] = None
    bank: Optional[str] = None
    phone: Optional[str] = None


@dataclass
class PaymentEntity(BaseEntity):
    id: UUID = field(default_factory=uuid4)

    amount: Decimal = field(default_factory=Decimal)
    currency: str = field(default_factory=PaymentCurrencies.RUB)
    description: str = field(default_factory=str)
    meta_data: PaymentMetaData = field(default_factory=PaymentMetaData)
    status: str = field(default_factory=str)
    idempotency_key: str = field(default_factory=str)

    webhook_url: Optional[str] = None
    expired_at: Optional[datetime] = None
    processing_error_message: Optional[str] = None
