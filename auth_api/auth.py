"""
HTTP Basic Auth module

This module is used to process http basic auth globally.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

from auth_api.repository import AuthDataRepository

security = HTTPBasic()


def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    """
    HTTP basic auth
    """
    repo = AuthDataRepository()

    fetched_auth_data = repo.fetch_user(credentials.username)
    if not fetched_auth_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "No User found"})

    if not secrets.compare_digest(credentials.password, fetched_auth_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Authentication Failed"},
            headers={"WWW-Authenticate": "Basic"}
        )

    return credentials.username
