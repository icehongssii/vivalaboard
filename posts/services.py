from datetime import datetime

import pytz
from sqlalchemy import asc, delete, desc, func, update

from config import get_settings
from users import model as user_model

from . import model, schema

settings = get_settings()
KST = pytz.timezone(settings.TIMEZONE)


def delete_post(db, post_id):
    qry = delete(model.Post).where(model.Post.post_id == post_id)
    db.execute(qry)
    db.commit()
    return post_id


def get_writer_id(db, post_id):
    return db.query(model.Post).filter(model.Post.post_id == post_id).first()


def edit_post(db, post):
    update_stmt = (
        update(model.Post)
        .where(model.Post.post_id == post.post_id)
        .values(content=post.content, title=post.title, updated_at=datetime.now(KST))
    )
    db.execute(update_stmt)
    db.commit()
    return post


def create_post(db, post):
    postData = model.Post(
        user_id=post.user_id,
        title=post.title,
        content=post.content,
        created_at=datetime.now(KST),
        updated_at=datetime.now(KST),
    )
    db.add(postData)
    db.commit()
    db.refresh(postData)
    return postData


def get_posts(db, pagenation):
    # 정렬 방향 설정
    order_direction = desc if pagenation.order_direction == schema.SortPosts.DESC else asc
    # created_at 또는 views로 정렬
    sort_column = model.Post.created_at if pagenation.sort_column == "created_at" else model.Post.views
    res = (
        db.query(
            model.Post.post_id,
            model.Post.title,
            model.Post.views,
            user_model.User.user_id,
            func.coalesce(user_model.User.username, "탈퇴한 유저").label("username"),
        )
        .outerjoin(user_model.User, model.Post.user_id == user_model.User.user_id)
        .order_by(order_direction(sort_column))
        .limit(pagenation.perPage)
        .offset((pagenation.page - 1) * pagenation.perPage)
        .all()
    )
    return res


def get_one_post(db, pid):
    post = db.query(model.Post).filter_by(post_id=pid).first()
    # 수정한적이 없다면 빈 값
    if post.created_at == post.updated_at:
        post.updated_at = ""
    return post
