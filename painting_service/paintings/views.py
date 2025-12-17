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
        
        # Логируем что пришло
        print(f"Request data keys: {list(request.data.keys())}")
        print(f"Request FILES keys: {list(request.FILES.keys()) if hasattr(request, 'FILES') else 'No FILES'}")
        print(f"Content-Type: {request.META.get('CONTENT_TYPE', 'Not set')}")
        
        # Преобразуем строковые значения в числа для валидации
        data = request.data.copy() if hasattr(request.data, 'copy') else dict(request.data)
        
        # Преобразуем colors_amount и markers_set_id в числа если они строки
        if 'colors_amount' in data:
            try:
                data['colors_amount'] = int(data['colors_amount'])
            except (ValueError, TypeError) as e:
                print(f"Error converting colors_amount: {e}, value: {data.get('colors_amount')}")
        
        if 'markers_set_id' in data:
            markers_set_id_val = data['markers_set_id']
            # Обрабатываем случаи: None, 'undefined', '', 0, пустой список
            if not markers_set_id_val or markers_set_id_val == 'undefined' or markers_set_id_val == '':
                data['markers_set_id'] = None
            else:
                try:
                    # Если это список (QueryDict), берем первый элемент
                    if isinstance(markers_set_id_val, list):
                        markers_set_id_val = markers_set_id_val[0] if markers_set_id_val else None
                    
                    if markers_set_id_val and markers_set_id_val != 'undefined' and markers_set_id_val != '':
                        markers_set_id = int(markers_set_id_val)
                        data['markers_set_id'] = markers_set_id if markers_set_id > 0 else None
                    else:
                        data['markers_set_id'] = None
                except (ValueError, TypeError) as e:
                    print(f"Error converting markers_set_id: {e}, value: {markers_set_id_val}")
                    data['markers_set_id'] = None
        
        if 'category_id' in data:
            category_id_val = data['category_id']
            # Обрабатываем случаи: None, 'undefined', '', 0, пустой список
            if not category_id_val or category_id_val == 'undefined' or category_id_val == '':
                data['category_id'] = None
            else:
                try:
                    # Если это список (QueryDict), берем первый элемент
                    if isinstance(category_id_val, list):
                        category_id_val = category_id_val[0] if category_id_val else None
                    
                    if category_id_val and category_id_val != 'undefined' and category_id_val != '':
                        category_id = int(category_id_val)
                        data['category_id'] = category_id if category_id > 0 else None
                    else:
                        data['category_id'] = None
                except (ValueError, TypeError) as e:
                    print(f"Error converting category_id: {e}, value: {category_id_val}")
                    data['category_id'] = None

        print(f"Processed data: {data}")
        print(f"Photo in data: {'photo' in data}")
        print(f"Photo in FILES: {'photo' in request.FILES if hasattr(request, 'FILES') else False}")

        serializer = PaintingCreateSerializer(data=data)
        if not serializer.is_valid():
            # Логируем ошибки валидации для отладки
            print(f"Validation errors: {serializer.errors}")
            print(f"Received data: {data}")
            from rest_framework.exceptions import ValidationError
            raise ValidationError(serializer.errors)

        painting = PaintingService.create_painting(
            user_id=user_id,
            validated_data=serializer.validated_data
        )

        try:
            markers_set_id = data.get("markers_set_id")  # Используем обработанные данные
            palette = None
            
            # Получаем палитру из catalog_service по markers_set_id
            if markers_set_id and markers_set_id != 'undefined':
                import requests as req
                try:
                    catalog_response = req.get(
                        f"http://catalog-service:8003/catalog/markers-sets/{markers_set_id}/",
                        timeout=5
                    )
                    if catalog_response.status_code == 200:
                        markers_set = catalog_response.json()
                        palette = markers_set.get("colors_data", [])
                        print(f"Loaded palette from markers_set_id {markers_set_id}: {len(palette)} colors")
                    else:
                        print(f"Failed to get markers set: status {catalog_response.status_code}")
                except Exception as e:
                    # Если не удалось получить палитру, используем None (дефолтная палитра)
                    print(f"Failed to get markers set: {e}")
                    palette = None
            else:
                print("No markers_set_id provided, using default palette")
            
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