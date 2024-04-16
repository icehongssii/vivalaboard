from sqlalchemy.orm import Session
from .model import User


def create_user_logic(db: Session) -> User:
    print("create_user_logic!!")
    return "create_user_logic"