from datetime import datetime

from sqlalchemy import event
from sqlmodel import Field


class TimestampMixin:
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)


@event.listens_for(TimestampMixin, "before_update", propagate=True)
def receive_before_update(_mapper, _connection, target):
    """Update updated_at on every update."""
    target.updated_at = datetime.now()


class DeletedAtMixin:
    deleted_at: datetime | None = Field(default=None, nullable=True)
