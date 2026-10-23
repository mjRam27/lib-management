import pytest
from fastapi.testclient import TestClient

from app.database import InMemoryDatabase, get_db
from app.database.seed import seed_database
from app.main import app

API = "/api/v1"


@pytest.fixture
def client() -> TestClient:
    """A client backed by a fresh, seeded in-memory database for each test."""
    db = InMemoryDatabase()
    seed_database(db)
    app.dependency_overrides[get_db] = lambda: db
    yield TestClient(app)
    app.dependency_overrides.clear()
