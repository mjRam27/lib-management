"""A tiny in-memory 'database' with tables, auto-increment ids and a lock."""

from collections import defaultdict
from collections.abc import Iterator
from contextlib import contextmanager
from threading import RLock
from typing import Any


class InMemoryDatabase:
    """Process-local storage that mimics a relational database.

    Each table is a dict of `{id: entity}`. Data is lost when the process stops.
    """

    def __init__(self) -> None:
        self._tables: dict[str, dict[int, Any]] = defaultdict(dict)
        self._sequences: dict[str, int] = defaultdict(int)
        self._lock = RLock()

    def table(self, name: str) -> dict[int, Any]:
        return self._tables[name]

    def next_id(self, table_name: str) -> int:
        with self._lock:
            self._sequences[table_name] += 1
            return self._sequences[table_name]

    @contextmanager
    def transaction(self) -> Iterator[None]:
        """Serialize a group of operations (FastAPI runs sync endpoints in threads).

        With a real database this becomes a DB transaction / session.begin().
        """
        with self._lock:
            yield

    def reset(self) -> None:
        with self._lock:
            self._tables.clear()
            self._sequences.clear()
