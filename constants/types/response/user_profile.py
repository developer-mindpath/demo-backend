from ninja import Schema


class UserProfileResponseSchema(Schema):
    username: str
    email: str
    message: str
