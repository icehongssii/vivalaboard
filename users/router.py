from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from . import schema, services
from db import get_db
from core import auth

KST = timezone(timedelta(hours=9))
now = datetime.now(KST)
router = APIRouter()
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="token")

# 정보수정 완료 버튼 눌렀을때
# 수정완료가 일어난다
# 정보
@router.post("/edit")
def edit_user_info(req:Request, user:schema.UserEdit, db:Session=Depends(get_db)):
    if not req.user:
        raise HTTPException(status_code=403, detail = "로그인하고오세요!")     
    user_id = int(req.user)
    user.user_id = user_id
    return services.update_user_info(db,user)



"""회원탈퇴"""
@router.post("/delete")
def user_delete(req: Request, user:schema.UserDelete, db: Session = Depends(get_db)):
    user_id = user.user_id
    password = user.password.get_secret_value()
    
    # 로그인 확인
    if not req.user:
        raise HTTPException(status_code=403, detail="로그인하고오세요!")
    
    current_user = int(req.user)
    
    # 요청된 사용자 ID가 현재 로그인한 사용자와 일치하는지 확인
    if current_user != user_id:
        raise HTTPException(status_code=403, detail="본인만 회원탈퇴가능")
    
    # 사용자의 비밀번호를 데이터베이스에서 가져오기
    user = auth.get_current_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=403, detail="사용자를 찾을 수 없습니다.")
    
    # 비밀번호 확인
    if not services.verify_password(password, user.password):
        raise HTTPException(status_code=403, detail="비밀번호가 틀려서 안됨")
    
    # 회원탈퇴 처리
    services.delete_user(db, user_id)
    return {"detail": f"{user_id}번호 이름{user.username}회원 탈퇴가 완료되었습니다."}

# /users/join
@router.post("/join")
def create_user(user: schema.UserCreate, db:Session = Depends(get_db)):
    if services.find_user_with_email(db, user.email):
        raise HTTPException(status_code=403, detail = "같은 이메일 존재")     
    return services.create_user(db,user)

# /users/join
@router.post("/login")
def login_user(user: schema.UserLogin, db:Session = Depends(get_db)):
    user_info = services.find_user_with_email(db, user.email)

    # 이메일이 잘못되었으면 빡구
    if not user_info:
        raise HTTPException(status_code=403, detail = "이메일 정보가 없어요")     
    
    # 이메일 맞아도 비밀번호가 잘못되었으면 빡구
    if not services.verify_password(user.password.get_secret_value(), user_info.password):
        raise HTTPException(status_code=403, detail = "비밀번호가 틀렸어요")
    
    return services.generate_login_token(db,user_info)