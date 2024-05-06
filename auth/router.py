from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import get_db

from . import schema, services

router = APIRouter()


# access token재발급 위해 refresh 토큰받기
@router.post("/get_access_token")
def regenerate_access_token(refresh_token: schema.RefreshToken, db: Session = Depends(get_db)):
    return services.refresh_refresh_toke(refresh_token, db)
