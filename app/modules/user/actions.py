from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.security import get_password_hash
from app.modules.user.models import User
from app.modules.user.schemas import UserCreate, UserUpdate


async def get_user(id: int, session: AsyncSession) -> User:
    user = await session.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_user_by_email(email: str, session: AsyncSession) -> User | None:
    statement = select(User).where(User.email == email)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def create_user(user_create: UserCreate, session: AsyncSession) -> User:
    user_create = {
        **user_create.model_dump(),
        "hashed_password": get_password_hash(user_create.password),
    }
    user = User.model_validate(user_create)
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


async def update_user(
    user: User, user_update: UserUpdate, session: AsyncSession
) -> User:
    update_dict = user_update.model_dump(exclude_unset=True)
    user.sqlmodel_update(update_dict)
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


async def delete_user(user: User, session: AsyncSession) -> User:
    user_delete = {
        "is_active": False,
        "deleted_at": datetime.now(),
    }

    user.sqlmodel_update(user_delete)
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user
