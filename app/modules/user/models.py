from pydantic import EmailStr
from sqlmodel import Field, SQLModel

from app.core.mixin import DeletedAtMixin, TimestampMixin


class User(SQLModel, TimestampMixin, DeletedAtMixin, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    email: EmailStr = Field(index=True, nullable=False, unique=True)
    is_active: bool = Field(default=True, nullable=False)
    is_superuser: bool = Field(default=False, nullable=False)
    full_name: str | None = Field(default=None, nullable=True)
    hashed_password: str = Field(nullable=False)
