from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import schema, services
from db import get_db

router = APIRouter()
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="token")
REFRESH_TKN_EXP_MIN = 1440
ALGORITHM = "HS256"
SECRET_KEY = "5d7253c2dc63339f8718bffdcd38302ed9e0bc8a8d4fc4bdca2d0be7f2de84ee1ad71189b36bc2b850c879983566def29453cb46417915831df074b89d44193f"
ACCESS_TKN_EXP_MIN = 30

    
@router.post("/get_access_token")
def regenerate_access_token(refresh_token: schema.RefreshToken, db:Session = Depends(get_db)):
    return services.refresh_refresh_toke(refresh_token,db)
    



