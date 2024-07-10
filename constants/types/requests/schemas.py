from typing import Optional

from ninja import Schema


class SignupSchema(Schema):
    first_name: str
    last_name: Optional[str] = None
    email: str
    password: str


class LoginSchema(Schema):
    email: str
    password: str
