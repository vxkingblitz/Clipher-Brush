from django.db import models


class Category(models.Model):
    category_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "categories"


class MarkersSet(models.Model):
    markers_set_id = models.BigAutoField(primary_key=True)
    colors_amount = models.IntegerField()
    brand_name = models.CharField(max_length=255)
    colors_data = models.JSONField()

    class Meta:
        db_table = "markers_sets"
