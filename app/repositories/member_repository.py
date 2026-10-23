"""Member data access."""

from app.models.member import Member
from app.repositories.base import InMemoryRepository


class MemberRepository(InMemoryRepository[Member]):
    table_name = "members"

    def get_by_email(self, email: str) -> Member | None:
        email = email.lower()
        return self.find_one(lambda member: member.email.lower() == email)

    def search(
        self,
        name: str | None = None,
        is_active: bool | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Member]:
        name = name.lower() if name else None

        def matches(member: Member) -> bool:
            if name and name not in member.name.lower():
                return False
            if is_active is not None and member.is_active != is_active:
                return False
            return True

        return self.find(matches, skip, limit)
