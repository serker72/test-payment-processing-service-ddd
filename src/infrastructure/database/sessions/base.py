from asyncio import current_task
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

from src.infrastructure.database.sessions.engine import session_factory


async def get_session() -> AsyncIterator[AsyncSession]:
    """Получение сессии SQLAlchemy"""
    async_session = async_scoped_session(session_factory=session_factory, scopefunc=current_task)
    try:
        async with async_session() as session, session.begin():
            yield session
    except Exception:
        await async_session.rollback()
        raise
    finally:
        await async_session.remove()


@asynccontextmanager
async def get_session_context() -> AsyncIterator[AsyncSession]:
    """Получение сессии SQLAlchemy для контекстного менеджера"""
    async_session = async_scoped_session(session_factory=session_factory, scopefunc=current_task)
    try:
        async with async_session() as session, session.begin():
            yield session
    except Exception:
        await async_session.rollback()
        raise
    finally:
        await async_session.remove()
