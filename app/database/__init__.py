"""Data storage layer. Currently an in-memory store; swap for a real DB later."""

from app.database.connection import get_db
from app.database.in_memory import InMemoryDatabase

__all__ = ["InMemoryDatabase", "get_db"]
