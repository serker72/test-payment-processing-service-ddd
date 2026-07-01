from typing import Any, Dict

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, Request, status

from src.domain.interfaces.services import IWebhookService
from src.presentation.utils.helpers import custom_json

webhook_router = APIRouter(prefix="/webhooks", tags=["Webhooks"], route_class=DishkaRoute)


@webhook_router.post("", response_model=Dict[str, str])
async def processing(data: Dict[str, Any], service: FromDishka[IWebhookService]):
    """Обработка вебхука"""
    response_data = await service.processing(data)
    return custom_json.CustomJSONResponse(
        content=response_data,
        status_code=status.HTTP_200_OK if response_data.get("status") == "success" else status.HTTP_400_BAD_REQUEST,
    )
