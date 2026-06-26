from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, TypeVar


@dataclass
class BaseEntity:
    id: Optional[int] = None

    # Audit fields
    created_at: Optional[datetime] = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        """Post-initialization validation and setup."""
        now = datetime.now(timezone.utc)
        if self.created_at is None:
            self.created_at = now
        if self.updated_at is None:
            self.updated_at = now

    def update_timestamp(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now(timezone.utc)

    def is_new(self) -> bool:
        """Check if this is a new entity (not persisted yet)."""
        return self.id is None


BaseEntityType = TypeVar("BaseEntityType", bound=BaseEntity)
