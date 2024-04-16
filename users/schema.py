from pydantic import BaseModel, EmailStr, SecretStr

class UserBase(BaseModel):
	username: str
	email: str 

# 유저가 회원가입할떄는  username, email, password만 잇으면된다 
class UserCreate(UserBase):
    password: str