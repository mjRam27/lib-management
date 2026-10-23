"""Book domain model."""

from dataclasses import dataclass

from app.core.exceptions import BusinessRuleError, ConflictError
from app.models.base import BaseEntity


@dataclass(kw_only=True)
class Book(BaseEntity):
    """A title in the catalogue, possibly with several physical copies."""

    title: str
    author: str
    isbn: str
    total_copies: int = 1
    available_copies: int | None = None
    published_year: int | None = None
    genre: str | None = None

    def __post_init__(self) -> None:
        if self.available_copies is None:
            self.available_copies = self.total_copies

    @property
    def is_available(self) -> bool:
        return self.available_copies > 0

    @property
    def borrowed_copies(self) -> int:
        return self.total_copies - self.available_copies

    def check_out(self) -> None:
        """Take one copy off the shelf."""
        if not self.is_available:
            raise ConflictError(f"No copies of '{self.title}' are currently available.")
        self.available_copies -= 1
        self.touch()

    def check_in(self) -> None:
        """Put one copy back on the shelf."""
        if self.available_copies >= self.total_copies:
            raise ConflictError(f"All copies of '{self.title}' are already in the library.")
        self.available_copies += 1
        self.touch()

    def set_total_copies(self, new_total: int) -> None:
        """Change stock size while keeping currently borrowed copies accounted for."""
        if new_total < self.borrowed_copies:
            raise BusinessRuleError(
                f"Cannot set total copies to {new_total}: "
                f"{self.borrowed_copies} copies are currently borrowed."
            )
        self.available_copies = new_total - self.borrowed_copies
        self.total_copies = new_total
        self.touch()
