from typing import Optional
from ninja import NinjaAPI, Schema
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from ninja.errors import HttpError
from django.views.decorators.csrf import csrf_exempt

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

def load_public_key():
    with open("./public_key.pem", "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())
    return public_key

def load_private_key():
    with open("./private_key.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)
    return private_key

# def encrypt_message(message: str, public_key):
#     encrypted = public_key.encrypt(
#         message.encode(),
#         padding.OAEP(
#             mgf=padding.MGF1(algorithm=hashes.SHA256()),
#             algorithm=hashes.SHA256(),
#             label=None,
#         ),
#     )
#     return encrypted
import base64
def decrypt_message(encrypted_message, private_key):
    encrypted_message = base64.b64decode(encrypted_message.encode('utf-8'))
    decrypted = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return decrypted.decode()

private_key = load_private_key()
public_key = load_public_key()

api = NinjaAPI()

class SignupSchema(Schema):
    first_name: str
    last_name: Optional[str] = None
    email: str
    password: str

class LoginSchema(Schema):
    email: str
    password: str

@api.post("/signup")
@csrf_exempt
def signup(request, payload: SignupSchema):
    try:
        user = User.objects.create_user(username=payload.email, first_name=payload.first_name, last_name=payload.last_name, email=payload.email, password=payload.password)
        return {"status": "success", "message": "User created successfully"}
    except Exception as e:
        print(e)
        raise HttpError(400, "Signup failed")

@api.post("/login")
@csrf_exempt
def login(request, payload: LoginSchema):
    try:
        decrypted_email = decrypt_message(payload.email, private_key)
        decrypted_password = decrypt_message(payload.password, private_key)
        user = authenticate(username=decrypted_email, password=decrypted_password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return {"status": "success", "token": token.key}
        else:
            raise HttpError(401, "Invalid email or password")
    except Exception as e:
        raise HttpError(400, "Invalid request")

@api.post("/logout")
@csrf_exempt
def logout(request, token: str):
    try:
        token_obj = Token.objects.get(key=token)
        token_obj.delete()
        return {"status": "success", "message": "Logout successful"}
    except Token.DoesNotExist:
        raise HttpError(401, "Invalid token")

@api.get("/profile")
@csrf_exempt
def profile(request, token: str):
    try:
        token_obj = Token.objects.get(key=token)
        user = token_obj.user

        return {"username": f"{user.first_name} {user.last_name}" , "email": user.email}
    except Token.DoesNotExist:
        raise HttpError(401, "Invalid token")
