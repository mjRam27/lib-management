"""Business logic for library members."""

from app.core.exceptions import ConflictError, NotFoundError
from app.models.member import Member
from app.repositories.loan_repository import LoanRepository
from app.repositories.member_repository import MemberRepository
from app.schemas.member import MemberCreate, MemberUpdate


class MemberService:
    def __init__(self, members: MemberRepository, loans: LoanRepository) -> None:
        self._members = members
        self._loans = loans

    def register_member(self, data: MemberCreate) -> Member:
        self._ensure_email_unique(data.email)
        return self._members.add(Member(**data.model_dump()))

    def get_member(self, member_id: int) -> Member:
        member = self._members.get(member_id)
        if member is None:
            raise NotFoundError(f"Member with id {member_id} not found.")
        return member

    def list_members(
        self,
        name: str | None = None,
        is_active: bool | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Member]:
        return self._members.search(name, is_active, skip, limit)

    def update_member(self, member_id: int, data: MemberUpdate) -> Member:
        member = self.get_member(member_id)
        changes = data.model_dump(exclude_unset=True)

        if "email" in changes and changes["email"].lower() != member.email.lower():
            self._ensure_email_unique(changes["email"])
        if "is_active" in changes:
            if changes.pop("is_active"):
                member.activate()
            else:
                member.deactivate()

        for field, value in changes.items():
            setattr(member, field, value)
        return self._members.update(member)

    def delete_member(self, member_id: int) -> None:
        member = self.get_member(member_id)
        active_loans = self._loans.active_loans_for_member(member_id)
        if active_loans:
            raise ConflictError(
                f"Cannot delete '{member.name}': {len(active_loans)} book(s) not yet returned."
            )
        self._members.delete(member_id)

    def _ensure_email_unique(self, email: str) -> None:
        if self._members.get_by_email(email) is not None:
            raise ConflictError(f"A member with email {email} already exists.")
