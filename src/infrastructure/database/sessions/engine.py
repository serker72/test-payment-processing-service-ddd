from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.infrastructure.config.settings import settings

engine = create_async_engine(
    settings.get_postgres_url(),
    echo=settings.sa_debug,
    max_overflow=settings.sa_max_overflow,
    pool_size=settings.sa_pool_size,
    pool_timeout=settings.sa_pool_timeout,
    pool_recycle=settings.sa_pool_recycle,
    pool_use_lifo=settings.sa_pool_use_lifo,
    pool_pre_ping=settings.sa_pool_pre_ping,
)
session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
