"""Business logic for the book catalogue."""

from app.core.exceptions import ConflictError, NotFoundError
from app.models.book import Book
from app.repositories.book_repository import BookRepository
from app.schemas.book import BookCreate, BookUpdate


class BookService:
    def __init__(self, books: BookRepository) -> None:
        self._books = books

    def create_book(self, data: BookCreate) -> Book:
        self._ensure_isbn_unique(data.isbn)
        return self._books.add(Book(**data.model_dump()))

    def get_book(self, book_id: int) -> Book:
        book = self._books.get(book_id)
        if book is None:
            raise NotFoundError(f"Book with id {book_id} not found.")
        return book

    def list_books(
        self,
        search: str | None = None,
        author: str | None = None,
        genre: str | None = None,
        available_only: bool = False,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Book]:
        return self._books.search(search, author, genre, available_only, skip, limit)

    def update_book(self, book_id: int, data: BookUpdate) -> Book:
        book = self.get_book(book_id)
        changes = data.model_dump(exclude_unset=True)

        if "isbn" in changes and changes["isbn"] != book.isbn:
            self._ensure_isbn_unique(changes["isbn"])
        if "total_copies" in changes:
            book.set_total_copies(changes.pop("total_copies"))

        for field, value in changes.items():
            setattr(book, field, value)
        return self._books.update(book)

    def delete_book(self, book_id: int) -> None:
        book = self.get_book(book_id)
        if book.borrowed_copies > 0:
            raise ConflictError(
                f"Cannot delete '{book.title}': {book.borrowed_copies} copies are still on loan."
            )
        self._books.delete(book_id)

    def _ensure_isbn_unique(self, isbn: str) -> None:
        if self._books.get_by_isbn(isbn) is not None:
            raise ConflictError(f"A book with ISBN {isbn} already exists.")
