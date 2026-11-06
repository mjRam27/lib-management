from auth import AuthService

def test_hash_password():
    auth_service = AuthService()
    password = "secrete123"
    password_hash = auth_service.hash_password(password)

    assert password_hash != password


def test_verify_correct_password():
    auth_service = AuthService()
    password = "secrete123"
    password_hash = auth_service.hash_password(password)

    result = auth_service.verify_password(password, password_hash)

    assert result is True

def test_verify_wrong_password():
    auth_service = AuthService()
    correct_password = "secrete123"
    wrong_password = "wrongpassword"
    password_hash = auth_service.hash_password(correct_password)

    result = auth_service.verify_password(wrong_password, password_hash)

    assert result is False