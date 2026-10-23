"""Translate domain exceptions into HTTP responses."""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.core.exceptions import BusinessRuleError, ConflictError, LibraryError, NotFoundError

_STATUS_CODES: dict[type[LibraryError], int] = {
    NotFoundError: status.HTTP_404_NOT_FOUND,
    ConflictError: status.HTTP_409_CONFLICT,
    BusinessRuleError: status.HTTP_400_BAD_REQUEST,
}


async def library_error_handler(request: Request, exc: LibraryError) -> JSONResponse:
    status_code = next(
        (code for exc_type, code in _STATUS_CODES.items() if isinstance(exc, exc_type)),
        status.HTTP_400_BAD_REQUEST,
    )
    return JSONResponse(status_code=status_code, content={"detail": exc.message})


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(LibraryError, library_error_handler)
