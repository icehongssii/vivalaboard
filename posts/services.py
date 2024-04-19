
from db import get_db
from fastapi import Depends
from . import model, schema
from users import model as user_model
from sqlalchemy import desc, asc

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
    
