import pytest

from users.model import User

"""탈퇴 실패"""


@pytest.mark.parametrize(
    "token, user_id_in_path, password, expected_status, expected_detail",
    [
        ("valid", 1, "incorrect_password", 403, "비밀번호 확인이 필요합니다."),  # 비밀번호가 잘못 입력된 경우
        ("expired", 1, "correct_password", 403, "로그인이 필요합니다."),  # 토큰이 만료된 경우
        ("invalid", 1, "correct_password", 403, "로그인이 필요합니다."),  # 잘못된 토큰인 경우
    ],
)
def test_user_delete_failure(
    test_client, monkeypatch, token, user_id_in_path, password, expected_status, expected_detail
):
    # 가짜 사용자 객체
    fake_user = type("User", (object,), {"user_id": user_id_in_path, "password": "hashed_password"})

    # 비밀번호 재검증
    def fake_verify_password(provided_password, actual_password):
        return provided_password == "correct_password" and actual_password == "hashed_password"

    # 토큰 검증 함수를 가짜로 교체
    monkeypatch.setattr(
        "core.auth.get_token_payload", lambda token: None if token in ["expired", "invalid"] else {"sub": 1}
    )
    # 사용자 검색 함수를 가짜로 교체
    monkeypatch.setattr("core.auth.get_current_user_by_id", lambda user_id, db: fake_user if user_id == 1 else None)
    monkeypatch.setattr("users.services.verify_password", fake_verify_password)

    response = test_client.post(
        "/users/delete",
        headers={"Authorization": f"Bearer {token}"},
        json={"user_id": user_id_in_path, "password": password},
    )

    assert response.status_code == expected_status
    assert response.json().get("detail") == expected_detail


"""로그인 실패"""


@pytest.mark.parametrize(
    "email,password,expected_status,expected_detail",
    [
        ("nonexistent@example.com", "anyPassword", 403, "사용자를 찾을 수 없습니다."),
        ("valid@example.com", "wrongPassword", 403, "비밀번호 확인이 필요합니다."),
    ],
)
def test_login_user_failure(test_client, monkeypatch, email, password, expected_status, expected_detail):
    # 이메일이 들어오면 None 리턴되면 이메일정보가 없다고 return됨
    monkeypatch.setattr(
        "users.services.find_user_with_email",
        lambda db, email: (
            None if email == "nonexistent@example.com" else User(email="valid@example.com", password="hashedPassword")
        ),
    )
    # password, hashedpwd가 들어오지만 항상 False를 리턴하는 케이스 따라서 항상 False가 리턴된다
    monkeypatch.setattr("users.services.verify_password", lambda password, hashed: False)

    response = test_client.post("/users/login", json={"email": email, "password": password})
    assert response.status_code == expected_status
    assert response.json().get("detail") == expected_detail


"""회원가입 실패"""


# TODO @icehongssii expected_detail 추가하기
#   assert response.json().get("detail") == expected_detail
@pytest.mark.parametrize(
    "username, email,password, expected_status, expected_detail",
    [
        ("anyusername", "duplicated@example.com", "anyPassword", 422, "중복된 이메일"),
        ("anyusername", "valid@example.com", "WRONGPASSWORD!", 422, "비밀번호 소문자가 1개라도 포함되어야함"),
        ("anyusername", "valid@example.com", "wrongp", 422, "비밀번호 8자이상"),
        ("anyusername", "valid@example.com", "wrongPassword#", 422, "숫자 한개 이상 포함"),
    ],
)
def test_register_user_failure(test_client, monkeypatch, username, email, password, expected_status, expected_detail):
    # 중복된 이메일이 들어오면 None 리턴되면 이메일정보가 없다고 return됨
    monkeypatch.setattr(
        "users.services.find_user_with_email", lambda db, email: False if email == "duplicated@example.com" else True
    )
    response = test_client.post("/users/join", json={"username": username, "email": email, "password": password})
    assert response.status_code == expected_status
