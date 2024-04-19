from sqlalchemy.orm import Session
from sqlalchemy import update
from . import model, schema
from auth import model as authModel
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from core import auth

KST = timezone(timedelta(hours=9))
now = datetime.now(KST)
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user:schema.UserCreate) -> model.User:
    hashed_pwd = return_hashed_password(user.password.get_secret_value())
    db_user = model.User(email=user.email, username=user.username, password=hashed_pwd)
    db.add(db_user)
    db.commit()
    db.refresh(db_user) # refresh your instance (so that it contains any new data from the database, like the generated ID).
    return db_user

def update_user_info(db: Session, user:schema.UserEdit):
    qry =update(model.User).where(model.User.user_id == user.user_id)\
        .values(username=user.username,
                password=user.password.get_secret_value()
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
    #  로그인을 위한 토큰발행 그리고 디비 업뎃
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
    
    return {"rt":rt, "at":at}