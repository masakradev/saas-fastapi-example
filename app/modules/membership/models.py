from sqlmodel import Field, SQLModel

from app.core.mixin import TimestampMixin


class Membership(SQLModel, TimestampMixin, table=True):
    __tablename__ = "memberships"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False, index=True)
    company_id: int = Field(foreign_key="companies.id", nullable=False, index=True)


class MembershipInvite(SQLModel, TimestampMixin, table=True):
    __tablename__ = "membership_invites"

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(nullable=False, index=True)
    company_id: int = Field(foreign_key="companies.id", nullable=False, index=True)
    user_id: int | None = Field(foreign_key="users.id", nullable=True, index=True)
    invited_by_id: int | None = Field(foreign_key="users.id", nullable=True, index=True)
