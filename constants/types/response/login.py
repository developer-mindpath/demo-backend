from typing import Any
from ninja import Schema


class LoginSuccessResponseSchema(Schema):
    message: str
    user_id: int
    token: Any
