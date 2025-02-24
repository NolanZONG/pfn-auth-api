from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, status, Depends
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from auth_api.auth import authenticate
from auth_api.database import Base, engine, SessionLocal
from auth_api.model import AuthData
from auth_api.repository import AuthDataRepository
from auth_api.validator import SignupRequest, UpdateAccountRequest


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
    if user_id != auth_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"message": "No permission for Get"})

    auth_data = repo_service.fetch_user(user_id)
    if not auth_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "No User found"})

    rsp = {
        "message": "User details by user_id",
        "user": {
            "user_id": user_id,
            "nickname": user_id if not auth_data.nickname else auth_data.nickname
        }
    }
    if auth_data.comment:
        rsp["user"]["comment"] = auth_data.comment

    return rsp


@app.patch("/users/{user_id}")
async def patch_user(user_id: str, request_body: UpdateAccountRequest, auth_user_id: str = Depends(authenticate)):
    if user_id != auth_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No permission for Update")
    if "user_id" in UpdateAccountRequest or "password" in UpdateAccountRequest:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "User updation failed",
                "cause": "not updatable user_id and password"
            }
        )
    auth_data = repo_service.fetch_user(auth_user_id)
    auth_data.nickname = request_body.nickname
    auth_data.comment = request_body.comment
    repo_service.update_user(auth_data)
    return {
        "message": "User successfully updated",
        "recipe": [
            {
                "nickname": request_body.nickname if not request_body.nickname else auth_user_id,
                "comment": request_body.comment
            }
        ]
    }


@app.post("/close")
async def delete_user(auth_user_id: str = Depends(authenticate)):
    repo_service.delete_user(user_id=auth_user_id)
    return {"message": "Account and user successfully removed"}


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == status.HTTP_401_UNAUTHORIZED:
        return JSONResponse(status_code=exc.status_code, content=exc.detail, headers=exc.headers)
    else:
        return JSONResponse(status_code=exc.status_code, content=exc.detail)


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
        else:
            if "user_id" in error["loc"] or "password" in error["loc"]:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "message": "Account creation failed",
                        "cause": error["msg"].split(",")[-1]
                    }
                )
            else:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "message": "User updation failed",
                        "cause": error["msg"].split(",")[-1]
                    }
                )
