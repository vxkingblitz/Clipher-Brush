import jwt
from datetime import datetime, timedelta
from django.conf import settings


class JwtService:
    @staticmethod
    def generate_token(user_id: int) -> str:
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(days=7),
        }
        return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")
