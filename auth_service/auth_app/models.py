from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta

class User(AbstractUser):
    TELEGRAM = 'telegram'
    AUTH_TYPES = [
        (TELEGRAM, 'Telegram'),
    ]
    
    PLAN_BASIC = 'basic'
    PLAN_PRO = 'pro'
    PLAN_TYPES = [
        (PLAN_BASIC, 'Basic'),
        (PLAN_PRO, 'Pro'),
    ]
    
    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True)
    username = models.CharField(max_length=150, unique=True, blank=True)
    auth_type = models.CharField(max_length=20, choices=AUTH_TYPES, default=TELEGRAM)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES, default=PLAN_BASIC)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.EmailField(blank=True, null=True)
    
    password = models.CharField(max_length=128, blank=True, null=True)
    
    class Meta:
        db_table = 'auth_users'
    
    def __str__(self):
        return f"User {self.telegram_id} ({self.plan_type})"

class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    session_token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'auth_sessions'
        indexes = [
            models.Index(fields=['session_token']),
            models.Index(fields=['expires_at']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(days=30)
        super().save(*args, **kwargs)
    
    def is_expired(self):
        return timezone.now() > self.expires_at