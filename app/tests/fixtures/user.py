import pytest

from app.modules.user.models import User


async def create_user(async_session) -> User:
    user = User(
        email="test@example.com",
        hashed_password="hashedpassword",
        is_active=True,
        is_superuser=False,
        full_name="Test User",
    )

    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    return user


@pytest.fixture
async def user(async_session) -> User:
    return await create_user(async_session)
