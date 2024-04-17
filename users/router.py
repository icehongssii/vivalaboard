from fastapi import APIRouter, Depends, HTTPException
import json
from typing import Literal
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from . import schema, services
from db import get_db

router = APIRouter()
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="token")
REFRESH_TKN_EXP_MIN = 1440
ALGORITHM = "HS256"
SECRET_KEY = "5d7253c2dc63339f8718bffdcd38302ed9e0bc8a8d4fc4bdca2d0be7f2de84ee1ad71189b36bc2b850c879983566def29453cb46417915831df074b89d44193f"
ACCESS_TKN_EXP_MIN = 30

def create_token(data: dict, mode:Literal['access', 'refresh']):
    data['exp']  = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TKN_EXP_MIN)
    data['mode'] = mode
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


# /users/join
@router.post("/join")
def create_user(user: schema.UserCreate, db:Session = Depends(get_db)):
    if services.find_user_with_email(db, user.email):
        raise HTTPException(status_code=400, detail = "같은 이메일 존재")     
    return services.create_user(db,user)

# /users/join
@router.post("/login")
def login_user(user: schema.UserLogin, db:Session = Depends(get_db)):
    user_info = services.find_user_with_email(db, user.email)
    
    # 이메일이 잘못되었으면 빡구
    if not user_info:
        raise HTTPException(status_code=400, detail = "이메일 정보가 없어요")     
    
    # 이메일 맞아도 비밀번호가 잘못되었으면 빡구
    if not services.verify_password(user.password.get_secret_value(), user_info.password):
        raise HTTPException(status_code=400, detail = "비밀번호가 틀렸어요")
    
    # 이메일과 비밀번호가 잘 맞았다면 access token 발행
    access_token = create_token(data={"email":user_info.email}, mode='access')
    
    # 이메일과 비밀번호가 잘 맞았다면 refresh token 발행
    if not user_info.refresh_token:
        user_info.refresh_token = create_token(data={"email":user_info.email}, mode='refresh')
    refresh_token = user_info.refresh_token
    

    return (access_token, refresh_token)    