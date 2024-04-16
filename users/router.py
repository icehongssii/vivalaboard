from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .services import create_user_logic
from . import schema
from db import get_db

router = APIRouter()

# /users/join
@router.post("/join")
def create_user(user_data: schema.UserCreate):
    return user_data
