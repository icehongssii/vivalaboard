from starlette.middleware.authentication import (
    AuthenticationMiddleware,AuthenticationError,AuthCredentials,UnauthenticatedUser)
from fastapi import Request, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt,JWTError,ExpiredSignatureError
from auth import model 
from db import get_db
from datetime import datetime, timedelta, timezone
KST = timezone(timedelta(hours=9))
now = datetime.now(KST)

ACCESS_TOKEN_EXPIRED_MINUTES=1
REFRESH_TOKEN_EXPIRED_MINUTES=60*24
ALGORITHM="HS256"
SECRET = "5d7253c2dc63339f8718bffdcd38302ed9e0bc8a8d4fc4bdca2d0be7f2de84ee1ad71189b36bc2b850c879983566def29453cb46417915831df074b89d44193f"
from starlette.authentication import AuthenticationBackend


class TokenAuthBackend(AuthenticationBackend):
    async def authenticate(self, request: Request):
        if not "Authorization" in request.headers:
            # None을 두개로 설정하지 않으면 starlette미들웨어에서
            #<starlette.authentication.UnauthenticatedUser>를 return하게되므로
            #명시적으로 None작성
            return None, None
        
        auth = request.headers["Authorization"]
        token_type, _, token = auth.partition(' ')
 
        payload = get_token_payload(token)
        # at가 만료되었거나 잘못된 형식일 경우
        if not payload:
            return None, None
        
        user_id = payload.get("sub") # 토큰이 만료되지 않았다        
        return AuthCredentials(["authenticated"]), user_id
        
        
def get_token_payload(token):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        print("만료된토큰")
        return None
    except JWTError:
        print("이상한토큰")
        return None
    return payload    

def get_current_user(user_id,db=None):
    if not db:
        db = get_db()
    user = db.query(model.User).filter(model.User.user_id == user_id).first()
    return user
    

# create token
def generate_tokens(user_id, exp):    
    payload = {
        "sub": str(user_id),
        "iat": datetime.now(),
        "exp": exp,
        "iss": "vivalaboard",
    }
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)



