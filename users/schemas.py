from typing import Optional, Any

from ninja import Schema


class SignupSchema(Schema):
    first_name: str
    last_name: Optional[str] = None
    email: str
    password: str


class LoginSchema(Schema):
    email: str
    password: str


class LoginSuccessResponseSchema(Schema):
    message: str
    user_id: int
    token: Any


class SignupSuccessResponseSchema(Schema):
    message: str
    user_id: int
    

class UserProfileResponseSchema(Schema):
    username: str
    email: str
    message: str
