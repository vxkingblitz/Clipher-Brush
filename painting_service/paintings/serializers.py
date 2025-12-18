from rest_framework import serializers
from .models import Painting


def get_media_url(value, request=None):
    """Формирует правильный URL для медиа файла через API gateway"""
    if not value:
        return None
    
    # Если value уже полный URL с внутренним адресом, заменяем его
    if isinstance(value, str):
        if "painting-service:8002" in value:
            # Заменяем внутренний адрес на путь через API gateway
            # Извлекаем путь после /media/
            if "/media/" in value:
                path = value.split("/media/")[1]
                # Возвращаем путь через API gateway (nginx проксирует /api/ к gateway)
                return f"/api/paintings/media/{path}"
            return value.replace("http://painting-service:8002", "/api/paintings")
        elif value.startswith("http://") or value.startswith("https://"):
            # Если это внешний URL, оставляем как есть
            return value
    
    # Если это относительный путь, добавляем префикс API gateway
    if value.startswith("/media/"):
        return f"/api/paintings{value}"
    
    return value


class PaintingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Painting
        fields = [
            "photo",
            "category_id",
            "markers_set_id",
            "colors_amount",
        ]


class PaintingResponseSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    painting_numbered = serializers.SerializerMethodField()
    painting_colored = serializers.SerializerMethodField()

    class Meta:
        model = Painting
        fields = "__all__"

    def get_photo(self, obj):
        return get_media_url(obj.photo.url if obj.photo else None)

    def get_painting_numbered(self, obj):
        return get_media_url(obj.painting_numbered.url if obj.painting_numbered else None)

    def get_painting_colored(self, obj):
        return get_media_url(obj.painting_colored.url if obj.painting_colored else None)


class PublicPaintingSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    painting_numbered = serializers.SerializerMethodField()
    painting_colored = serializers.SerializerMethodField()

    class Meta:
        model = Painting
        fields = [
            "painting_id",
            "user_id",
            "username",
            "photo",
            "painting_numbered",
            "painting_colored",
            "generated_at",
            "category_id",
            "colors_amount",
        ]

    def get_photo(self, obj):
        return get_media_url(obj.photo.url if obj.photo else None)

    def get_painting_numbered(self, obj):
        return get_media_url(obj.painting_numbered.url if obj.painting_numbered else None)

    def get_painting_colored(self, obj):
        return get_media_url(obj.painting_colored.url if obj.painting_colored else None)
