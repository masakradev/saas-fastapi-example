import logging
from typing import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

logger = logging.getLogger(__name__)


def get_async_engine() -> AsyncEngine:
    """Return async database engine."""
    try:
        async_engine: AsyncEngine = create_async_engine(
            settings.SQLALCHEMY_DATABASE_URI(),
            future=True,
        )

        return async_engine
    except SQLAlchemyError as e:
        logger.critical("Failed to create async database engine")

        raise e


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield an async session."""
    async_session = async_sessionmaker(
        bind=get_async_engine(),
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False,
    )
    async with async_session() as async_sess:
        try:

            yield async_sess

        except SQLAlchemyError as e:
            logger.critical("Database session error occurred")

            raise e
