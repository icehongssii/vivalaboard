from sqlalchemy.orm import Session
from . import model, schema


def create_user_logic(db: Session, user:schema.UserCreate) -> model.User:
    m = model.User(email=user.email, username=user.username, password=user.password)
    db.add(m)
    db.commit()
    db.refresh(m) # refresh your instance (so that it contains any new data from the database, like the generated ID).
    return m