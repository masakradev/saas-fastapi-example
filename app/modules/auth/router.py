from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.core.deps import SessionDep
from app.modules.auth.actions import authenticate, create_access_token
from app.modules.auth.schemas import Token

router = APIRouter(tags=["auth"])


@router.post("/access-token")
async def access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep
) -> Token:
    """
    OAuth2 compatible token login, get an access token
    """
    user = await authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return Token(access_token=create_access_token(user.id))
