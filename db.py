from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
#import backend.config as config

# DATABASE_USERNAME = config.DATABASE_USERNAME
# DATABASE_PASSWORD = config.DATABASE_PASSWORD
# DATABASE_HOST = config.DATABASE_HOST
# DATABASE_NAME = config.DATABASE_NAME

DATABASE_USERNAME = "root"
DATABASE_PASSWORD = "rootpassword"
DATABASE_HOST = "localhost"
DATABASE_NAME = "mydb"

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, 
                       )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
metadata = MetaData()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()