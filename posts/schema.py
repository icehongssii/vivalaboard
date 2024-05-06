from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional


class SortPosts(Enum):
    ASC = "asc"
    DESC = "desc"


class Pagination(BaseModel):
    page: int = 1
    perPage: int = 5
    sort_column: str = "created_at"
    order_direction: SortPosts = SortPosts.DESC


class PostWrite(BaseModel):
    user_id: int = None
    title: str = Field(max_length=100, min_length=1)
    content: str = Field(min_length=1)


class PostEditReq(PostWrite):
    post_id: int


class PostView(BaseModel):
    post_id: int
    username: str = None
    user_id: int
    title: str
    views: int


class PostResponse(BaseModel):
    post_id: int
    user_id: Optional[int]
    title: str
    views: int
    username: str
