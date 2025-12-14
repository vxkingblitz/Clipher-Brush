from rest_framework.views import APIView
from rest_framework.response import Response
from services.user_service import UserService
from services.jwt_service import JwtService
from common.exceptions import ApiException


class TelegramAuthView(APIView):
    def post(self, request):
        init_data = request.data.get("init_data")
        if not init_data:
            raise ApiException(
                "Validation error",
                "init_data is required",
                400
            )

        try:
            user = UserService.get_or_create_user(init_data)
        except Exception:
            raise ApiException(
                "Auth error",
                "Invalid telegram data",
                401
            )

        token = JwtService.generate_token(user.user_id)

        return Response({
            "access_token": token,
            "user_id": user.user_id
        })
