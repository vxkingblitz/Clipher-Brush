import requests
from django.http import HttpResponse
from django.core.files.uploadedfile import InMemoryUploadedFile
import io


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

        # Для медиа файлов проксируем напрямую к /media/ без префикса /paintings/
        if path.startswith("media/"):
            target_url = f"{base_url}/{path}"
        else:
            target_url = f"{base_url}/{service}/{path}"

        headers = {
            key: value
            for key, value in request.headers.items()
            if key.lower() not in ["host", "content-length"]
        }

        # Прокидываем user_id из JWT в микросервисы через заголовок,
        # чтобы они могли понимать, от какого пользователя пришел запрос
        user_id = getattr(request, "user_id", None)
        if user_id is not None:
            headers["X-User-Id"] = str(user_id)
            
            # Для POST запросов к paintings получаем username из auth_service
            # и передаем его через заголовок, чтобы сохранить в базе
            if service == "paintings" and request.method == "POST":
                try:
                    auth_url = f"{SERVICE_URLS['auth']}/auth/users/{user_id}/"
                    print(f"API Gateway: Requesting user info from {auth_url}")
                    auth_response = requests.get(
                        auth_url,
                        timeout=2
                    )
                    print(f"API Gateway: Auth service response status: {auth_response.status_code}")
                    if auth_response.status_code == 200:
                        user_data = auth_response.json()
                        print(f"API Gateway: User data received: {user_data}")
                        username = user_data.get("username")
                        # Если username null или пустой, используем first_name как fallback
                        if not username or username.strip() == "":
                            username = user_data.get("first_name") or user_data.get("last_name") or None
                        if username:
                            headers["X-Username"] = str(username)
                            print(f"API Gateway: Setting X-Username header to '{username}' for user_id {user_id}")
                        else:
                            print(f"API Gateway: Warning - Username is null/empty for user_id {user_id}, user_data: {user_data}")
                    else:
                        print(f"API Gateway: Failed to get user {user_id}, status: {auth_response.status_code}, response: {auth_response.text}")
                except Exception as e:
                    # Если не удалось получить username, продолжаем без него
                    print(f"API Gateway: Error getting username for user_id {user_id}: {e}")
                    import traceback
                    print(traceback.format_exc())

        # Обработка multipart/form-data для загрузки файлов
        # Для multipart передаем raw body напрямую, так как Django может не парсить его автоматически
        content_type = request.META.get('CONTENT_TYPE', '')
        is_multipart = 'multipart/form-data' in content_type.lower()
        
        if is_multipart:
            # Для multipart передаем raw body с оригинальным Content-Type
            # Это сохранит boundary и все данные
            data = request.body
            # Сохраняем оригинальный Content-Type с boundary
            if 'content-type' not in headers and content_type:
                headers['Content-Type'] = content_type
        else:
            # Для обычных запросов (JSON и т.д.) используем body
            data = request.body
            # Убираем Content-Type из заголовков для body, чтобы requests сам определил
            if 'content-type' in headers:
                if 'application/json' not in headers.get('content-type', '').lower():
                    headers.pop('content-type', None)
        
        response = requests.request(
            method=request.method,
            url=target_url,
            headers=headers,
            data=data,
            params=request.GET,
            timeout=120 if is_multipart else 30,
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
