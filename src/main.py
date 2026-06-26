import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from src.infrastructure.config import constants as c
from src.infrastructure.config.settings import settings
from src.presentation.api.middlewares import ApiKeyHeaderMiddleware, RequestProcessingTimeMiddleware
from src.presentation.api.routes import healthcheck_router, outbox_router, payment_router, rabbit_router, webhook_router
from src.presentation.utils.helpers.custom_json import CustomJSONResponse

without_authentication_endpoints = ["/", "/docs", "/redoc", "/openapi.json", "/healthcheck", "/webhooks"]

log_level = "DEBUG" if settings.debug is True else "INFO"
logger.remove()
logger.add(sys.stderr, format=c.FORMAT_LOG_APP, level=log_level)
log_extra = {"request_id": "-", "user_ip": "-"}
logger.configure(extra=log_extra)


app = FastAPI(
    title="Test Tasks: Payment Processing Service DDD",
    version="0.1.0",
    default_response_class=CustomJSONResponse,
)

app.add_middleware(RequestProcessingTimeMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_allow_origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    ApiKeyHeaderMiddleware,
    key_value=settings.backend_authentication_header_value,
    header_name=settings.backend_authentication_header_key,
    ignored_endpoints=without_authentication_endpoints,
)

app.include_router(payment_router, prefix=settings.backend_api_prefix)
app.include_router(outbox_router)
app.include_router(rabbit_router)
app.include_router(healthcheck_router)
app.include_router(webhook_router)


@rabbit_router.publisher(settings.consumer_queue_name)
@outbox_router.subscriber(settings.consumer_queue_name)
async def outbox_handler(body: dict) -> dict:
    """Обработка события в очереди Outbox"""
    return body
