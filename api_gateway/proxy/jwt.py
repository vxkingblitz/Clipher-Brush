import jwt
from django.conf import settings
from common.exceptions import ApiException


class JwtMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/auth/"):
            return self.get_response(request)

        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            raise ApiException(
                title="Authorization error",
                description="Authorization header missing",
                status=401
            )

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=["HS256"]
            )
            request.user_id = payload["user_id"]
        except jwt.ExpiredSignatureError:
            raise ApiException(
                title="Authorization error",
                description="Token expired",
                status=401
            )
        except jwt.InvalidTokenError:
            raise ApiException(
                title="Authorization error",
                description="Invalid token",
                status=401
            )

        return self.get_response(request)
