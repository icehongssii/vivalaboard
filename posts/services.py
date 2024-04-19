
from db import get_db
from fastapi import Depends
from . import model, schema
from users import model as user_model
from sqlalchemy import desc, asc,update
from datetime import datetime, timedelta, timezone
KST = timezone(timedelta(hours=9))

def edit_post(db,post):    
    update_stmt = update(model.Post).where(model.Post.post_id == post.post_id)\
                      .values(content=post.content, title=post.title, updated_at=datetime.now(KST))
    db.execute(update_stmt)
    db.commit()
    return post    

def create_post(db, post):
    postData = model.Post(
        user_id = post.user_id, 
        title = post.title,
        content = post.content,
        created_at = datetime.now(KST),
        updated_at = datetime.now(KST)
    )
    db.add(postData)
    db.commit()
    db.refresh(postData)
    return postData
    

def get_posts(db, pagenation):
    # 정렬 방향 설정
    order_direction = desc if pagenation.order_direction == schema.SortPosts.DESC else asc
    # created_at 또는 views로 정렬
    sort_column = model.Post.created_at if pagenation.sort_column == 'created_at' else model.Post.views
    
    return db.query(model.Post)\
        .join(user_model.User, model.Post.user_id == user_model.User.user_id)\
        .order_by(order_direction(sort_column))\
        .limit(pagenation.perPage)\
        .offset((pagenation.page - 1) * pagenation.perPage)\
        .all()    
    
def get_one_post(db, pid):
    post = db.query(model.Post).filter_by(post_id=pid).first()
    if post.created_at == post.updated_at:
        post.updated_at = ""
    return post