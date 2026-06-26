from fastapi import APIRouter, Depends, HTTPException, Request, status
from idemptx import idempotent

from src.domain.entities import PaymentEntity, PaymentStatuses
from src.domain.interfaces.services import IPaymentService
from src.infrastructure.config.settings import settings
from src.infrastructure.external.redis import async_idemptx_backend
from src.infrastructure.ioc import get_payment_service
from src.presentation.api.routes.outbox import outbox_router
from src.presentation.api.schemas.payments import PaymentCreateRequest, PaymentCreateResponse, PaymentResponse
from src.presentation.utils.helpers import custom_json

payment_router = APIRouter(prefix="/payments", tags=["Payments"])


@payment_router.post("/", response_model=PaymentCreateResponse)
@idempotent(storage_backend=async_idemptx_backend)
async def create_payment(
    data: PaymentCreateRequest,
    request: Request,
    service: IPaymentService = Depends(get_payment_service),
):
    """Создание нового платежа"""
    entity: PaymentEntity = await service.create(
        {
            **data.model_dump(),
            **{
                "status": PaymentStatuses.pending.name,
                "idempotency_key": request.state.idempotency_key,
            },
        }
    )
    response_data = PaymentCreateResponse(payment_id=str(entity.id), status=entity.status, created_at=entity.created_at)
    await outbox_router.broker.publish(
        custom_json.loads(custom_json.custom_json_serializer(response_data)),
        queue=settings.consumer_queue_name,
        session=service.get_repository().get_session(),
    )
    return custom_json.CustomJSONResponse(content=response_data.model_dump(), status_code=status.HTTP_202_ACCEPTED)


@payment_router.get("/{payment_id}", response_model=PaymentResponse)
async def retrieve_payment(payment_id: str, service: IPaymentService = Depends(get_payment_service)):
    """Получение данных платежа"""
    entity = await service.retrieve(payment_id)
    if not entity:
        raise HTTPException(status_code=404, detail="PaymentEntity not found")
    return PaymentResponse.model_validate(entity)
