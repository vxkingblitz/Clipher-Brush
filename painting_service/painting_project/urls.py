from django.urls import include, path

urlpatterns = [
    path("paintings/", include("paintings.urls")),
]
