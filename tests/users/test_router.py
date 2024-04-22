import pytest
from users.model import User


"""로그인"""
@pytest.mark.parametrize("email,password,expected_status,expected_detail", [
    ("nonexistent@example.com", "anyPassword", 403, "이메일 정보가 없어요"),
    ("valid@example.com", "wrongPassword", 403, "비밀번호가 틀렸어요")
])
def test_login_user_failure(test_client, monkeypatch, email, password, expected_status, expected_detail):
    # 이메일이 들어오면 None 리턴되면 이메일정보가 없다고 return됨
    monkeypatch.setattr('users.services.find_user_with_email', lambda db, email: None if email == "nonexistent@example.com" else User(email="valid@example.com", password="hashedPassword"))
    # password, hashedpwd가 들어오지만 항상 False를 리턴하는 케이스 따라서 항상 False가 리턴된다
    monkeypatch.setattr('users.services.verify_password', lambda password, hashed: False)


    response = test_client.post("/users/login", json={"email": email, "password": password})
    assert response.status_code == expected_status
    assert response.json().get("detail") == expected_detail


