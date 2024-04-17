from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from . import schema, services
from db import get_db

router = APIRouter()

# /users/join
@router.post("/join")
def create_user(user: schema.UserCreate, db:Session = Depends(get_db)):
    return services.create_user(db, user)
