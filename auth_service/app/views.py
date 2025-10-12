from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth import authenticate
from auth_app.models import User, UserSession
from auth_app.serializers import TelegramAuthSerializer, UserSerializer, UserProfileSerializer
import secrets

class HealthView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        return Response({
            "status": "healthy", 
            "service": "auth",
            "version": "1.0.0"
        })

class TelegramAuthView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = TelegramAuthSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {"error": "Invalid data", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        telegram_data = serializer.validated_data
        telegram_id = telegram_data['id']
        
        try:
            user = User.objects.get(telegram_id=telegram_id)
            created = False
            
            if telegram_data.get('username') and user.username != telegram_data['username']:
                user.username = telegram_data['username']
            if telegram_data.get('first_name') and user.first_name != telegram_data['first_name']:
                user.first_name = telegram_data['first_name']
            if telegram_data.get('last_name') and user.last_name != telegram_data['last_name']:
                user.last_name = telegram_data['last_name']
            user.save()
            
        except User.DoesNotExist:
            user = User.objects.create(
                telegram_id=telegram_id,
                username=telegram_data.get('username', ''),
                first_name=telegram_data.get('first_name', ''),
                last_name=telegram_data.get('last_name', ''),
                # Для Telegram auth пароль не нужен, но Django требует
                password=f"telegram_{telegram_id}_{secrets.token_urlsafe(16)}"
            )
            created = True
        
        refresh = RefreshToken.for_user(user)
        
        session_token = secrets.token_urlsafe(32)
        UserSession.objects.create(
            user=user,
            session_token=session_token
        )
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'session_token': session_token,
            'created': created
        }, status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
    def patch(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpgradePlanView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        
        if user.plan_type == User.PLAN_PRO:
            return Response(
                {"error": "User already has PRO plan"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.plan_type = User.PLAN_PRO
        user.save()
        
        return Response({
            "message": "Plan upgraded to PRO successfully",
            "user": UserSerializer(user).data
        })

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        UserSession.objects.filter(user=request.user, is_active=True).update(is_active=False)
        
        # Для JWT клиент должен удалить токен на своей стороне
        return Response({"message": "Logged out successfully"})

class ValidateSessionView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        session_token = request.data.get('session_token')
        
        if not session_token:
            return Response(
                {"error": "session_token is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            session = UserSession.objects.get(
                session_token=session_token,
                is_active=True
            )
            
            if session.is_expired():
                session.is_active = False
                session.save()
                return Response(
                    {"error": "Session expired"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            session.save()
            
            return Response({
                "valid": True,
                "user": UserSerializer(session.user).data
            })
            
        except UserSession.DoesNotExist:
            return Response(
                {"error": "Invalid session token"},
                status=status.HTTP_401_UNAUTHORIZED
            )