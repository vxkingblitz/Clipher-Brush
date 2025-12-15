import json
from auth_app.models import User
from .telegram_auth_service import TelegramAuthService


class UserService:

    @staticmethod
    def get_or_create_user(init_data: str) -> User:
        validated = TelegramAuthService.validate_init_data(init_data)
        user_data = json.loads(validated["user"])

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
