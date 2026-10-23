"""Book request/response schemas."""

from datetime import date, datetime
from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, Field


def normalize_isbn(value: str) -> str:
    """Strip hyphens/spaces and validate ISBN-10 or ISBN-13 shape."""
    cleaned = value.replace("-", "").replace(" ", "").upper()
    is_isbn10 = len(cleaned) == 10 and cleaned[:9].isdigit() and (cleaned[9].isdigit() or cleaned[9] == "X")
    is_isbn13 = len(cleaned) == 13 and cleaned.isdigit()
    if not (is_isbn10 or is_isbn13):
        raise ValueError("ISBN must have 10 or 13 digits (hyphens allowed).")
    return cleaned


def validate_published_year(value: int) -> int:
    current_year = date.today().year
    if not 1000 <= value <= current_year:
        raise ValueError(f"published_year must be between 1000 and {current_year}.")
    return value


Title = Annotated[str, Field(min_length=1, max_length=200)]
Author = Annotated[str, Field(min_length=1, max_length=120)]
Genre = Annotated[str, Field(max_length=50)]
Copies = Annotated[int, Field(ge=1, le=1000)]
ISBN = Annotated[str, AfterValidator(normalize_isbn)]
PublishedYear = Annotated[int, AfterValidator(validate_published_year)]


class BookCreate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra={
            "example": {
                "title": "Fluent Python",
                "author": "Luciano Ramalho",
                "isbn": "978-1492056355",
                "total_copies": 3,
                "published_year": 2022,
                "genre": "Programming",
            }
        },
    )

    title: Title
    author: Author
    isbn: ISBN
    total_copies: Copies = 1
    published_year: PublishedYear | None = None
    genre: Genre | None = None


class BookUpdate(BaseModel):
    """Partial update: only fields that are sent are changed."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra={"example": {"total_copies": 5, "genre": "Computer Science"}},
    )

    title: Title | None = None
    author: Author | None = None
    isbn: ISBN | None = None
    total_copies: Copies | None = None
    published_year: PublishedYear | None = None
    genre: Genre | None = None


class BookRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    author: str
    isbn: str
    total_copies: int
    available_copies: int
    is_available: bool
    published_year: int | None
    genre: str | None
    created_at: datetime
    updated_at: datetime
