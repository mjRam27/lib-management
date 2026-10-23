"""Domain exceptions.

These are raised by models and services and know nothing about HTTP.
The API layer maps them to status codes (see app/api/error_handlers.py).
"""


class LibraryError(Exception):
    """Base class for all library domain errors."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class NotFoundError(LibraryError):
    """A requested resource does not exist."""


class ConflictError(LibraryError):
    """The request conflicts with the current state (duplicates, already returned, ...)."""


class BusinessRuleError(LibraryError):
    """The request violates a lending rule (loan limits, inactive member, ...)."""
