from collections.abc import AsyncGenerator
from os import environ

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings


def set_test_env():
    environ["ENV"] = "TEST"


def pytest_configure():
    set_test_env()
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


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
