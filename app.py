from fastapi import FastAPI
from starlette.middleware.authentication import AuthenticationMiddleware

from auth.router import router as auth_router
from core import auth
from posts.router import router as posts_router
from users.router import router as user_router

app = FastAPI()

app.add_middleware(AuthenticationMiddleware, backend=auth.TokenAuthBackend())
app.include_router(user_router, prefix="/users")
app.include_router(auth_router, prefix="/auth")
app.include_router(posts_router, prefix="/posts")
