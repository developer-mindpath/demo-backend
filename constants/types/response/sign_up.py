from ninja import Schema


class SignupSuccessResponseSchema(Schema):
    message: str
    user_id: int

# SIGNUP_SUCCESS = {"status": "success", "message": "User created successfully", "user_id": ""}