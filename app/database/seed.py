"""Sample data so the API is usable straight away in Swagger."""

from app.database.in_memory import InMemoryDatabase
from app.models import Book, Member, MembershipType
from app.repositories import BookRepository, MemberRepository


def _sample_books() -> list[Book]:
    return [
        Book(title="The Hobbit", author="J.R.R. Tolkien", isbn="9780547928227", total_copies=3, published_year=1937, genre="Fantasy"),
        Book(title="1984", author="George Orwell", isbn="9780451524935", total_copies=2, published_year=1949, genre="Dystopian"),
        Book(title="Clean Code", author="Robert C. Martin", isbn="9780132350884", total_copies=4, published_year=2008, genre="Programming"),
        Book(title="The Pragmatic Programmer", author="David Thomas, Andrew Hunt", isbn="9780135957059", total_copies=2, published_year=2019, genre="Programming"),
        Book(title="Dune", author="Frank Herbert", isbn="9780441172719", total_copies=1, published_year=1965, genre="Science Fiction"),
    ]


def _sample_members() -> list[Member]:
    return [
        Member(name="Asha Rao", email="asha.rao@example.com", phone="+91 90000 11111"),
        Member(name="John Smith", email="john.smith@example.com", membership_type=MembershipType.PREMIUM),
    ]


def seed_database(db: InMemoryDatabase) -> None:
    """Insert sample books and members if the store is empty."""
    books = BookRepository(db)
    members = MemberRepository(db)

    if books.count() == 0:
        for book in _sample_books():
            books.add(book)
    if members.count() == 0:
        for member in _sample_members():
            members.add(member)
