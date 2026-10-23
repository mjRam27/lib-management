"""Database access point used by the dependency-injection layer.

When adding a real database, replace this with an engine/session factory
(e.g. a SQLAlchemy `SessionLocal`) and yield a session from `get_db`.
"""

from app.database.in_memory import InMemoryDatabase

_database = InMemoryDatabase()


def get_db() -> InMemoryDatabase:
    return _database
