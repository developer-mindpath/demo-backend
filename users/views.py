from datetime import datetime

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from ninja import NinjaAPI
from rest_framework.authtoken.models import Token

from users.constants.constants import (HTTP_200_OK, HTTP_201_CREATED,
                                       HTTP_400_BAD_REQUEST,
                                       HTTP_401_UNAUTHORIZED, LOGIN_ERROR,
                                       LOGIN_INVALID_CREDENTIALS,
                                       LOGIN_SUCCESS, LOGOUT_ERROR,
                                       LOGOUT_SUCCESS, PROFILE_ERROR,
                                       PROFILE_SUCCESS, PROJECT_TITLE,
                                       SIGNUP_ERROR, SIGNUP_SUCCESS, USER_ID)
from users.keys import decrypt_message
from users.logger import logger
from users.schemas import LoginSchema, SignupSchema

api = NinjaAPI(title=PROJECT_TITLE)


@api.post("/signup", response=dict, tags=["User"])
@csrf_exempt
def signup(request: HttpRequest, payload: SignupSchema) -> JsonResponse:
    try:
        timestamp = datetime.now().timestamp()
        user = User.objects.create_user(
            username=payload.email,
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=payload.email,
            password=payload.password,
            id=timestamp
        )
        response = SIGNUP_SUCCESS.copy()
        response.update({USER_ID: timestamp})
        return JsonResponse(response, status=HTTP_201_CREATED)
    except Exception as e:
        logger.info(e)
        return JsonResponse(SIGNUP_ERROR, status=HTTP_400_BAD_REQUEST)


@api.post("/login", response=dict, tags=["User"])
@csrf_exempt
def login(request: HttpRequest, payload: LoginSchema) -> JsonResponse:
    try:
        decrypted_email = decrypt_message(payload.email)
        decrypted_password = decrypt_message(payload.password)
        user = authenticate(username=decrypted_email, password=decrypted_password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            response = LOGIN_SUCCESS.copy()
            response.update({USER_ID: user.id})
            return JsonResponse({"token": token.key, **response}, status=HTTP_200_OK)
        else:
            return JsonResponse(LOGIN_INVALID_CREDENTIALS, status=HTTP_401_UNAUTHORIZED)
    except Exception as e:
        logger.info(e)
        return JsonResponse(LOGIN_ERROR, status=HTTP_400_BAD_REQUEST)


@api.post("/logout", response=dict, tags=["User"])
@csrf_exempt
def logout(request: HttpRequest) -> JsonResponse:
    try:
        token = request.headers.get('Authorization')
        token_obj = Token.objects.get(key=token)
        token_obj.delete()
        return JsonResponse(LOGOUT_SUCCESS, status=HTTP_200_OK)
    except Token.DoesNotExist:
        return JsonResponse(LOGOUT_ERROR, status=HTTP_401_UNAUTHORIZED)


@api.get("/users/{user_id}", response=dict, tags=["User"])
@csrf_exempt
def profile(request: HttpRequest, user_id: int) -> JsonResponse:
    try:
        token = request.headers.get('Authorization')
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        requested_user = User.objects.get(id=user_id)
        return JsonResponse({"username": f"{requested_user.first_name} {requested_user.last_name}", "email": requested_user.email, **PROFILE_SUCCESS}, status=HTTP_200_OK)
    except Token.DoesNotExist:
        return JsonResponse(PROFILE_ERROR, status=HTTP_401_UNAUTHORIZED)
