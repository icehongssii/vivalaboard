from fastapi import APIRouter, Depends
from . import services, schema
from typing import Annotated
from sqlalchemy.orm import Session
from db import get_db
router = APIRouter()

# 기본페이지
@router.get("/")
def get_post_list(pagenation=Depends(schema.Pagination), db:Session = Depends(get_db)):
    return services.get_posts(db,pagenation)

@router.get("/view")
# /posts/view?post_id=11
def get_one_post(post_id:int=1, db:Session=Depends(get_db)):
    return services.get_one_post(db, post_id)