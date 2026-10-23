"""Book data access."""

from app.models.book import Book
from app.repositories.base import InMemoryRepository


class BookRepository(InMemoryRepository[Book]):
    table_name = "books"

    def get_by_isbn(self, isbn: str) -> Book | None:
        return self.find_one(lambda book: book.isbn == isbn)

    def search(
        self,
        query: str | None = None,
        author: str | None = None,
        genre: str | None = None,
        available_only: bool = False,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Book]:
        """Filter books. `query` matches title, author or ISBN (case-insensitive)."""
        query = query.lower() if query else None
        author = author.lower() if author else None
        genre = genre.lower() if genre else None

        def matches(book: Book) -> bool:
            if query and not (
                query in book.title.lower() or query in book.author.lower() or query in book.isbn.lower()
            ):
                return False
            if author and author not in book.author.lower():
                return False
            if genre and (book.genre is None or genre != book.genre.lower()):
                return False
            if available_only and not book.is_available:
                return False
            return True

        return self.find(matches, skip, limit)
