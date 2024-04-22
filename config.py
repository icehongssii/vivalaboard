import os
from functools import lru_cache
from pydantic_settings import BaseSettings
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import quote_plus

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):

    # App
    DEBUG: bool = bool(os.environ.get("DEBUG", 0))
    ENV: str = os.environ.get("ENV", 'dev')
    
    # TIMEZONE
    TIMEZONE: str = os.environ.get("TIMEZONE", 'Asia/Seoul')
    

    # DB
    MYSQL_HOST: str = os.environ.get("MYSQL_HOST", 'localhost')
    MYSQL_USR: str = os.environ.get("MYSQL_USR", 'root')
    MYSQL_PWD: str = os.environ.get("MYSQL_PWD", 'rootpassword')
    MYSQL_PORT: int = int(os.environ.get("MYSQL_PORT", 3306))
    MYSQL_DB: str = os.environ.get("MYSQL_DB", 'mydb')
    DB_URL: str = f"mysql+pymysql://{MYSQL_USR}:%s@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}" % quote_plus(MYSQL_PWD)

    # JWT
    JWT_SECRET: str = os.environ.get("JWT_SECRET", "5d7253c2dc63339f8718bffdcd38302ed9e0bc8a8d4fc4bdca2d0be7f2de84ee1ad71189b36bc2b850c879983566def29453cb46417915831df074b89d44193f")
    JWT_ALGORITHM: str = os.environ.get("ACCESS_TOKEN_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINS: int = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINS", 3))
    REFRESH_TOKEN_EXPIRE_MINS: int = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINS", 1440))

@lru_cache()
def get_settings() -> Settings:
    return Settings()