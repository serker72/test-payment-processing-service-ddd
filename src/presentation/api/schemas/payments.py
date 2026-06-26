from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PaymentMetaData(BaseModel):
    """Схема общих метаданных платежа"""

    address: str = Field(description="Номер карты/кошелька")
    fio: str = Field(default=None, description="ФИО владельца карты/кошелька")
    exp_date: str | None = Field(default=None, description="Срок действия карты")
    bank: str | None = Field(default=None, description="Наименование банка")
    phone: str | None = Field(default=None, description="Номер телефона")


class PaymentBase(BaseModel):
    """Схема общих данных платежа"""

    amount: Decimal = Field(description="Сумма")
    currency: str = Field(description="Валюта")
    description: str = Field(description="Описание")
    meta_data: PaymentMetaData = Field(description="Метаданные")
    webhook_url: str | None = Field(default=None, description="URL для уведомления о результате")
    expired_at: datetime | None = Field(default=None, description="Срок действия")


class PaymentExtend(BaseModel):
    """Схема дополнительных данных платежа"""

    status: str = Field(description="Статус")
    idempotency_key: str = Field(description="Уникальный ключ для защиты от дублей")


class PaymentResponse(PaymentBase, PaymentExtend):
    """Схема данных платежа"""

    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(description="ID платежа")
    created_at: datetime = Field(description="Время создания")
    updated_at: datetime | None = Field(default=None, description="Время изменения")
    processing_error_message: str | None = Field(default=None, description="Сообщение об ошибке обработки")


class PaymentCreateRequest(PaymentBase):
    """Схема запроса создания платежа"""


class PaymentCreateExtendedRequest(PaymentBase, PaymentExtend):
    """Схема запроса создания платежа"""


class PaymentCreateResponse(BaseModel):
    """Схема ответа на запрос создания платежа"""

    payment_id: str = Field(description="ID платежа")
    status: str = Field(description="Статус")
    created_at: datetime = Field(description="Время создания")
