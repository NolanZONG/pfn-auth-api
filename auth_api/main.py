from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI

from auth_api.database import Base, engine, SessionLocal
from auth_api.model import AuthData
from auth_api.repository import AuthDataRepository


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


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/signup")
async def signup(user_id):
    repo = AuthDataRepository()
    repo.insert_user(AuthData(user_id="zong", password="www"))
    return {"message": "Hello World"}

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    repo = AuthDataRepository()
    c = repo.fetch_user("zong")
    return {"message": f"{c.password}"}


@app.patch("/users/{user_id}")
async def patch_user():
    repo = AuthDataRepository()
    repo.update_user(AuthData(user_id="zong", password="yyy", nickname="mao"))
    return {"message": "Hello World"}


@app.post("/close")
async def delete_user():
    repo = AuthDataRepository()
    repo.delete_user(AuthData(user_id="TaroYamada", password="PaSSwd4TY", nickname="Taro", comment="I'm happy."))
    return {"message": "Hello World"}
