from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ninja import NinjaAPI
from ninja.errors import HttpError
from rest_framework.authtoken.models import Token

from common.auth.authentication import decrypt_message
from common.constants.common import AUTHORIZATION, PROJECT_TITLE, USER
from common.enums.http_status_code import HttpStatus
from common.constants.messages import EMAIL_ALREADY_EXISTS, EXCEPTION_OCCURED, INTERNAL_SERVER_ERROR_MESSAGE, LOGIN_INVALID_CREDENTIANLS_MESSAGE, LOGIN_MESSAGE, LOGOUT_SUCCESS_MESSAGE, PROFILE_MESSAGE, SIGN_UP_MESSAGE, TOKEN_ERROR_MESSAGE
from common.helpers.logger_helper import logger
from users.schemas import LoginSchema, LoginSuccessResponseSchema, LogoutResponseSchema, SignupSchema, SignupSuccessResponseSchema, UserProfileResponseSchema

api = NinjaAPI(title=PROJECT_TITLE)


@api.post("/signup", response=SignupSuccessResponseSchema, tags=[USER])
@csrf_exempt
def signup(request: HttpRequest, payload: SignupSchema) -> JsonResponse:
    try:
        User.objects.create_user(
            username=payload.email,
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=payload.email,
            password=payload.password,
        )
        response = SignupSuccessResponseSchema(message=SIGN_UP_MESSAGE).dict()
        return JsonResponse(response, status=HttpStatus.HTTP_200_OK.value, safe=True)
    except IntegrityError as e:
        logger.exception(f"{EXCEPTION_OCCURED} {e}")
        raise HttpError(HttpStatus.HTTP_409_CONFLICT.value, EMAIL_ALREADY_EXISTS)
    except Exception as e:
        logger.exception(f"{EXCEPTION_OCCURED} {e}")
        raise HttpError(HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR.value, INTERNAL_SERVER_ERROR_MESSAGE)


@api.post("/login", response=LoginSuccessResponseSchema, tags=[USER])
@csrf_exempt
def login(request: HttpRequest, payload: LoginSchema) -> JsonResponse:
    try:
        decrypted_email = decrypt_message(payload.email)
        decrypted_password = decrypt_message(payload.password)
        user = authenticate(username=decrypted_email, password=decrypted_password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            response = LoginSuccessResponseSchema(
                message=LOGIN_MESSAGE,
                token=token.key
            ).dict()
            return JsonResponse(response, status=HttpStatus.HTTP_200_OK.value, safe=False)
        else:
            raise HttpError(HttpStatus.HTTP_401_UNAUTHORIZED.value, LOGIN_INVALID_CREDENTIANLS_MESSAGE)
    except HttpError as e:
        logger.exception(f"{EXCEPTION_OCCURED} {e}")
        raise e
    except Exception as e:
        logger.exception(f"{EXCEPTION_OCCURED} {e}")
        raise HttpError(HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR.value, INTERNAL_SERVER_ERROR_MESSAGE)


@api.post("/logout", response=dict, tags=[USER])
@csrf_exempt
def logout(request: HttpRequest) -> JsonResponse:
    try:
        token = request.headers.get(AUTHORIZATION)
        token_obj = Token.objects.get(key=token)
        token_obj.delete()
        response = LogoutResponseSchema(message=LOGOUT_SUCCESS_MESSAGE).dict()
        return JsonResponse(response, status=HttpStatus.HTTP_200_OK.value, safe=False)
    except Token.DoesNotExist:
        logger.exception(f"{EXCEPTION_OCCURED} {e}")
        raise HttpError(HttpStatus.HTTP_401_UNAUTHORIZED.value, TOKEN_ERROR_MESSAGE)
    except Exception as e:
        logger.exception(f"{EXCEPTION_OCCURED} {e}")
        raise HttpError(HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR.value, INTERNAL_SERVER_ERROR_MESSAGE)


@api.get("/user", response=UserProfileResponseSchema, tags=[USER])
@csrf_exempt
def user(request: HttpRequest) -> JsonResponse:
    try:
        token = request.headers.get(AUTHORIZATION)
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        response = UserProfileResponseSchema(
            username=user.first_name,
            email=user.email,
            message=PROFILE_MESSAGE
        ).dict()
        return JsonResponse(response, status=HttpStatus.HTTP_200_OK.value, safe=False)
    except Token.DoesNotExist:
        logger.exception(f"{EXCEPTION_OCCURED} {e}")
        raise HttpError(HttpStatus.HTTP_401_UNAUTHORIZED.value, TOKEN_ERROR_MESSAGE)
    except Exception as e:
        logger.exception(f"{EXCEPTION_OCCURED} {e}")
        raise HttpError(HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR.value, INTERNAL_SERVER_ERROR_MESSAGE)
