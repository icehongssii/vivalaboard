from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from config import get_settings

settings = get_settings()

engine = create_engine(settings.DB_URL)
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