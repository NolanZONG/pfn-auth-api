"""
Auth Data Repository

This module provides a repository class for managing user auth data in the database.
The `AuthDataRepository` class interacts with the `AuthData` model to perform operations.
"""
from fastapi import HTTPException

from sqlalchemy.exc import IntegrityError

from auth_api.model import AuthData
from auth_api.database import SessionLocal, Base, engine


class AuthDataRepository:
    """
    This class provides methods for interacting with the user auth data in the database.
    """
    def __init__(self):
        """
        Initializes the repository by creating an SQLAlchemy session.
        """
        self.session = SessionLocal()

    def insert_user(self, user_id: str, password: str) -> None:
        """
        Insert a user auth data into the database based on the provided user_id and password

        :param user_id: the provided user_id
        :param password: the provided password
        :return: None
        """
        try:

            self.session.add(AuthData(user_id=user_id, password=password))
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise HTTPException(status_code=400, detail={
  "message": "Account creation failed",
  "cause": "already same user_id is used"
})
        finally:
            self.session.close()
