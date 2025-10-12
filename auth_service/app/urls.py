from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    HealthView,
    TelegramAuthView,
    UserProfileView,
    UpgradePlanView,
    LogoutView,
    ValidateSessionView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', HealthView.as_view(), name='health-cheack'),
    path('auth/telegram/', TelegramAuthView.as_view(), name='telegram-auth'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/validate-session/', ValidateSessionView.as_view(), name='validate-session'),
    path('user/profile/', UserProfileView.as_view(), name='user-profile'),
    path('user/upgrade-plan/', UpgradePlanView.as_view(), name='upgrade-plan'),
]
