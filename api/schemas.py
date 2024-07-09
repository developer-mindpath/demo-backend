from typing import Optional

from ninja import Schema
from ninja.errors import HttpError
from pydantic import field_validator

from .constants.messages import (FIRST_NAME_ALPHA_ERROR, FIRST_NAME_LENGTH_ERROR,
                       LAST_NAME_ALPHA_ERROR, LAST_NAME_LENGTH_ERROR,
                       PASSWORD_ALPHA_ERROR, PASSWORD_DIGIT_ERROR,
                       PASSWORD_LENGTH_ERROR)


class SignupSchema(Schema):
    first_name: str
    last_name: Optional[str] = None
    email: str
    password: str

    @field_validator('first_name')
    def first_name_validation(cls, value):
        if not (1 <= len(value) <= 50):
            raise HttpError(400, FIRST_NAME_LENGTH_ERROR)
        if not value.isalpha():
            raise HttpError(400, FIRST_NAME_ALPHA_ERROR)
        return value

    @field_validator('last_name')
    def last_name_validation(cls, value):
        if value is not None:
            if len(value) > 50:
                raise HttpError(400, LAST_NAME_LENGTH_ERROR)
            if not value.isalpha():
                raise HttpError(400, LAST_NAME_ALPHA_ERROR)
        return value

    @field_validator('password')
    def password_validation(cls, value):
        if not (8 <= len(value) <= 128):
            raise HttpError(400, PASSWORD_LENGTH_ERROR)
        if not any(char.isdigit() for char in value):
            raise HttpError(400, PASSWORD_DIGIT_ERROR)
        if not any(char.isalpha() for char in value):
            raise HttpError(400, PASSWORD_ALPHA_ERROR)
        return value


class LoginSchema(Schema):
    email: str
    password: str
