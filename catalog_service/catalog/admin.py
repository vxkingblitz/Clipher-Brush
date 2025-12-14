from django.contrib import admin
from .models import Category, MarkersSet


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("category_id", "name")


@admin.register(MarkersSet)
class MarkersSetAdmin(admin.ModelAdmin):
    list_display = ("markers_set_id", "brand_name", "colors_amount")
