from django.urls import path
from .views import TelegramAuthView, UserDetailView

urlpatterns = [
    path("auth/telegram/", TelegramAuthView.as_view()),
    path("auth/users/<int:user_id>/", UserDetailView.as_view()),
]
