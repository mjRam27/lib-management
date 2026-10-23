"""Lending endpoints: borrow, return, renew and track loans."""

from typing import Annotated

from fastapi import APIRouter, Path, Query, status

from app.api.dependencies import LoanServiceDep
from app.models.loan import LoanStatus
from app.schemas.common import ErrorResponse
from app.schemas.loan import LoanCreate, LoanRead, LoanRenew

router = APIRouter(prefix="/loans", tags=["Loans"])

LoanId = Annotated[int, Path(ge=1, description="Loan ID")]
NOT_FOUND = {404: {"model": ErrorResponse, "description": "Loan, book or member not found"}}
RULE_VIOLATION = {
    400: {"model": ErrorResponse, "description": "Lending rule violated"},
    409: {"model": ErrorResponse, "description": "Conflict with current state"},
}


@router.post(
    "",
    response_model=LoanRead,
    status_code=status.HTTP_201_CREATED,
    summary="Borrow a book",
    responses={**NOT_FOUND, **RULE_VIOLATION},
)
def borrow_book(payload: LoanCreate, service: LoanServiceDep):
    return service.borrow_book(payload)


@router.get("", response_model=list[LoanRead], summary="List loans")
def list_loans(
    service: LoanServiceDep,
    member_id: Annotated[int | None, Query(ge=1)] = None,
    book_id: Annotated[int | None, Query(ge=1)] = None,
    status_filter: Annotated[LoanStatus | None, Query(alias="status")] = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    return service.list_loans(member_id, book_id, status_filter, skip, limit)


@router.get("/overdue", response_model=list[LoanRead], summary="List overdue loans")
def list_overdue_loans(
    service: LoanServiceDep,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    return service.list_overdue_loans(skip, limit)


@router.get("/{loan_id}", response_model=LoanRead, summary="Get a loan", responses=NOT_FOUND)
def get_loan(loan_id: LoanId, service: LoanServiceDep):
    return service.get_loan(loan_id)


@router.post(
    "/{loan_id}/return",
    response_model=LoanRead,
    summary="Return a borrowed book (fine is calculated if late)",
    responses={**NOT_FOUND, **RULE_VIOLATION},
)
def return_book(loan_id: LoanId, service: LoanServiceDep):
    return service.return_book(loan_id)


@router.post(
    "/{loan_id}/renew",
    response_model=LoanRead,
    summary="Extend a loan's due date",
    responses={**NOT_FOUND, **RULE_VIOLATION},
)
def renew_loan(loan_id: LoanId, service: LoanServiceDep, payload: LoanRenew | None = None):
    return service.renew_loan(loan_id, payload or LoanRenew())
