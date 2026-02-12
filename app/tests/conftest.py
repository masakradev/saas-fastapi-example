import logging
from collections.abc import AsyncGenerator
from os import environ

import pytest
from alembic import command
from alembic.config import Config
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.account import Account
from app.core.config import settings
from app.core.db import get_async_session
from app.core.deps import get_account
from app.main import app
from app.modules.company.models import Company
from app.modules.user.models import User
from app.tests.fixtures.user import user  # noqa: F401

models = [User, Company]

pytestmark = pytest.mark.anyio


def set_test_env():
    environ["ENV"] = "TEST"


def pytest_configure():
    logging.disable(logging.CRITICAL)
    set_test_env()
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


def get_test_engine() -> AsyncEngine:
    async_engine: AsyncEngine = create_async_engine(
        settings.SQLALCHEMY_DATABASE_URI(sync=False, test=True),
        future=True,
    )

    return async_engine


@pytest.fixture()
async def async_session() -> AsyncGenerator[AsyncSession, None]:
    async_engine = get_test_engine()

    async_session = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False,  # document this
    )

    async with async_session() as async_sess:
        yield async_sess


@pytest.fixture(autouse=True)
async def cleanup_db(anyio_backend, async_session) -> None:
    for x in models:
        await async_session.execute(delete(x))
    await async_session.commit()


@pytest.fixture()
async def async_client(user, async_session):
    async def _get_test_async_session() -> AsyncGenerator[AsyncSession, None]:
        yield async_session

    async def _get_test_account() -> Account:
        return Account(user=user, company=None)

    app.dependency_overrides[get_async_session] = _get_test_async_session
    app.dependency_overrides[get_account] = _get_test_account
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
