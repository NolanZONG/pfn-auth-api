from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, status, Depends
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from auth_api.auth import authenticate
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
    return {"message": "Hello! This is PFN coding test"}


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
async def get_user(user_id: str, auth_user_id: str = Depends(authenticate)):
    c = repo_service.fetch_user("zong")
    return {"user_id": f"{user_id}", "name": auth_user_id}



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
    if exc.status_code == status.HTTP_400_BAD_REQUEST and exc.detail == "insert_user_duplicated":
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": "Account creation failed",
                "cause": "already same user_id is used"
            }
        )
    if exc.status_code == status.HTTP_404_NOT_FOUND:
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": "No User found"}
        )

    if exc.status_code == status.HTTP_401_UNAUTHORIZED:
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": "Authentication Failed"},
            headers={"WWW-Authenticate": "Basic"}
        )
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    for error in exc.errors():
        if error["type"] == "missing":
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "message": "Account creation failed",
                    "cause": "required user_id and password"
                }
            )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message": "Account creation failed",
                "cause": f"{'.'.join(str(loc) for loc in error["loc"][1:])}:{error['msg']}"
            }
        )


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "message": "Account creation failed",
            "cause": str(exc)
        }
    )
