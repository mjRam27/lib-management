"""Generic repository interface and its in-memory implementation."""

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Generic, TypeVar

from app.database.in_memory import InMemoryDatabase
from app.models.base import BaseEntity

T = TypeVar("T", bound=BaseEntity)


class AbstractRepository(ABC, Generic[T]):
    """CRUD contract every storage backend must fulfil."""

    @abstractmethod
    def get(self, entity_id: int) -> T | None: ...

    @abstractmethod
    def list_all(self, skip: int = 0, limit: int = 100) -> list[T]: ...

    @abstractmethod
    def add(self, entity: T) -> T: ...

    @abstractmethod
    def update(self, entity: T) -> T: ...

    @abstractmethod
    def delete(self, entity_id: int) -> bool: ...

    @abstractmethod
    def count(self) -> int: ...


class InMemoryRepository(AbstractRepository[T]):
    """Stores entities in a named table of an InMemoryDatabase."""

    table_name: str

    def __init__(self, db: InMemoryDatabase) -> None:
        self._db = db

    @property
    def _table(self) -> dict[int, T]:
        return self._db.table(self.table_name)

    def get(self, entity_id: int) -> T | None:
        return self._table.get(entity_id)

    def list_all(self, skip: int = 0, limit: int = 100) -> list[T]:
        return self.find(lambda _: True, skip, limit)

    def find(self, predicate: Callable[[T], bool], skip: int = 0, limit: int = 100) -> list[T]:
        """Return entities matching `predicate`, ordered by id, paginated."""
        with self._db.transaction():
            matches = [entity for entity in self._table.values() if predicate(entity)]
        return matches[skip : skip + limit]

    def find_one(self, predicate: Callable[[T], bool]) -> T | None:
        with self._db.transaction():
            return next((entity for entity in self._table.values() if predicate(entity)), None)

    def add(self, entity: T) -> T:
        with self._db.transaction():
            entity.id = self._db.next_id(self.table_name)
            self._table[entity.id] = entity
        return entity

    def update(self, entity: T) -> T:
        with self._db.transaction():
            entity.touch()
            self._table[entity.id] = entity
        return entity

    def delete(self, entity_id: int) -> bool:
        with self._db.transaction():
            return self._table.pop(entity_id, None) is not None

    def count(self) -> int:
        return len(self._table)
