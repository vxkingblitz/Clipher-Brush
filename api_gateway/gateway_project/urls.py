from django.urls import re_path
from proxy.views import ProxyView

# Wrapper для обработки multipart/form-data
def proxy_forward(request, service, path):
    # Принудительно парсим multipart/form-data если нужно
    if request.method == 'POST' and 'multipart/form-data' in request.META.get('CONTENT_TYPE', ''):
        # Django автоматически парсит multipart через middleware, но нужно убедиться
        # что request.FILES и request.POST доступны
        pass
    return ProxyView.forward(request, service, path)

urlpatterns = [
    re_path(
        r"^(?P<service>auth|paintings|catalog)/(?P<path>.*)$",
        proxy_forward
    ),
]
