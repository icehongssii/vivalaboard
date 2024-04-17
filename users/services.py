from sqlalchemy.orm import Session
from . import model, schema
from passlib.context import CryptContext

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user:schema.UserCreate) -> model.User:
    hashed_pwd = return_hashed_password(user.password.get_secret_value())
    db_user = model.User(email=user.email, username=user.username, password=hashed_pwd)
    db.add(db_user)
    db.commit()
    db.refresh(db_user) # refresh your instance (so that it contains any new data from the database, like the generated ID).
    return db_user

def find_user_with_email(db: Session, email:str) -> int:
        return db.query(model.User).filter(model.User.email == email).first()
    
def return_hashed_password(password):
    return PWD_CONTEXT.hash(password)
