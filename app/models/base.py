"""Shared base class for all domain entities."""

from dataclasses import dataclass, field
from datetime import datetime, timezone


def utc_now() -> datetime:
    """Current time as a timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)


@dataclass(kw_only=True)
class BaseEntity:
    """Fields every persisted entity has. `id` is assigned by the repository."""

    id: int | None = None
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def touch(self) -> None:
        """Mark the entity as modified."""
        self.updated_at = utc_now()
