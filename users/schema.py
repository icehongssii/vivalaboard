from pydantic import BaseModel, EmailStr, SecretStr, field_validator


# Password를 사용한 이유는 로깅할 대 **로 찍히게 할려고
# 근데 Password에서 밸리데이션 체크를 할려고하는데 안된다
# 왜냐면 password = value.get_secret_value()  # SecretStr의 값을 얻기위해선 이런 작업을 필요로하기때문
# 기본적으로  SecretStr은 Iteraable이 아니기 때문
"""
class UserCreate(UserBase):
    password: SecretStr Field(min_length=8) 이거넣나 안넣나 똑같음 Field
    @field_validator('password')
    @classmethod
    def pwd_must_contains_numeric(cls, pwd: str) -> str:
        if not any(i.isdigit() for i in pwd):
            raise ValueError('must contains at least 1 digit')
        return pwd    
TypeError: 'SecretStr' object is not iterable
"""


class UserBase(BaseModel):
	email: EmailStr 

# 유저가 회원가입할떄는  username, email, password만 잇으면된다 
class UserCreate(UserBase):
    username: str
    password: SecretStr
    # 아래의 field_validor대신에 regular expression을 쓰는 것도 방법이다
    # regex=r'(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*])'
    
    @field_validator('password')
    def pwd_must_contains_alphabet(cls, pwd: SecretStr):
        secret_value = pwd.get_secret_value()  # SecretStr의 실제 값을 얻어옴
        if not any(char.isupper() for char in secret_value):
            raise ValueError('Password must contain at least 1 upper case letter')
        if not any(char.islower() for char in secret_value):
            raise ValueError('Password must contain at least 1 lower case letter')
        return pwd
    
    @field_validator('password')
    def pwd_len_must_over_8(cls,pwd: SecretStr):
        secret_value = pwd.get_secret_value()  # SecretStr의 실제 값을 얻어옴
        if len(secret_value) < 8:
            raise ValueError('must contains at least 1 digit')
        return pwd

    @field_validator('password')
    def pwd_must_contains_special_char(cls, pwd: SecretStr):
        secret_value = pwd.get_secret_value()  # SecretStr의 실제 값을 얻어옴
        if not any(char in "#?!@$%^&*-" for char in secret_value):
            raise ValueError('must contains at least 1 special char')
        return pwd

    @field_validator('password')
    @classmethod
    def pwd_must_contains_numeric(cls, pwd: str) -> str:
        secret_value = pwd.get_secret_value()  # SecretStr의 실제 값을 얻어옴
        if not any(char.isdigit() for char in secret_value):
            raise ValueError('must contains at least 1 digit')
        return pwd    
