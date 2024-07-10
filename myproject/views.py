from typing import Dict

from django.http import HttpRequest, JsonResponse


def health_check(request: HttpRequest) -> JsonResponse:
    response_data: Dict[str, str] = {"status": "ok"}
    return JsonResponse(response_data)
