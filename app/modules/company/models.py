from sqlmodel import Field, SQLModel

from app.core.mixin import DeletedAtMixin, TimestampMixin


class Company(SQLModel, TimestampMixin, DeletedAtMixin, table=True):
    __tablename__ = "companies"

    id: int = Field(primary_key=True)
    name: str = Field(nullable=False)
    slug: str = Field(index=True, nullable=False, unique=True)
    is_active: bool = Field(default=True, nullable=False)
