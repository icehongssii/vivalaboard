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

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}?charset=utf8mb4"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
#https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.connect_args                       
#Add Parameters to the URL Query string¶
#Simple string values, as well as some numeric values and boolean flags, may be often specified in the query string of the URL directly. A common example of this is DBAPIs that accept an argument encoding for character encodings, such as most MySQL DBAPIs:
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
metadata = MetaData()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()