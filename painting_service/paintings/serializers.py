from rest_framework import serializers
from .models import Painting
import requests
import os
from django.conf import settings


class PaintingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Painting
        fields = [
            "photo",
            "category_id",
            "markers_set_id",
            "colors_amount",
        ]


def get_username_from_auth_service(user_id):
    """Получает username из auth_service по user_id"""
    try:
        response = requests.get(
            f"http://auth-service:8001/auth/users/{user_id}/",
            timeout=2
        )
        if response.status_code == 200:
            user_data = response.json()
            return user_data.get("username")
    except Exception:
        pass
    return None


def build_media_url(image_field_value):
    """Преобразует внутренний URL медиафайла в URL через API Gateway"""
    if not image_field_value:
        return None
    
    if not isinstance(image_field_value, str):
        return str(image_field_value)
    
    # Получаем базовый URL API из переменной окружения или используем дефолтный
    api_base_url = os.getenv('API_BASE_URL', 'https://cipherbrush.ru/api')
    
    # Если URL уже абсолютный и содержит внутренний адрес сервиса, заменяем его
    if 'painting-service:8002' in image_field_value:
        # Извлекаем путь к файлу (например, /media/numbered_1.png)
        if '/media/' in image_field_value:
            media_path = image_field_value.split('/media/')[1]
        else:
            # Пытаемся извлечь имя файла
            media_path = image_field_value.split('/')[-1]
        
        return f"{api_base_url}/paintings/media/{media_path}"
    
    # Если URL уже правильный (через API Gateway или внешний), возвращаем как есть
    if image_field_value.startswith('http'):
        # Проверяем, не содержит ли он внутренний адрес
        if 'painting-service:8002' not in image_field_value:
            return image_field_value
    
    # Если относительный путь начинается с /media/, преобразуем его
    if image_field_value.startswith('/media/'):
        media_path = image_field_value.replace('/media/', '', 1)
        return f"{api_base_url}/paintings/media/{media_path}"
    
    # Если путь не начинается с /, но содержит media, добавляем базовый URL
    if 'media/' in image_field_value and not image_field_value.startswith('http'):
        if image_field_value.startswith('media/'):
            return f"{api_base_url}/paintings/{image_field_value}"
        else:
            # Извлекаем путь после media/
            if '/media/' in image_field_value:
                media_path = image_field_value.split('/media/')[1]
                return f"{api_base_url}/paintings/media/{media_path}"
    
    # Если ничего не подошло, возвращаем как есть (может быть уже правильный URL)
    return image_field_value


class PaintingResponseSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()
    painting_numbered = serializers.SerializerMethodField()
    painting_colored = serializers.SerializerMethodField()

    class Meta:
        model = Painting
        fields = "__all__"

    def get_username(self, obj):
        if obj.user_id:
            return get_username_from_auth_service(obj.user_id)
        return None

    def get_photo(self, obj):
        if obj.photo:
            try:
                # Получаем URL из ImageField
                url = obj.photo.url if hasattr(obj.photo, 'url') else str(obj.photo)
                return build_media_url(url)
            except (ValueError, AttributeError):
                return None
        return None

    def get_painting_numbered(self, obj):
        if obj.painting_numbered:
            try:
                url = obj.painting_numbered.url if hasattr(obj.painting_numbered, 'url') else str(obj.painting_numbered)
                return build_media_url(url)
            except (ValueError, AttributeError):
                return None
        return None

    def get_painting_colored(self, obj):
        if obj.painting_colored:
            try:
                url = obj.painting_colored.url if hasattr(obj.painting_colored, 'url') else str(obj.painting_colored)
                return build_media_url(url)
            except (ValueError, AttributeError):
                return None
        return None


class PublicPaintingSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    painting_numbered = serializers.SerializerMethodField()
    painting_colored = serializers.SerializerMethodField()

    class Meta:
        model = Painting
        fields = [
            "painting_id",
            "user_id",
            "username",
            "painting_numbered",
            "painting_colored",
            "generated_at",
            "category_id",
            "colors_amount",
        ]

    def get_username(self, obj):
        if obj.user_id:
            return get_username_from_auth_service(obj.user_id)
        return None

    def get_painting_numbered(self, obj):
        if obj.painting_numbered:
            try:
                url = obj.painting_numbered.url if hasattr(obj.painting_numbered, 'url') else str(obj.painting_numbered)
                return build_media_url(url)
            except (ValueError, AttributeError):
                return None
        return None

    def get_painting_colored(self, obj):
        if obj.painting_colored:
            try:
                url = obj.painting_colored.url if hasattr(obj.painting_colored, 'url') else str(obj.painting_colored)
                return build_media_url(url)
            except (ValueError, AttributeError):
                return None
        return None
