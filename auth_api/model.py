"""
Auth Data Model

This module defines an SQLAlchemy model for storing user auth data in the MySQL database.
"""

from sqlalchemy import Column, String

from .database import Base


class AuthData(Base):
    """
    represents a table named "auth_data"
    """
    __tablename__ = "auth_data"

    user_id = Column(String(32), primary_key=True)
    password = Column(String(32), nullable=False)
    nickname = Column(String(32), nullable=True)
    comment = Column(String(128), nullable=True)
