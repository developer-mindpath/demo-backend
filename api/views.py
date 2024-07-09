from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ninja import NinjaAPI
from rest_framework.authtoken.models import Token

from .constants.constants import (HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST,
                        HTTP_401_UNAUTHORIZED, LOGIN_ERROR,
                        LOGIN_INVALID_CREDENTIALS, LOGIN_SUCCESS, LOGOUT_ERROR,
                        LOGOUT_SUCCESS, PROFILE_ERROR, PROFILE_SUCCESS,
                        SIGNUP_ERROR, SIGNUP_SUCCESS, PROJECT_TITLE)
from .keys import decrypt_message, private_key
from .schemas import LoginSchema, SignupSchema

api = NinjaAPI(title=PROJECT_TITLE)


@api.post("/signup", response=dict, tags=["Authentication"])
@csrf_exempt
def signup(request, payload: SignupSchema):
    try:
        user = User.objects.create_user(
            username=payload.email,
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=payload.email,
            password=payload.password
        )
        return JsonResponse(SIGNUP_SUCCESS, status=HTTP_201_CREATED)
    except Exception as e:
        return JsonResponse(SIGNUP_ERROR, status=HTTP_400_BAD_REQUEST)


@api.post("/login", response=dict, tags=["Authentication"])
@csrf_exempt
def login(request, payload: LoginSchema):
    try:
        decrypted_email = decrypt_message(payload.email, private_key)
        decrypted_password = decrypt_message(payload.password, private_key)
        user = authenticate(username=decrypted_email,
                            password=decrypted_password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse({"token": token.key, **LOGIN_SUCCESS}, status=HTTP_200_OK)
        else:
            return JsonResponse(LOGIN_INVALID_CREDENTIALS, status=HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return JsonResponse(LOGIN_ERROR, status=HTTP_400_BAD_REQUEST)


@api.post("/logout", response=dict, tags=["Authentication"])
@csrf_exempt
def logout(request, token: str):
    try:
        token_obj = Token.objects.get(key=token)
        token_obj.delete()
        return JsonResponse(LOGOUT_SUCCESS, status=HTTP_200_OK)
    except Token.DoesNotExist:
        return JsonResponse(LOGOUT_ERROR, status=HTTP_401_UNAUTHORIZED)


@api.get("/profile", response=dict, tags=["User"])
@csrf_exempt
def profile(request, token: str):
    try:
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        return JsonResponse({"username": f"{user.first_name} {user.last_name}", "email": user.email, **PROFILE_SUCCESS}, status=HTTP_200_OK)
    except Token.DoesNotExist:
        return JsonResponse(PROFILE_ERROR, status=HTTP_401_UNAUTHORIZED)
