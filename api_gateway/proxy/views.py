import requests
from django.http import HttpResponse


SERVICE_URLS = {
    "auth": "http://auth-service:8001",
    "paintings": "http://painting-service:8002",
    "catalog": "http://catalog-service:8003",
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

        # Прокидываем user_id из JWT в микросервисы через заголовок,
        # чтобы они могли понимать, от какого пользователя пришел запрос
        user_id = getattr(request, "user_id", None)
        if user_id is not None:
            headers["X-User-Id"] = str(user_id)

        response = requests.request(
            method=request.method,
            url=target_url,
            headers=headers,
            data=request.body,
            params=request.GET,
        )

        # Создаем HttpResponse с содержимым ответа
        http_response = HttpResponse(
            response.content,
            status=response.status_code,
            content_type=response.headers.get("Content-Type", "application/json"),
        )

        # Передаем все заголовки из ответа микросервиса (кроме тех, что Django обрабатывает сам)
        excluded_headers = {
            "connection",
            "content-encoding",
            "content-length",
            "transfer-encoding",
            "server",
        }
        for header, value in response.headers.items():
            if header.lower() not in excluded_headers:
                http_response[header] = value

        return http_response
