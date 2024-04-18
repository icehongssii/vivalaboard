from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from . import schema, services
from db import get_db

KST = timezone(timedelta(hours=9))
now = datetime.now(KST)
router = APIRouter()
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="token")




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
    
    return services.generate_login_token(db,user_info)