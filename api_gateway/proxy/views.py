import requests
from django.http import HttpResponse
from proxy.services import SERVICES
from common.exceptions import ApiException


class ProxyView:
    @staticmethod
    def forward(request, service, path):
        if service not in SERVICES:
            raise ApiException(
                "Service error",
                "Service not found",
                404
            )

        service_url = f"{SERVICES[service]}/{path}"

        headers = {
            key: value
            for key, value in request.headers.items()
            if key.lower() != "host"
        }

        # пробрасываем user_id дальше
        if hasattr(request, "user_id"):
            headers["X-User-Id"] = str(request.user_id)

        try:
            response = requests.request(
                method=request.method,
                url=service_url,
                headers=headers,
                params=request.GET,
                data=request.body,
                timeout=30
            )
        except requests.RequestException:
            raise ApiException(
                "Service unavailable",
                f"{service} service unavailable",
                503
            )

        return HttpResponse(
            response.content,
            status=response.status_code,
            content_type=response.headers.get("Content-Type", "application/json")
        )
