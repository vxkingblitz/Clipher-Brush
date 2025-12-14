import json
from .telegram_auth import TelegramAuthService
from auth_app.models import User


class UserService:

    @staticmethod
    def get_or_create_user(init_data: str) -> User:
        validated_data = TelegramAuthService.validate_init_data(init_data)

        user_data = json.loads(validated_data["user"])

        user, _ = User.objects.update_or_create(
            telegram_id=user_data["id"],
            defaults={
                "username": user_data.get("username"),
                "first_name": user_data.get("first_name"),
                "last_name": user_data.get("last_name"),
                "photo_url": user_data.get("photo_url"),
            }
        )

        return user
