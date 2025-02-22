from typing import Annotated

from fastapi import FastAPI

from auth_api.repository import AuthDataRepository

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/api/{user_id}")
async def test(user_id):
    repo = AuthDataRepository()
    repo.insert_user(user_id, "123")
    repo.insert_user(user_id, "122")
    return {"message": "Hello World"}