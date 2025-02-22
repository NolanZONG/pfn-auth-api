from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI

from auth_api.database import Base, engine, SessionLocal, preset_user
from auth_api.repository import AuthDataRepository


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        session.add(preset_user)
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


@app.get("/api/{user_id}")
async def test(user_id):
    repo = AuthDataRepository()
    repo.insert_user(user_id, "123")
    repo.insert_user(user_id, "122")
    return {"message": "Hello World"}
