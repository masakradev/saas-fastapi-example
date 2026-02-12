from datetime import datetime

from sqlalchemy import event
from sqlalchemy.orm import Mapped, mapped_column
from sqlmodel import Field, SQLModel


class TimestampMixin(SQLModel):
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )


@event.listens_for(TimestampMixin, "before_update", propagate=True)
def receive_before_update(_mapper, _connection, target):
    """Update updated_at on every update."""
    target.updated_at = datetime.now()


class DeletedAtMixin(SQLModel):
    deleted_at: Mapped[datetime | None] = mapped_column(default=None)
