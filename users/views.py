from datetime import datetime

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ninja import NinjaAPI
from rest_framework.authtoken.models import Token

from constants.constants import AUTHORIZATION, LOGIN_ERROR_MESSAGE, LOGIN_INVALID_CREDENTIANLS_MESSAGE, LOGOUT_SUCCESS_MESSAGE, PROJECT_TITLE, SIGNUP_ERROR_MESSAGE, TOKEN_ERROR_MESSAGE
from constants.enums.http_status_code import HttpStatus
from constants.messages import LOGIN_MESSAGE, PROFILE_MESSAGE, SIGN_UP_MESSAGE
from constants.helper.decryption_helper import logger
from constants.types.response.login import LoginSuccessResponseSchema
from constants.types.response.sign_up import SignupSuccessResponseSchema
from constants.types.response.user_profile import UserProfileResponseSchema
from constants.types.requests.schemas import LoginSchema, SignupSchema
from users.keys import decrypt_message

api = NinjaAPI(title=PROJECT_TITLE)


@api.post("/signup", response=SignupSuccessResponseSchema, tags=["User"])
@csrf_exempt
def signup(request: HttpRequest, payload: SignupSchema) -> JsonResponse:
    try:
        timestamp = datetime.now().timestamp() * 1000000
        user = User.objects.create_user(
            username=payload.email,
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=payload.email,
            password=payload.password,
            id=timestamp
        )
        response = SignupSuccessResponseSchema(
            message=SIGN_UP_MESSAGE,
            user_id=timestamp
        ).dict()
        return JsonResponse(response, status=HttpStatus.HTTP_200_OK.value, safe=False)
    except ValueError as ve:
        logger.info(ve)
        return JsonResponse(data=SIGNUP_ERROR_MESSAGE, status=HttpStatus.HTTP_400_BAD_REQUEST.value, safe=False)
    except Exception as e:
        logger.info(e)
        return JsonResponse(SIGNUP_ERROR_MESSAGE, status=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR.value, safe=False)


@api.post("/login", response=LoginSuccessResponseSchema, tags=["User"])
@csrf_exempt
def login(request: HttpRequest, payload: LoginSchema) -> JsonResponse:
    try:
        decrypted_email = decrypt_message(payload.email)
        decrypted_password = decrypt_message(payload.password)
        user = authenticate(username=decrypted_email,
                            password=decrypted_password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            response = LoginSuccessResponseSchema(
                user_id=user.id,
                message=LOGIN_MESSAGE,
                token=token.key
            ).dict()
            print(response)
            return JsonResponse(response, status=HttpStatus.HTTP_200_OK.value, safe=False)
        else:
            return JsonResponse(LOGIN_INVALID_CREDENTIANLS_MESSAGE, status=HttpStatus.HTTP_401_UNAUTHORIZED.value, safe=False)
    except ValueError as ve:
        logger.info(ve)
        return JsonResponse(LOGIN_ERROR_MESSAGE, status=HttpStatus.HTTP_400_BAD_REQUEST.value, safe=False)
    except Exception as e:
        logger.info(e)
        return JsonResponse(LOGIN_ERROR_MESSAGE, status=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR.value, safe=False)


@api.post("/logout", response=dict, tags=["User"])
@csrf_exempt
def logout(request: HttpRequest) -> JsonResponse:
    try:
        token = request.headers.get(AUTHORIZATION)
        token_obj = Token.objects.get(key=token)
        token_obj.delete()
        return JsonResponse(LOGOUT_SUCCESS_MESSAGE, status=HttpStatus.HTTP_200_OK.value, safe=False)
    except Token.DoesNotExist:
        return JsonResponse(TOKEN_ERROR_MESSAGE, status=HttpStatus.HTTP_401_UNAUTHORIZED.value, safe=False)
    except Exception as e:
        logger.info(e)
        return JsonResponse(SIGNUP_ERROR_MESSAGE, status=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR.value, safe=False)


@api.get("/users/{user_id}", response=UserProfileResponseSchema, tags=["User"])
@csrf_exempt
def profile(request: HttpRequest, user_id: int) -> JsonResponse:
    try:
        token = request.headers.get(AUTHORIZATION)
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        requested_user = User.objects.get(id=user_id)
        response = UserProfileResponseSchema(
            username=requested_user.first_name,
            email=requested_user.email,
            message=PROFILE_MESSAGE
        ).dict()
        return JsonResponse(response, status=HttpStatus.HTTP_200_OK.value, safe=False)
    except Token.DoesNotExist:
        return JsonResponse(TOKEN_ERROR_MESSAGE, status=HttpStatus.HTTP_401_UNAUTHORIZED.value, safe=False)
