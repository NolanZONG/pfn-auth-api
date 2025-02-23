"""
Validators for auth api requests

This module defines the validator classes for validating the request body of auth api
"""
import re

from pydantic import BaseModel, field_validator, Field, model_validator


class SignupRequest(BaseModel):
    """
    Validator class for validating signup request body
    """
    user_id: str = Field(min_length=6, max_length=20)
    password: str = Field(min_length=8, max_length=20)

    @field_validator("user_id")
    def user_id_pattern(cls, value):
        if re.search(r"[^a-zA-Z0-9]", value):
            raise ValueError("user_id can only contain half-width alphanumeric characters")
        return value

    @field_validator("password")
    def password_pattern(cls, value):
        if re.search(r"[\s\00-\x1F\x7F]", value):
            raise ValueError("password cannot contain spaces or control characters")
        return value


class UpdateAccountRequest(BaseModel):
    """
    Validator class for validating update account request body
    """
    nickname: str | None = Field(default=None, max_length=30)
    comment: str | None = Field(default=None)

    @field_validator("nickname")
    def nickname_pattern(cls, value):
        if re.search(r"[\00-\x1F\x7F]", value):
            raise ValueError("nickname cannot contain control characters")
        return value

    @field_validator("comment")
    def comment_pattern(cls, value):
        if re.search(r"[\00-\x1F\x7F]", value):
            raise ValueError("comment cannot contain control characters")
        return value

    @model_validator(mode="before")
    def at_least_one_field(cls, values):
        if not values.get("nickname") and not values.get("comment"):
            raise ValueError("required nickname or comment")
        return values
