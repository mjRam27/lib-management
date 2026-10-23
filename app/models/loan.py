"""Loan domain model: one member borrowing one copy of a book."""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

from app.core.exceptions import BusinessRuleError, ConflictError
from app.models.base import BaseEntity, utc_now


class LoanStatus(str, Enum):
    ACTIVE = "active"
    OVERDUE = "overdue"
    RETURNED = "returned"


@dataclass(kw_only=True)
class Loan(BaseEntity):
    book_id: int
    member_id: int
    due_date: datetime
    borrowed_at: datetime = field(default_factory=utc_now)
    returned_at: datetime | None = None
    renewals: int = 0
    fine_amount: float = 0.0

    @property
    def is_returned(self) -> bool:
        return self.returned_at is not None

    @property
    def is_overdue(self) -> bool:
        return not self.is_returned and utc_now() > self.due_date

    @property
    def status(self) -> LoanStatus:
        if self.is_returned:
            return LoanStatus.RETURNED
        if self.is_overdue:
            return LoanStatus.OVERDUE
        return LoanStatus.ACTIVE

    def days_overdue(self, as_of: datetime | None = None) -> int:
        """Whole days past the due date (as of return date, or now if still out)."""
        reference = as_of or self.returned_at or utc_now()
        if reference <= self.due_date:
            return 0
        return (reference - self.due_date).days

    def calculate_fine(self, fine_per_day: float, as_of: datetime | None = None) -> float:
        return round(self.days_overdue(as_of) * fine_per_day, 2)

    def mark_returned(self, fine_per_day: float) -> None:
        if self.is_returned:
            raise ConflictError(f"Loan {self.id} has already been returned.")
        self.returned_at = utc_now()
        self.fine_amount = self.calculate_fine(fine_per_day, self.returned_at)
        self.touch()

    def renew(self, extra_days: int, max_renewals: int) -> None:
        if self.is_returned:
            raise ConflictError(f"Loan {self.id} has already been returned.")
        if self.is_overdue:
            raise BusinessRuleError("Overdue loans cannot be renewed. Please return the book.")
        if self.renewals >= max_renewals:
            raise BusinessRuleError(f"Loan has reached the maximum of {max_renewals} renewals.")
        self.due_date += timedelta(days=extra_days)
        self.renewals += 1
        self.touch()
