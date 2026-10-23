"""Book catalogue endpoints."""

from typing import Annotated

from fastapi import APIRouter, Path, Query, status

from app.api.dependencies import BookServiceDep
from app.schemas.book import BookCreate, BookRead, BookUpdate
from app.schemas.common import ErrorResponse

router = APIRouter(prefix="/books", tags=["Books"])

BookId = Annotated[int, Path(ge=1, description="Book ID")]
NOT_FOUND = {404: {"model": ErrorResponse, "description": "Book not found"}}
CONFLICT = {409: {"model": ErrorResponse, "description": "Conflict with current state"}}


@router.post(
    "",
    response_model=BookRead,
    status_code=status.HTTP_201_CREATED,
    summary="Add a new book",
    responses=CONFLICT,
)
def create_book(payload: BookCreate, service: BookServiceDep):
    return service.create_book(payload)


@router.get("", response_model=list[BookRead], summary="List / search books")
def list_books(
    service: BookServiceDep,
    search: Annotated[str | None, Query(description="Matches title, author or ISBN")] = None,
    author: str | None = None,
    genre: str | None = None,
    available_only: bool = False,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    return service.list_books(search, author, genre, available_only, skip, limit)


@router.get("/{book_id}", response_model=BookRead, summary="Get a book", responses=NOT_FOUND)
def get_book(book_id: BookId, service: BookServiceDep):
    return service.get_book(book_id)


@router.patch(
    "/{book_id}",
    response_model=BookRead,
    summary="Update a book",
    responses={**NOT_FOUND, **CONFLICT},
)
def update_book(book_id: BookId, payload: BookUpdate, service: BookServiceDep):
    return service.update_book(book_id, payload)


@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a book",
    responses={**NOT_FOUND, **CONFLICT},
)
def delete_book(book_id: BookId, service: BookServiceDep) -> None:
    service.delete_book(book_id)
