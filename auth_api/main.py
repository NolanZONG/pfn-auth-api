from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from starlette.responses import JSONResponse

from auth_api.database import Base, engine, SessionLocal
from auth_api.model import AuthData
from auth_api.repository import AuthDataRepository
from auth_api.validator import SignupRequest


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        session.add(AuthData(user_id="TaroYamada", password="PaSSwd4TY", nickname="Taro", comment="I'm happy."))
        session.commit()
    except Exception as e:
        print(e)
    finally:
        session.close()

    yield


app = FastAPI(lifespan=lifespan)
repo_service = AuthDataRepository()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/signup")
async def signup(request_body: SignupRequest):
    repo_service.insert_user(AuthData(user_id=request_body.user_id, password=request_body.password))
    inserted_user = repo_service.fetch_user(request_body.user_id)

    return {
        "message": "Account successfully created",
        "user": {
            "user_id": inserted_user.user_id,
            "nickname": inserted_user.user_id
        }
    }

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    c = repo_service.fetch_user("zong")
    return {"message": f"{c.password}"}


@app.patch("/users/{user_id}")
async def patch_user(user_id: str):
    repo_service.update_user(AuthData(user_id="zong", password="yyy", nickname="mao"))
    return {"message": "Hello World"}


@app.post("/close")
async def delete_user():
    repo_service.delete_user(user_id="TaroYamada")
    return {"message": "Hello World"}


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):

    if exc.status_code == 400 and exc.detail == "insert_user_duplicated":
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": "Account creation failed",
                "cause": "already same user_id is used"
            }
        )

    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})