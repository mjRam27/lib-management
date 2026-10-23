"""Loan data access."""

from app.models.loan import Loan, LoanStatus
from app.repositories.base import InMemoryRepository


class LoanRepository(InMemoryRepository[Loan]):
    table_name = "loans"

    def search(
        self,
        member_id: int | None = None,
        book_id: int | None = None,
        status: LoanStatus | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Loan]:
        def matches(loan: Loan) -> bool:
            if member_id is not None and loan.member_id != member_id:
                return False
            if book_id is not None and loan.book_id != book_id:
                return False
            if status is not None and loan.status != status:
                return False
            return True

        return self.find(matches, skip, limit)

    def active_loans_for_member(self, member_id: int) -> list[Loan]:
        return self.find(lambda loan: loan.member_id == member_id and not loan.is_returned, limit=10_000)

    def has_active_loan(self, member_id: int, book_id: int) -> bool:
        return self.find_one(
            lambda loan: loan.member_id == member_id and loan.book_id == book_id and not loan.is_returned
        ) is not None
