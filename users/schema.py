from pydantic import BaseModel, EmailStr, SecretStr, field_validator
from typing import Optional


class UserPassword(BaseModel):
    _password: Optional[SecretStr] = None
    # TODO @icehongssii 24022 아래 정규식 곧바로 사용시 에러발생
    #      error: look-around, including look-ahead and look-behind, is not supported
    # 아래의 field_validor대신에 regular expression을 쓰는 것도 방법이다
    # regex=r'(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*])'

    @staticmethod
    def pwd_must_contains(pwd: Optional[SecretStr] = None):
        if pwd is None:
            return None
        # SecretStr 타입 검사
        if isinstance(pwd, SecretStr):
            secret_value = pwd.get_secret_value()
        else:
            secret_value = pwd  # 이미 문자열로 되어있는 경우

        if not any(char.isupper() for char in secret_value):
            raise ValueError("Password must contain at least 1 upper case letter")
        if not any(char.islower() for char in secret_value):
            raise ValueError("Password must contain at least 1 lower case letter")
        if len(secret_value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(char in "#?!@$%^&*-" for char in secret_value):
            raise ValueError("Password must contain at least one special character")
        if not any(char.isdigit() for char in secret_value):
            raise ValueError("Password must contain at least one digit")
        return pwd

    @field_validator("_password", mode="before", check_fields=False)
    def password_validator(cls, pwd: Optional[SecretStr] = None):
        return cls.pwd_must_contains(pwd)


class UserCreate(UserPassword):
    email: EmailStr
    username: str = None
    password: SecretStr

    # Apply the same password validation to new_password
    @field_validator("password", mode="before")
    def password_validator(cls, pwd: Optional[SecretStr] = None):
        return cls.pwd_must_contains(pwd)


class UserLogin(BaseModel):
    email: EmailStr
    password: SecretStr


class UserDelete(BaseModel):
    password: SecretStr


class UserEdit(UserPassword):
    # 수정페이지로 들어갈땐 user_id가 필요없고(토큰에 있으니)
    # 수정 완료 버튼을 누를 땐 user_id가 필요하므로 option에 넣는다
    user_id: Optional[int] = None
    username: str = None
    password: SecretStr
    new_password: Optional[SecretStr] = None

    @field_validator("new_password", mode="before", check_fields=False)
    def new_password_validator(cls, pwd: Optional[SecretStr] = None):
        return cls.pwd_must_contains(pwd)


class UserView(BaseModel):
    user_id: int
