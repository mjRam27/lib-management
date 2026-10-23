"""Dependency-injection wiring: builds repositories and services per request.

This is the single place to change when switching storage backends.
"""

from typing import Annotated

from fastapi import Depends

from app.core.config import Settings, get_settings
from app.database import InMemoryDatabase, get_db
from app.repositories import BookRepository, LoanRepository, MemberRepository
from app.services import BookService, LoanService, MemberService

DatabaseDep = Annotated[InMemoryDatabase, Depends(get_db)]
SettingsDep = Annotated[Settings, Depends(get_settings)]


# Repositories
def get_book_repository(db: DatabaseDep) -> BookRepository:
    return BookRepository(db)


def get_member_repository(db: DatabaseDep) -> MemberRepository:
    return MemberRepository(db)


def get_loan_repository(db: DatabaseDep) -> LoanRepository:
    return LoanRepository(db)


BookRepositoryDep = Annotated[BookRepository, Depends(get_book_repository)]
MemberRepositoryDep = Annotated[MemberRepository, Depends(get_member_repository)]
LoanRepositoryDep = Annotated[LoanRepository, Depends(get_loan_repository)]


# Services
def get_book_service(books: BookRepositoryDep) -> BookService:
    return BookService(books)


def get_member_service(members: MemberRepositoryDep, loans: LoanRepositoryDep) -> MemberService:
    return MemberService(members, loans)


def get_loan_service(
    db: DatabaseDep,
    loans: LoanRepositoryDep,
    books: BookRepositoryDep,
    members: MemberRepositoryDep,
    settings: SettingsDep,
) -> LoanService:
    return LoanService(db, loans, books, members, settings)


BookServiceDep = Annotated[BookService, Depends(get_book_service)]
MemberServiceDep = Annotated[MemberService, Depends(get_member_service)]
LoanServiceDep = Annotated[LoanService, Depends(get_loan_service)]
