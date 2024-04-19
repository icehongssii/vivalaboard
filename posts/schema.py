from pydantic import BaseModel, EmailStr, SecretStr, field_validator
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
