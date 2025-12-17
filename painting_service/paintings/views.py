from paintings.services.ml_client import MlClient
from paintings.services.painting_service import PaintingService
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from paintings.models import Painting
from paintings.serializers import PaintingCreateSerializer, PaintingResponseSerializer
from paintings.serializers import PublicPaintingSerializer
from paintings.models import Painting
from common.exceptions import ApiException


class PaintingCreateView(APIView):
    def post(self, request):
        user_id = request.headers.get("X-User-Id")

        serializer = PaintingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        painting = PaintingService.create_painting(
            user_id=user_id,
            validated_data=serializer.validated_data
        )

        try:
            palette = request.data.get("palette")
            result = MlClient.process_painting(painting, palette)

            painting.painting_numbered = result["numbered_image"]
            painting.painting_colored = result["colored_image"]
            painting.status = "completed"
            painting.save()

        except Exception:
            painting.status = "failed"
            painting.save()

        return Response(
            PaintingResponseSerializer(painting).data,
            status=201
        )


class PublicPaintingFeedView(ListAPIView):
    serializer_class = PublicPaintingSerializer

    def get_queryset(self):
        return (
            Painting.objects
            .filter(is_public=True, status="completed")
            .order_by("-generated_at")
        )


class PublicPaintingDetailView(RetrieveAPIView):
    serializer_class = PublicPaintingSerializer
    lookup_field = "painting_id"

    def get_queryset(self):
        return Painting.objects.filter(is_public=True)
    

class PublishPaintingView(APIView):
    def post(self, request, painting_id):
        user_id = request.headers.get("X-User-Id")

        try:
            painting = Painting.objects.get(
                painting_id=painting_id,
                user_id=user_id
            )
        except Painting.DoesNotExist:
            raise ApiException(
                "Not found",
                "Painting not found or access denied",
                404
            )

        painting.is_public = True
        painting.save()

        return Response({"status": "published"})


class SavePaintingView(APIView):
    def post(self, request, painting_id):
        user_id = request.headers.get("X-User-id")

        try:
            painting = Painting.objects.get(
                painting_id=painting_id,
                user_id=user_id
            )
        except Painting.DoesNotExist:
            raise ApiException(
                "Not found",
                "Painting not found",
                404
            )
        
        painting.is_saved = not painting.is_saved
        painting.save()

        return Response({
            "painting_od": painting.painting_id,
            "is_saved": painting.is_saved
        })


class MyPaintgsListView(ListAPIView):
    serializer_class = PaintingResponseSerializer

    def get_queryset(self):
        user_id = self.request.headers.get("X-User-Id")
        return Painting.objects.filter(user_id=user_id).order_by("-generated_at")
    

class PaintingDetailView(APIView):
    def get(self, requet, painting_id):
        user_id = requet.headers.get("X-User-id")

        try:
            painting = Painting.objects.get(
                painting_id=painting_id,
                user_id=user_id
            )
        except Painting.DoesNotExist:
            raise ApiException(
                "Not found",
                "Painting not found",
                404
            )
        
        return Response(
            PaintingResponseSerializer(painting).data
        )