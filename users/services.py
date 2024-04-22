from sqlalchemy.orm import Session
from sqlalchemy import update, delete
from . import model, schema
from auth import model as authModel
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from core import auth

KST = timezone(timedelta(hours=9))
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

def delete_user(db, user_id):
    qry = delete(model.User).where(model.User.user_id == user_id)
    db.execute(qry)
    db.commit()
    return user_id

def create_user(db: Session, user:schema.UserCreate) -> model.User:
    hashed_pwd = return_hashed_password(user.password.get_secret_value())
    db_user = model.User(email=user.email, username=user.username, password=hashed_pwd)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_info(db: Session, user:schema.UserEdit):
    password = user.password
    # 비밀번호를 바꾸고 싶다면 
    if user.new_password:
        password = return_hashed_password(user.new_password.get_secret_value()) 
    qry =update(model.User).where(model.User.user_id == user.user_id)\
        .values(username=user.username,
                password=password
                )
    db.execute(qry)
    db.commit()
    return user


def verify_password(password, hashed_password) -> bool:
    return PWD_CONTEXT.verify(password, hashed_password)
    
def find_user_with_email(db: Session, email:str) -> int:
        return db.query(model.User).filter(model.User.email == email).first()
    
def return_hashed_password(password):
    return PWD_CONTEXT.hash(password)

def generate_login_token(db: Session, user_info:schema.UserLogin):
    rt  = auth.generate_tokens(user_info.user_id, datetime.now(KST) + timedelta(minutes=10))    

    # 업서트
    token = db.query(authModel.RefreshToken).filter_by(user_id=user_info.user_id).first()
    if token:
        token.token = rt
        token.expires_at = datetime.now(KST) + timedelta(minutes=1440),
        token.created_at = datetime.now(KST)
    else:
        token = authModel.RefreshToken(
            user_id=user_info.user_id,
            token=rt,
            expires_at=datetime.now(KST) + timedelta(minutes=1440),
            created_at=datetime.now(KST)
        )
        db.add(token)
    db.commit()
    db.refresh(token)
        
    at  = auth.generate_tokens(user_info.user_id, datetime.now(KST) + timedelta(minutes=1440))
    
    return {"refresh_token":rt, "access_token":at}