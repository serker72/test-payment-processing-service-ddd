from asyncio import current_task
from typing import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from src.application.services import PaymentService, WebhookService
from src.domain.entities import PaymentEntity
from src.domain.interfaces.repositories import IPaymentRepository
from src.domain.interfaces.services import IPaymentService, IWebhookService
from src.infrastructure.config.settings import settings
from src.infrastructure.database.models import PaymentModel
from src.infrastructure.database.repositories import SQLAlchemyPaymentRepository


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_async_engine(self) -> AsyncEngine:
        """Создание асинхронного подключения к БД"""
        return create_async_engine(
            settings.get_postgres_url(),
            echo=settings.sa_debug,
            max_overflow=settings.sa_max_overflow,
            pool_size=settings.sa_pool_size,
            pool_timeout=settings.sa_pool_timeout,
            pool_recycle=settings.sa_pool_recycle,
            pool_use_lifo=settings.sa_pool_use_lifo,
            pool_pre_ping=settings.sa_pool_pre_ping,
        )

    @provide(scope=Scope.APP)
    def provide_async_session_maker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        """Создание фабрики для сессий"""
        return async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    @provide(scope=Scope.REQUEST)
    async def provide_async_session(
        self, session_factory: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        """Генератор сессии для запроса"""
        async_session = async_scoped_session(session_factory=session_factory, scopefunc=current_task)
        try:
            async with async_session() as session, session.begin():
                yield session
        except Exception:
            await async_session.rollback()
            raise
        finally:
            await async_session.remove()


class PaymentRepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def provide_payment_repository(self, session: AsyncSession) -> IPaymentRepository:
        return SQLAlchemyPaymentRepository(session, PaymentModel, PaymentEntity)


class PaymentServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def provide_payment_service(self, repository: IPaymentRepository) -> IPaymentService:
        return PaymentService(repository, PaymentEntity)


class WebhookServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def provide_payment_service(self) -> IWebhookService:
        return WebhookService()
