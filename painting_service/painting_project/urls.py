from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("paintings/", include("paintings.urls")),
]

# Раздача медиа файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
