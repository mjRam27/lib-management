from tests.conftest import API

NEW_MEMBER = {"name": "Ravi Kumar", "email": "ravi.kumar@example.com"}


def test_register_member(client):
    response = client.post(f"{API}/members", json=NEW_MEMBER)
    assert response.status_code == 201
    assert response.json()["membership_type"] == "standard"


def test_duplicate_email_rejected(client):
    response = client.post(f"{API}/members", json={**NEW_MEMBER, "email": "ASHA.RAO@example.com"})
    assert response.status_code == 409


def test_invalid_email_rejected(client):
    assert client.post(f"{API}/members", json={**NEW_MEMBER, "email": "not-an-email"}).status_code == 422


def test_deactivate_member(client):
    response = client.patch(f"{API}/members/1", json={"is_active": False})
    assert response.json()["is_active"] is False
    assert len(client.get(f"{API}/members", params={"is_active": True}).json()) == 1


def test_cannot_delete_member_with_active_loan(client):
    client.post(f"{API}/loans", json={"book_id": 1, "member_id": 1})
    assert client.delete(f"{API}/members/1").status_code == 409
