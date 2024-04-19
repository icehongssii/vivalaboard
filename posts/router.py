from fastapi import APIRouter, Depends
from . import services, schema
from typing import Annotated
from sqlalchemy.orm import Session
from db import get_db
router = APIRouter()

@router.get("/")
def get_post_list(pagenation=Depends(schema.Pagination), db:Session = Depends(get_db)):
    return services.get_posts(db,pagenation)