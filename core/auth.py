from datetime import datetime

import pytz
from fastapi import Depends, Request
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy.orm import Session
from starlette.authentication import AuthenticationBackend
from starlette.middleware.authentication import AuthCredentials

from config import get_settings
from db import get_db

settings = get_settings()


class TokenAuthBackend(AuthenticationBackend):
    async def authenticate(self, request: Request):
        if "Authorization" not in request.headers:
            # None을 두개로 설정하지 않으면 starlette미들웨어에서
            # <starlette.authentication.UnauthenticatedUser>를 return하게되므로
            # 명시적으로 None작성
            return None, None

        auth = request.headers["Authorization"]
        token_type, _, token = auth.partition(" ")

        payload = get_token_payload(token)
        if not payload:
            return None, None

        user_id = payload.get("sub")  # 토큰이 만료되지 않았다
        return AuthCredentials(["authenticated"]), user_id


def get_token_payload(token):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except ExpiredSignatureError:
        return None
    except JWTError:
        return None
    return payload


def get_current_user_by_id(user_id, db: Session = Depends(get_db)):
    from users.model import User

    if not db:
        db = get_db()
    user = db.query(User).filter(User.user_id == user_id).first()
    return user


# create token
def generate_tokens(user_id, expire_time):
    payload = {
        "sub": str(user_id),
        "iat": datetime.now(pytz.timezone(settings.TIMEZONE)),
        "exp": expire_time,
        "iss": "vivalaboard",
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
