from fastapi import APIRouter

from app.core.deps import AccountDep, SessionDep
from app.modules.user import actions
from app.modules.user.schemas import UserCreate, UserResponse, UserUpdate

router = APIRouter(tags=["users"])


@router.put("/", response_model=UserResponse)
async def update_user(
    user_update: UserUpdate, session: SessionDep, account: AccountDep
):
    user = await actions.update_user(account.user, user_update, session)

    return user


@router.post("/", status_code=201, response_model=UserResponse)
async def create_user(user_create: UserCreate, session: SessionDep):
    user = await actions.create_user(user_create, session)

    return user


@router.delete("/", response_model=UserResponse)
async def delete_user(session: SessionDep, account: AccountDep):
    # TODO - user can only delete themselves, so we need to get the user id from the token
    user = await actions.delete_user(account.user, session)

    return user
