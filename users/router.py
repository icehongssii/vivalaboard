from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .services import create_user_logic
from . import schema
from db import get_db

router = APIRouter()

# /users/join
@router.post("/join")
def create_user(user: schema.UserCreate, db:Session = Depends(get_db)):
    return create_user_logic(db, user)