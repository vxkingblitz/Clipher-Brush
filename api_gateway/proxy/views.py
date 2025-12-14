import requests
from django.http import HttpResponse
from proxy.services import SERVICES
from common.exceptions import ApiException


class ProxyView:

    @staticmethod
    def forward(request, service_name: str, path: str):
        if service_name not in SERVICES:
            raise ApiException(
                title="Service error",
                description="Service not found",
                status=404
            )

        service_url = f"{SERVICES[service_name]}/{path}"

        headers = {
            key: value for key, value in request.headers.items()
            if key.lower() != "host"
        }

        headers["X-User-Id"] = str(getattr(request, "user_id", ""))

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
                title="Service unavailable",
                description=f"{service_name} is unavailable",
                status=503
            )

        if response.status_code >= 400:
            try:
                return HttpResponse(
                    response.content,
                    status=response.status_code,
                    content_type="application/json"
                )
            except Exception:
                raise ApiException(
                    title="Service error",
                    description="Invalid response from service",
                    status=500
                )

        return HttpResponse(
            response.content,
            status=response.status_code,
            content_type=response.headers.get("Content-Type")
        )
