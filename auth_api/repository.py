"""
Auth Data Repository

This module provides a repository class for managing user auth data in the database.
The `AuthDataRepository` class interacts with the `AuthData` model to perform operations.
"""
from typing import Optional

from fastapi import HTTPException

from sqlalchemy.exc import IntegrityError

from .model import AuthData
from .database import SessionLocal


class AuthDataRepository:
    """
    This class provides methods for interacting with the user auth data in the database.
    """
    def __init__(self):
        """
        Initializes the repository by creating an SQLAlchemy session.
        """
        self.session = SessionLocal()


    def insert_user(self, auth_data: AuthData) -> None:
        """
        Insert a user auth data record into the database
        """
        try:
            self.session.add(auth_data)
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise HTTPException(status_code=400, detail="already exist")
        finally:
            self.session.close()

    def delete_user(self, user_id: str) -> None:
        """
        Delete the user auth data record from the database by user_id
        """
        try:
            data = self.session.get(AuthData, user_id)
            self.session.delete(data)
            self.session.commit()
        except Exception:
            self.session.rollback()
        finally:
            self.session.close()

    def fetch_user(self, user_id: str) -> Optional[AuthData]:
        """
        Fetch a user auth data record by specified user_id
        """
        try:
            auth_data = self.session.get(AuthData, user_id)
            return auth_data
        except Exception:
            print("error")
        finally:
            self.session.close()

    def update_user(self, auth_data: AuthData) -> None:
        """
        Update a user auth data record by provided new object
        """
        try:
            self.session.query(AuthData).filter(AuthData.user_id==auth_data.user_id).update(
                {
                    "password": auth_data.password,
                    "nickname": auth_data.nickname,
                    "comment": auth_data.comment
                }
            )
            self.session.commit()
        except Exception:
            self.session.rollback()
            print("error")
        finally:
            self.session.close()
