from paintings.services.ml_client import MlClient
from paintings.services.painting_service import PaintingService
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import parsers
from paintings.models import Painting
from paintings.serializers import PaintingCreateSerializer, PaintingResponseSerializer
from paintings.serializers import PublicPaintingSerializer
from paintings.models import Painting
from common.exceptions import ApiException


class PaintingCreateView(APIView):
    parser_classes = [parsers.MultiPartParser, parsers.JSONParser]
    
    def post(self, request):

        user_id = request.headers.get("X-User-Id")
        
        # Преобразуем строковые значения в числа для валидации
        data = request.data.copy() if hasattr(request.data, 'copy') else dict(request.data)
        
        # Преобразуем colors_amount и markers_set_id в числа если они строки
        if 'colors_amount' in data:
            try:
                data['colors_amount'] = int(data['colors_amount'])
            except (ValueError, TypeError):
                pass
        
        if 'markers_set_id' in data and data['markers_set_id']:
            try:
                data['markers_set_id'] = int(data['markers_set_id'])
            except (ValueError, TypeError):
                pass
        
        if 'category_id' in data and data['category_id']:
            try:
                data['category_id'] = int(data['category_id'])
            except (ValueError, TypeError):
                pass

        serializer = PaintingCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        painting = PaintingService.create_painting(
            user_id=user_id,
            validated_data=serializer.validated_data
        )

        try:
            markers_set_id = request.data.get("markers_set_id")
            palette = None
            
            # Получаем палитру из catalog_service по markers_set_id
            if markers_set_id:
                import requests as req
                try:
                    catalog_response = req.get(
                        f"http://catalog-service:8003/catalog/markers-sets/{markers_set_id}/",
                        timeout=5
                    )
                    if catalog_response.status_code == 200:
                        markers_set = catalog_response.json()
                        palette = markers_set.get("colors_data", [])
                except Exception as e:
                    # Если не удалось получить палитру, используем None (дефолтная палитра)
                    print(f"Failed to get markers set: {e}")
                    palette = None
            
            # Если палитра не получена, передаем None - image_processor использует дефолтную PALETTE_OBJECTS
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