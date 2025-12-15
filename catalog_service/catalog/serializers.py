from rest_framework import serializers
from .models import Category, MarkersSet


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["category_id", "name"]


class MarkersSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarkersSet
        fields = [
            "markers_set_id",
            "colors_amount",
            "brand_name",
            "colors_data",
        ]
