
from core import auth
from datetime import datetime, timedelta, timezone
from core import auth
from . import model

KST = timezone(timedelta(hours=9))
now = datetime.now(KST)

# 리프레시 토큰이 들어온다
def refresh_refresh_toke(t,db):
    payload = auth.get_token_payload(t.refresh_token)
    if not payload:
        return None
    user_id = payload.get("sub")     
    res = db.query(model.RefreshToken).filter(model.RefreshToken.user_id == user_id, model.RefreshToken.token == t.refresh_token).first()
    if res:
        auth.generate_tokens(user_id, "exp")