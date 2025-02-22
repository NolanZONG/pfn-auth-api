"""
Auth Data Model

This module defines the `AuthData` model class using the Pydantic library.
The model represents a user auth data record with properties for user_id, password, nickname, comment.
"""

from pydantic import BaseModel


class AuthData(BaseModel):
    """
    Auth Data Model

    This class represents a user auth data record with properties for user_id, password, nickname, comment.
    """
    user_id: str
    password: str
    nickname: str
    comment: str

    class Config:
        orm_mode = True