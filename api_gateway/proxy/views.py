import requests
from django.http import HttpResponse


SERVICE_URLS = {
    "auth": "http://auth-service:8000",
    "paintings": "http://painting-service:8000",
    "catalog": "http://catalog-service:8000",
}


class ProxyView:

    @staticmethod
    def forward(request, service, path):
        base_url = SERVICE_URLS.get(service)
        if not base_url:
            return HttpResponse(status=404)

        target_url = f"{base_url}/{service}/{path}"

        headers = {
            key: value
            for key, value in request.headers.items()
            if key.lower() != "host"
        }

        response = requests.request(
            method=request.method,
            url=target_url,
            headers=headers,
            data=request.body,
            params=request.GET,
        )

        return HttpResponse(
            response.content,
            status=response.status_code,
            content_type=response.headers.get("Content-Type"),
        )
