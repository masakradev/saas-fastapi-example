from typing import Annotated
from uuid import UUID

import jwt
from fastapi import Depends, HTTPException, Path, Request, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.account import Account
from app.core.config import ALGORITHM, settings
from app.core.db import get_async_session
from app.modules.auth.schemas import TokenPayload
from app.modules.company.models import Company
from app.modules.user.models import User

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"/auth/access-token")

TokenDep = Annotated[str, Depends(reusable_oauth2)]
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


async def get_account(
    session: SessionDep, token: TokenDep, request: Request
) -> Account:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except InvalidTokenError, ValidationError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = await session.get(User, int(token_data.sub))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    company: Company | None = None
    company_id = request.path_params.get("company_id")
    if company_id:
        try:
            company = await session.get(Company, company_id)
            if not company:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Company not found",
                )
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid company ID format",
            )

    return Account(user=user, company=company)


AccountDep = Annotated[Account, Depends(get_account)]
