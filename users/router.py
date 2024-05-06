from datetime import timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from core import auth
from db import get_db

from . import schema, services

KST = timezone(timedelta(hours=9))
router = APIRouter()


@router.post("/edit")
def edit_user_info(req: Request, user: schema.UserEdit, db: Session = Depends(get_db)):
    # 토큰이 잘못되었을 경우(invalid 또는 expired), 현재 미들웨러를 통해 이미 authrized된 상태이므로
    if not req.user:
        raise HTTPException(status_code=403, detail="로그인이 필요합니다.")

    curret_password = user.password.get_secret_value()

    current_user_id = int(req.user)
    db_user = auth.get_current_user_by_id(current_user_id, db)

    if not db_user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    if not services.verify_password(curret_password, db_user.password):
        raise HTTPException(status_code=403, detail="기존 비밀번호가 맞지 않습니다.")

    user.user_id = current_user_id
    services.update_user_info(db, user)
    return {"message": "사용자 정보가 성공적으로 업데이트되었습니다."}


# 비밀번호 누르고 탈퇴하기 버튼 누르는 순간 벌어지는 이벤트임
@router.post("/delete")
def user_delete(req: Request, user: schema.UserDelete, db: Session = Depends(get_db)):
    # 현재 미들웨러를 통해 이미 authrized된 상태이므로
    if not req.user:
        raise HTTPException(status_code=403, detail="로그인이 필요합니다.")

    password = user.password.get_secret_value()
    current_user_id = int(req.user)

    # 사용자의 비밀번호를 데이터베이스에서 가져오기
    user = auth.get_current_user_by_id(current_user_id, db)
    if not user:
        raise HTTPException(status_code=403, detail="사용자를 찾을 수 없습니다.")

    if not services.verify_password(password, user.password):
        raise HTTPException(status_code=403, detail="비밀번호 확인이 필요합니다.")

    services.delete_user(db, current_user_id)
    return {"detail": "회원 탈퇴가 완료되었습니다."}


@router.post("/join")
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    if services.find_user_with_email(db, user.email):
        raise HTTPException(status_code=403, detail="중복된 이메일 존재")
    return services.create_user(db, user)


@router.post("/login")
def login_user(user: schema.UserLogin, db: Session = Depends(get_db)):
    user_info = services.find_user_with_email(db, user.email)

    if not user_info:
        raise HTTPException(status_code=403, detail="사용자를 찾을 수 없습니다.")

    if not services.verify_password(user.password.get_secret_value(), user_info.password):
        raise HTTPException(status_code=403, detail="비밀번호 확인이 필요합니다.")

    # TODO servies.generate_login_token이 여기 적절하있는게 맞나?
    return services.generate_login_token(db, user_info)
