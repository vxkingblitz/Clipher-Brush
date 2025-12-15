from rest_framework import serializers
from .models import Painting


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
    class Meta:
        model = Painting
        fields = "__all__"


class PublicPaintingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Painting
        fields = [
            "painting_id",
            "user_id",
            "painting_numbered",
            "painting_colored",
            "generated_at",
            "category_id",
            "colors_amount",
        ]
