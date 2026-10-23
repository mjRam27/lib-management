from tests.conftest import API

NEW_BOOK = {"title": "Fluent Python", "author": "Luciano Ramalho", "isbn": "978-1492056355", "total_copies": 2}


def test_list_seeded_books(client):
    response = client.get(f"{API}/books")
    assert response.status_code == 200
    assert len(response.json()) == 5


def test_create_book_normalizes_isbn(client):
    response = client.post(f"{API}/books", json=NEW_BOOK)
    assert response.status_code == 201
    body = response.json()
    assert body["isbn"] == "9781492056355"
    assert body["available_copies"] == 2


def test_duplicate_isbn_rejected(client):
    client.post(f"{API}/books", json=NEW_BOOK)
    assert client.post(f"{API}/books", json=NEW_BOOK).status_code == 409


def test_invalid_isbn_rejected(client):
    response = client.post(f"{API}/books", json={**NEW_BOOK, "isbn": "123"})
    assert response.status_code == 422


def test_search_books(client):
    response = client.get(f"{API}/books", params={"search": "orwell"})
    assert [book["title"] for book in response.json()] == ["1984"]


def test_update_and_delete_book(client):
    response = client.patch(f"{API}/books/1", json={"total_copies": 5})
    assert response.json()["available_copies"] == 5

    assert client.delete(f"{API}/books/1").status_code == 204
    assert client.get(f"{API}/books/1").status_code == 404
