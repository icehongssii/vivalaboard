from pydantic import BaseModel, EmailStr,Field, SecretStr, field_validator
from datetime import datetime
from enum import Enum

class SortPosts(Enum):
    ASC = "asc"
    DESC = "desc"

class Pagination(BaseModel):
    page: int = 1
    perPage: int = 5
    sort_column: str = 'created_at'
    order_direction: SortPosts = SortPosts.DESC
    class Config:
        orm_mode = True

class Post(BaseModel):
    pass

class PostWrite(Post):
    user_id:int = None
    title: str=Field(max_length=100, min_length=1)
    content: str=Field( min_length=1)