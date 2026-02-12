from collections.abc import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings


def get_test_engine() -> AsyncEngine:
    async_engine: AsyncEngine = create_async_engine(
        settings.SQLALCHEMY_DATABASE_URI(sync=False, test=True),
        future=True,
    )

    return async_engine


async def get_test_async_session() -> AsyncGenerator[AsyncSession, None]:
    async_engine = get_test_engine()

    async_session = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False,  # document this
    )

    async with async_session() as async_sess:
        yield async_sess


@pytest.fixture()
async def async_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_test_async_session():
        yield session
        break
