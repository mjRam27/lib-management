"""Business logic for borrowing, returning and renewing books."""

from datetime import timedelta

from app.core.config import Settings
from app.core.exceptions import BusinessRuleError, ConflictError, NotFoundError
from app.database.in_memory import InMemoryDatabase
from app.models.base import utc_now
from app.models.book import Book
from app.models.loan import Loan, LoanStatus
from app.models.member import Member, MembershipType
from app.repositories.book_repository import BookRepository
from app.repositories.loan_repository import LoanRepository
from app.repositories.member_repository import MemberRepository
from app.schemas.loan import LoanCreate, LoanRenew


class LoanService:
    def __init__(
        self,
        db: InMemoryDatabase,
        loans: LoanRepository,
        books: BookRepository,
        members: MemberRepository,
        settings: Settings,
    ) -> None:
        self._db = db
        self._loans = loans
        self._books = books
        self._members = members
        self._settings = settings

    def borrow_book(self, data: LoanCreate) -> Loan:
        loan_days = data.loan_days or self._settings.default_loan_days
        if loan_days > self._settings.max_loan_days:
            raise BusinessRuleError(f"Loan period cannot exceed {self._settings.max_loan_days} days.")

        # Multi-step operation: check rules, take a copy, record the loan - all or nothing.
        with self._db.transaction():
            member = self._get_member(data.member_id)
            book = self._get_book(data.book_id)
            self._check_member_can_borrow(member, book)

            book.check_out()
            self._books.update(book)
            loan = Loan(
                book_id=book.id,
                member_id=member.id,
                due_date=utc_now() + timedelta(days=loan_days),
            )
            return self._loans.add(loan)

    def return_book(self, loan_id: int) -> Loan:
        with self._db.transaction():
            loan = self.get_loan(loan_id)
            loan.mark_returned(self._settings.fine_per_day)

            book = self._books.get(loan.book_id)
            if book is not None:
                book.check_in()
                self._books.update(book)
            return self._loans.update(loan)

    def renew_loan(self, loan_id: int, data: LoanRenew) -> Loan:
        with self._db.transaction():
            loan = self.get_loan(loan_id)
            loan.renew(data.extra_days, self._settings.max_renewals)
            return self._loans.update(loan)

    def get_loan(self, loan_id: int) -> Loan:
        loan = self._loans.get(loan_id)
        if loan is None:
            raise NotFoundError(f"Loan with id {loan_id} not found.")
        return loan

    def list_loans(
        self,
        member_id: int | None = None,
        book_id: int | None = None,
        status: LoanStatus | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Loan]:
        return self._loans.search(member_id, book_id, status, skip, limit)

    def list_overdue_loans(self, skip: int = 0, limit: int = 100) -> list[Loan]:
        return self._loans.search(status=LoanStatus.OVERDUE, skip=skip, limit=limit)

    def list_member_loans(
        self, member_id: int, status: LoanStatus | None = None, skip: int = 0, limit: int = 100
    ) -> list[Loan]:
        self._get_member(member_id)
        return self._loans.search(member_id=member_id, status=status, skip=skip, limit=limit)

    def _check_member_can_borrow(self, member: Member, book: Book) -> None:
        if not member.is_active:
            raise BusinessRuleError(f"Member '{member.name}' is inactive and cannot borrow books.")

        active_loans = self._loans.active_loans_for_member(member.id)
        if any(loan.is_overdue for loan in active_loans):
            raise BusinessRuleError("Member has overdue books. Return them before borrowing more.")

        limit = self._loan_limit(member.membership_type)
        if len(active_loans) >= limit:
            raise BusinessRuleError(f"Member has reached the limit of {limit} active loans.")

        if self._loans.has_active_loan(member.id, book.id):
            raise ConflictError(f"Member already has '{book.title}' on loan.")

    def _loan_limit(self, membership_type: MembershipType) -> int:
        if membership_type is MembershipType.PREMIUM:
            return self._settings.max_loans_premium
        return self._settings.max_loans_standard

    def _get_member(self, member_id: int) -> Member:
        member = self._members.get(member_id)
        if member is None:
            raise NotFoundError(f"Member with id {member_id} not found.")
        return member

    def _get_book(self, book_id: int) -> Book:
        book = self._books.get(book_id)
        if book is None:
            raise NotFoundError(f"Book with id {book_id} not found.")
        return book
