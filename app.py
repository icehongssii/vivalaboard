from fastapi import FastAPI
from users.router import router as user_router
from auth.router import router as auth_router
from core import auth
from starlette.middleware.authentication import AuthenticationMiddleware
app = FastAPI()

app.add_middleware(AuthenticationMiddleware, backend=auth.TokenAuthBackend())
app.include_router(user_router, prefix="/users")
app.include_router(auth_router, prefix="/auth")

@app.get("/")
def root():
    return {"message": "Hello World"}