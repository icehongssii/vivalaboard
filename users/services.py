from sqlalchemy.orm import Session
from . import model, schema


def create_user(db: Session, user:schema.UserCreate) -> model.User:
    db_user = model.User(email=user.email, username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user) # refresh your instance (so that it contains any new data from the database, like the generated ID).
    return db_user

def find_user_with_email(db: Session, email:str) -> int:
        return db.query(model.User).filter(model.User.email == email).first()