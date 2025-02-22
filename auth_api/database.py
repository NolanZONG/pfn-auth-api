"""
Database Configuration using SQLAlchemy

This module sets up the configuration for connecting to a MySQL database using SQLAlchemy.
It defines the necessary environment variables for the database credentials
and creates a SQLAlchemy engine and session maker for establishing connections and managing sessions.
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from auth_api.model import AuthData


db_user = os.environ["DB_USER"]
db_password = os.environ["DB_PASSWORD"]
db_host = os.environ["DB_HOST"]
db_name = os.environ["DB_NAME"]
preset_user = AuthData(user_id="TaroYamada", password="PaSSwd4TY", nickname="Taro", comment="I'm happy.")

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"

engine = create_engine(url=SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        session.add(preset_user)
        session.commit()
    except Exception as e:
        print(e)
    finally:
        session.close()