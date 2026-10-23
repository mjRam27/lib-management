"""Repositories: the only layer that talks to the data store."""

from app.repositories.base import AbstractRepository, InMemoryRepository
from app.repositories.book_repository import BookRepository
from app.repositories.loan_repository import LoanRepository
from app.repositories.member_repository import MemberRepository

__all__ = [
    "AbstractRepository",
    "BookRepository",
    "InMemoryRepository",
    "LoanRepository",
    "MemberRepository",
]
