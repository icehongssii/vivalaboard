from fastapi import APIRouter, Depends, Request, HTTPException
from . import services, schema
from typing import Annotated
from sqlalchemy.orm import Session
from db import get_db
router = APIRouter()
from starlette.authentication import requires

# 기본페이지
@router.get("/")
def get_post_list(pagenation=Depends(schema.Pagination), db:Session = Depends(get_db)):
    return services.get_posts(db,pagenation)

@router.get("/view")
# /posts/view?post_id=11
def get_one_post(post_id:int=1, db:Session=Depends(get_db)):
    return services.get_one_post(db, post_id)


@router.post("/write")
# /posts/view?post_id=11
def write_post(req:Request,post:schema.PostWrite, db:Session=Depends(get_db)):
    user_id = req.user
    if not user_id:     
        raise HTTPException(status_code=403, detail = "로그인하고오세요!")     
    post.user_id = user_id
    return services.create_post(db,post)