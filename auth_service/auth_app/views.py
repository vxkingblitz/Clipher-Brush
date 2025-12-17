from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from services.user_service import UserService
from services.jwt_service import JwtService
from common.exceptions import ApiException

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name="dispatch")
class TelegramAuthView(APIView):
    permission_classes = [AllowAny]

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


@method_decorator(csrf_exempt, name="dispatch")
class UserDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id):
        user = UserService.get_user_by_id(user_id)
        if not user:
            raise ApiException(
                "Not found",
                "User not found",
                404
            )

        return Response({
            "user_id": user.user_id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "photo_url": user.photo_url,
        })
