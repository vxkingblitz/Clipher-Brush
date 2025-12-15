from django.urls import path
from processor.views import ProcessImageView

urlpatterns = [
    path("process/", ProcessImageView.as_view()),
]
