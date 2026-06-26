from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities import PaymentEntity
from src.domain.interfaces.repositories import IPaymentRepository
from src.infrastructure.database.models import PaymentModel
from src.infrastructure.database.repositories import SQLAlchemyPaymentRepository
from src.infrastructure.database.sessions.base import get_session


def get_payment_repository(
    session: AsyncSession = Depends(get_session),
) -> IPaymentRepository:
    return SQLAlchemyPaymentRepository(session, PaymentModel, PaymentEntity)
