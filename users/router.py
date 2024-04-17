from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import schema, services
from db import get_db

router = APIRouter()

# /users/join
@router.post("/join")
def create_user(user: schema.UserCreate, db:Session = Depends(get_db)):
    if services.find_user_with_email(db, user.email):
        raise HTTPException(status_code=400, detail = "같은 이메일 존재")     
    return services.create_user(db,user)