"""Loan request/response schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.loan import LoanStatus


class LoanCreate(BaseModel):
    """Borrow a book. `loan_days` defaults to the configured standard period."""

    model_config = ConfigDict(json_schema_extra={"example": {"book_id": 1, "member_id": 1, "loan_days": 14}})

    book_id: int = Field(ge=1)
    member_id: int = Field(ge=1)
    loan_days: int | None = Field(default=None, ge=1)


class LoanRenew(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {"extra_days": 7}})

    extra_days: int = Field(default=7, ge=1, le=30)


class LoanRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    book_id: int
    member_id: int
    borrowed_at: datetime
    due_date: datetime
    returned_at: datetime | None
    status: LoanStatus
    is_overdue: bool
    renewals: int
    fine_amount: float
    created_at: datetime
    updated_at: datetime
