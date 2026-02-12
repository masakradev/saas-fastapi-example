from datetime import datetime, timedelta, timezone
from typing import Any

from jwt import encode
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import ALGORITHM, settings
from app.core.security import verify_password
from app.modules.user.actions import get_user_by_email


async def authenticate(session: AsyncSession, email: str, password: str):
    user = await get_user_by_email(email=email, session=session)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(subject: str | Any) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
