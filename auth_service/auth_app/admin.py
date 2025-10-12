from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserSession

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('telegram_id', 'username', 'first_name', 'plan_type', 'created_at')
    list_filter = ('plan_type', 'auth_type', 'created_at')
    search_fields = ('telegram_id', 'username', 'first_name', 'last_name')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Telegram Info', {
            'fields': ('telegram_id', 'auth_type', 'plan_type')
        }),
    )

@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_token', 'created_at', 'expires_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('user__telegram_id', 'session_token')