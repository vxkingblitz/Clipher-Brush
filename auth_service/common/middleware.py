from django.http import JsonResponse
from common.exceptions import ApiException


class ApiExceptionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except ApiException as exc:
            return JsonResponse(
                {
                    "title": exc.title,
                    "description": exc.description,
                    "status": exc.status
                },
                status=exc.status
            )
