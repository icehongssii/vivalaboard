from fastapi import APIRouter, Depends, Request, HTTPException
from . import services, schema
from typing import List
from sqlalchemy.orm import Session
from db import get_db
router = APIRouter()


@router.get("/delete")
def delete_post(req: Request, post_id: int, db: Session = Depends(get_db)):
    post_user_id = services.get_writer_id(db, post_id).user_id
    if not req.user:
        raise HTTPException(status_code=403, detail="로그인하고오세요!")
    user_id = int(req.user)
    if user_id != post_user_id:
        raise HTTPException(status_code=403, detail="작성자만 삭제 할 수 있어요")
    return {"result": "success", "deleted_post_id": post_id}


@router.get("/", response_model=List[schema.PostResponse])
def get_post_list(pagenation=Depends(schema.Pagination), db: Session = Depends(get_db)):
    res = services.get_posts(db, pagenation)
    return [schema.PostResponse(user_id=result.user_id, title=result.title,
                                post_id=result.post_id, views=result.views,
                                username=result.username)
            for result in res]


@router.get("/view")
def get_one_post(post_id: int=1, db: Session=Depends(get_db)):
    return services.get_one_post(db, post_id)


@router.post("/edit")
def edit_post(req: Request, post: schema.PostEditReq, db: Session=Depends(get_db)):
    # 실제로 클라이언트에서 요청을 보낼땐
    # post.user_id가 바뀔수가 없다
    writer = services.get_writer_id(db, post.post_id).user_id
    post.user_id = writer
    user_id = int(req.user)
    if not user_id:
        raise HTTPException(status_code=403, detail="로그인하고오세요!")
    if user_id != post.user_id:
        raise HTTPException(status_code=403, detail="작성자만 수정할 수 있어요")
    return services.edit_post(db, post)


@router.post("/write")
def write_post(req: Request, post: schema.PostWrite, db: Session=Depends(get_db)):
    user_id = req.user
    if not user_id:
        raise HTTPException(status_code=403, detail="로그인하고오세요!")
    post.user_id = user_id
    return services.create_post(db, post)
