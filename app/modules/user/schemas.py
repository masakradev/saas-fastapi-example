from pydantic import EmailStr
from sqlmodel import Field, SQLModel

from app.core.mixin import TimestampMixin


class UserResponse(SQLModel, TimestampMixin):
    id: int | None = Field(default=None, primary_key=True)
    email: EmailStr = Field(nullable=False)
    is_superuser: bool = Field(default=False, nullable=False)
    full_name: str | None = Field(default=None, nullable=True)


class UserUpdate(SQLModel):
    email: EmailStr = Field(nullable=False, unique=True)
    full_name: str | None = Field(default=None, nullable=True)


class UserCreate(SQLModel):
    email: EmailStr = Field(nullable=False, unique=True)
    password: str = Field(nullable=False, min_length=8)
    full_name: str | None = Field(default=None, nullable=True)
