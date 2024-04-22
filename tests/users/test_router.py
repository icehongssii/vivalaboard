import pytest
from users.model import User
from fastapi import Request
from starlette.status import HTTP_403_FORBIDDEN

"""회원 탈퇴"""
@pytest.mark.parametrize("token, user_id_in_path, expected_status, expected_detail", [
    ("expired", 1, 403, "로그인하고오세요!"),
    ("invalid", 1, 403, "로그인하고오세요!"),
    ("1", 2, 403, "본인만 회원탈퇴가능")
])
def test_user_delete_failure(test_client,monkeypatch, token, user_id_in_path, expected_status, expected_detail):
    def fake_get_token_payload(token):
        if token in ["expired", "invalid"]:
            return None  # 토큰이 만료되었거나 잘못되었을 때
        return {"sub": "1"}  # 유효한 토큰일 때, 사용자 ID '1'을 반환

    # Monkeypatch the token validation method
    monkeypatch.setattr('core.auth.get_token_payload', fake_get_token_payload)

    response = test_client.delete(f"/users/{user_id_in_path}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == expected_status
    assert response.json().get("detail") == expected_detail



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

"""회원가입"""
# TODO @icehongssii expected_detail 추가하기
#   assert response.json().get("detail") == expected_detail
@pytest.mark.parametrize("username,email,password,expected_status,expected_detail", [
    ("anyusername","duplicated@example.com", "anyPassword", 422, "중복된 이메일"),
    ("anyusername","valid@example.com", "WRONGPASSWORD!", 422, "비밀번호 소문자가 1개라도 포함되어야함"),
    ("anyusername","valid@example.com", "wrongp", 422, "비밀번호 8자이상"),
    ("anyusername","valid@example.com", "wrongPassword#", 422, "숫자 한개 이상 포함"),
])
def test_register_user_failure(test_client, monkeypatch,username, email, password, expected_status, expected_detail):
    # 중복된 이메일이 들어오면 None 리턴되면 이메일정보가 없다고 return됨
    monkeypatch.setattr('users.services.find_user_with_email', lambda db, email: False if email == "duplicated@example.com" else True)
    response = test_client.post("/users/join", json={"username":username,"email": email, "password": password})
    assert response.status_code == expected_status
    