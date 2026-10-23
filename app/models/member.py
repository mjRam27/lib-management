"""Member domain model."""

from dataclasses import dataclass
from enum import Enum

from app.models.base import BaseEntity


class MembershipType(str, Enum):
    STANDARD = "standard"
    PREMIUM = "premium"


@dataclass(kw_only=True)
class Member(BaseEntity):
    """A registered library member who can borrow books."""

    name: str
    email: str
    phone: str | None = None
    membership_type: MembershipType = MembershipType.STANDARD
    is_active: bool = True

    def activate(self) -> None:
        self.is_active = True
        self.touch()

    def deactivate(self) -> None:
        self.is_active = False
        self.touch()
