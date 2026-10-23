"""Member management endpoints."""

from typing import Annotated

from fastapi import APIRouter, Path, Query, status

from app.api.dependencies import LoanServiceDep, MemberServiceDep
from app.models.loan import LoanStatus
from app.schemas.common import ErrorResponse
from app.schemas.loan import LoanRead
from app.schemas.member import MemberCreate, MemberRead, MemberUpdate

router = APIRouter(prefix="/members", tags=["Members"])

MemberId = Annotated[int, Path(ge=1, description="Member ID")]
NOT_FOUND = {404: {"model": ErrorResponse, "description": "Member not found"}}
CONFLICT = {409: {"model": ErrorResponse, "description": "Conflict with current state"}}


@router.post(
    "",
    response_model=MemberRead,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new member",
    responses=CONFLICT,
)
def register_member(payload: MemberCreate, service: MemberServiceDep):
    return service.register_member(payload)


@router.get("", response_model=list[MemberRead], summary="List / search members")
def list_members(
    service: MemberServiceDep,
    name: Annotated[str | None, Query(description="Partial name match")] = None,
    is_active: bool | None = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    return service.list_members(name, is_active, skip, limit)


@router.get("/{member_id}", response_model=MemberRead, summary="Get a member", responses=NOT_FOUND)
def get_member(member_id: MemberId, service: MemberServiceDep):
    return service.get_member(member_id)


@router.patch(
    "/{member_id}",
    response_model=MemberRead,
    summary="Update a member (including activate/deactivate)",
    responses={**NOT_FOUND, **CONFLICT},
)
def update_member(member_id: MemberId, payload: MemberUpdate, service: MemberServiceDep):
    return service.update_member(member_id, payload)


@router.delete(
    "/{member_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a member",
    responses={**NOT_FOUND, **CONFLICT},
)
def delete_member(member_id: MemberId, service: MemberServiceDep) -> None:
    service.delete_member(member_id)


@router.get(
    "/{member_id}/loans",
    response_model=list[LoanRead],
    summary="List a member's loans",
    responses=NOT_FOUND,
)
def list_member_loans(
    member_id: MemberId,
    service: LoanServiceDep,
    status_filter: Annotated[LoanStatus | None, Query(alias="status")] = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    return service.list_member_loans(member_id, status_filter, skip, limit)
