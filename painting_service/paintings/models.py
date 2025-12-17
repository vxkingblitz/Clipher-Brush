from django.db import models


class Painting(models.Model):
    painting_id = models.BigAutoField(primary_key=True)

    user_id = models.BigIntegerField()
    username = models.CharField(max_length=255, null=True, blank=True)

    photo = models.ImageField(upload_to="original/")
    painting_numbered = models.ImageField(
        upload_to="numbered/",
        null=True,
        blank=True
    )
    painting_colored = models.ImageField(
        upload_to="colored/",
        null=True,
        blank=True
    )

    generated_at = models.DateTimeField(auto_now_add=True)

    category_id = models.IntegerField(null=True, blank=True)

    is_public = models.BooleanField(default=False)
    is_saved = models.BooleanField(default=False)

    markers_set_id = models.IntegerField(null=True, blank=True)
    colors_amount = models.IntegerField()

    status = models.CharField(
        max_length=32,
        default="pending"
    )

    class Meta:
        db_table = "paintings"
