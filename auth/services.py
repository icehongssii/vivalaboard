from core import auth
from . import model
from datetime import datetime, timedelta
import pytz
from config import get_settings

settings = get_settings()

KST = pytz.timezone(settings.TIMEZONE)


# 리프레시 토큰이 들어온다
def refresh_refresh_toke(t, db):
    payload = auth.get_token_payload(t.refresh_token)
    if not payload:
        return None
    # 요청 토큰이 만료되지 않았고
    user_id = payload.get("sub")
    # user_id가 존재하고 요청토큰과 디디 발급 토큰이 같으므로
    res = (
        db.query(model.RefreshToken)
        .filter(model.RefreshToken.user_id == user_id, model.RefreshToken.token == t.refresh_token)
        .first()
    )
    # access token 발급
    if res:
        auth.generate_tokens(user_id, datetime.now(KST) + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINS))
