from django.urls import re_path
from proxy.views import ProxyView

urlpatterns = [
    re_path(
        r"^(?P<service>auth|paintings|catalog)/(?P<path>.*)$",
        lambda request, service, path: ProxyView.forward(request, service, path)
    ),
]
