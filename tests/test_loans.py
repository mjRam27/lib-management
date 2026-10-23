from datetime import timedelta

from app.database import get_db
from app.main import app
from app.models import utc_now
from tests.conftest import API


def borrow(client, book_id=1, member_id=1, **extra):
    return client.post(f"{API}/loans", json={"book_id": book_id, "member_id": member_id, **extra})


def test_borrow_and_return(client):
    response = borrow(client)
    assert response.status_code == 201
    loan = response.json()
    assert loan["status"] == "active"
    assert client.get(f"{API}/books/1").json()["available_copies"] == 2

    returned = client.post(f"{API}/loans/{loan['id']}/return").json()
    assert returned["status"] == "returned"
    assert returned["fine_amount"] == 0
    assert client.get(f"{API}/books/1").json()["available_copies"] == 3


def test_cannot_return_twice(client):
    loan_id = borrow(client).json()["id"]
    client.post(f"{API}/loans/{loan_id}/return")
    assert client.post(f"{API}/loans/{loan_id}/return").status_code == 409


def test_unavailable_book(client):
    borrow(client, book_id=5, member_id=1)  # Dune has a single copy
    assert borrow(client, book_id=5, member_id=2).status_code == 409


def test_same_book_twice_rejected(client):
    borrow(client)
    assert borrow(client).status_code == 409


def test_standard_member_loan_limit(client):
    for book_id in (1, 2, 3):
        assert borrow(client, book_id=book_id).status_code == 201
    response = borrow(client, book_id=4)
    assert response.status_code == 400
    assert "limit" in response.json()["detail"]


def test_inactive_member_cannot_borrow(client):
    client.patch(f"{API}/members/1", json={"is_active": False})
    assert borrow(client).status_code == 400


def test_unknown_book_or_member(client):
    assert borrow(client, book_id=999).status_code == 404
    assert borrow(client, member_id=999).status_code == 404


def test_renew_loan(client):
    loan = borrow(client).json()
    renewed = client.post(f"{API}/loans/{loan['id']}/renew", json={"extra_days": 7}).json()
    assert renewed["renewals"] == 1
    assert renewed["due_date"] > loan["due_date"]


def test_overdue_loan_fine(client):
    loan_id = borrow(client).json()["id"]
    # Push the due date 3 days into the past directly in the store.
    db = app.dependency_overrides[get_db]()
    db.table("loans")[loan_id].due_date = utc_now() - timedelta(days=3, hours=1)

    assert [loan["id"] for loan in client.get(f"{API}/loans/overdue").json()] == [loan_id]
    assert client.post(f"{API}/loans/{loan_id}/renew").status_code == 400

    returned = client.post(f"{API}/loans/{loan_id}/return").json()
    assert returned["fine_amount"] == 3.0
