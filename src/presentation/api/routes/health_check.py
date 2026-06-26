from fastapi import APIRouter, Depends, HTTPException, Request, status

healthcheck_router = APIRouter(prefix="/healthcheck", tags=["Health check"])


@healthcheck_router.get("", response_model=dict)
async def health_check():
    """Проверка работоспособности сервиса"""
    return {"status": "healthy"}
