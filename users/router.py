from fastapi import APIRouter, Depends, HTTPException, Request
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from . import schema, services
from db import get_db
from core import auth
KST = timezone(timedelta(hours=9))

router = APIRouter()

"""회원 정보 수정"""
@router.post("/edit")
def edit_user_info(req: Request, user: schema.UserEdit, db: Session = Depends(get_db)):
    curret_password = user.password.get_secret_value()
    
    # 토큰이 잘못되었을 경우(invalid 또는 expired)
    if not req.user:
        raise HTTPException(status_code=403, detail="로그인이 필요합니다.")
    
    user_id = int(req.user)
    db_user = auth.get_current_user_by_id(user_id, db)
    
    if not db_user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    
    if not services.verify_password(curret_password, db_user.password):
        raise HTTPException(status_code=403, detail="기존 비밀번호가 맞지 않습니다.")

    user.user_id = user_id  
    services.update_user_info(db, user)
    return {"message": "사용자 정보가 성공적으로 업데이트되었습니다."}


"""회원탈퇴"""
@router.post("/delete")
def user_delete(req: Request, user:schema.UserDelete, db: Session = Depends(get_db)):
    user_id = user.user_id
    password = user.password.get_secret_value()
    
    if not req.user:
        raise HTTPException(status_code=403, detail="로그인이 필요합니다.")
    
    current_user = int(req.user)
    
    if current_user != user_id:
        raise HTTPException(status_code=403, detail="잘못된 접근입니다.")
    
    # 사용자의 비밀번호를 데이터베이스에서 가져오기
    user = auth.get_current_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=403, detail="사용자를 찾을 수 없습니다.")
    
    if not services.verify_password(password, user.password):
        raise HTTPException(status_code=403, detail="비밀번호가 틀려서 안됨")
    
    services.delete_user(db, user_id)
    return {"detail": "회원 탈퇴가 완료되었습니다."}

"""회원가입"""
@router.post("/join")
def create_user(user: schema.UserCreate, db:Session = Depends(get_db)):
    if services.find_user_with_email(db, user.email):
        raise HTTPException(status_code=403, detail = "중복된 이메일 존재")     
    return services.create_user(db,user)

"""로그인"""
@router.post("/login")
def login_user(user: schema.UserLogin, db:Session = Depends(get_db)):
    user_info = services.find_user_with_email(db, user.email)

    if not user_info:
        raise HTTPException(status_code=403, detail = "사용자를 찾을 수 없습니다.")
    
    if not services.verify_password(user.password.get_secret_value(), user_info.password):
        raise HTTPException(status_code=403, detail = "기존 비밀번호가 맞지 않습니다.")
    
    return services.generate_login_token(db,user_info)