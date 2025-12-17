from paintings.models import Painting


class PaintingService:
    @staticmethod
    def create_painting(user_id, validated_data):
        painting = Painting.objects.create(
            user_id=user_id,
            photo=validated_data["photo"],
            category_id=validated_data.get("category_id"),
            markers_set_id=validated_data.get("markers_set_id"),
            colors_amount=validated_data["colors_amount"],
            status="pending",
            is_public=True,  # По умолчанию публикуем в ленту
        )
        return painting
