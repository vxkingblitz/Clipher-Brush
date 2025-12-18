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
        username = request.headers.get("X-Username")
        
        print(f"PaintingCreateView: Received user_id={user_id}, username={username}")
        
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
            username=username,
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
            
            print(f"Calling MlClient.process_painting with palette: {palette is not None}")
            # Если палитра не получена, передаем None - image_processor использует дефолтную PALETTE_OBJECTS
            result = MlClient.process_painting(painting, palette)
            print(f"ML processing result: {result}")

            # Скачиваем файлы из image_processing_service через HTTP
            # image_processing_service возвращает пути внутри своего контейнера,
            # нужно скачать файлы через HTTP endpoint или использовать общий volume
            import os
            import requests as req
            from django.core.files.base import ContentFile
            from django.conf import settings
            
            numbered_path = result.get("numbered_image")
            colored_path = result.get("colored_image")
            job_id = result.get("job_id")
            
            print(f"Trying to access files: numbered={numbered_path}, colored={colored_path}, job_id={job_id}")
            
            # Пробуем скачать файлы через HTTP endpoint image_processing_service
            # Или используем общий путь, если volume настроен
            base_url = "http://image-processing-service:8004"
            
            # Скачиваем numbered image
            if numbered_path and job_id:
                try:
                    # Пробуем скачать через HTTP endpoint (если он есть) или использовать общий путь
                    # Сначала пробуем прямой доступ к файлу (если volume общий)
                    if os.path.exists(numbered_path):
                        print(f"File exists locally: {numbered_path}")
                        with open(numbered_path, 'rb') as f:
                            file_name = f"numbered_{painting.painting_id}.png"
                            painting.painting_numbered.save(
                                file_name,
                                ContentFile(f.read()),
                                save=True
                            )
                            print(f"Saved numbered image to: {painting.painting_numbered.path}")
                    else:
                        # Файл находится в общем volume image_processing_service
                        # Путь в image_processing_service: /app/media/output/{job_id}/numbered.png
                        # В painting_service доступен как: /shared_media/output/{job_id}/numbered.png
                        print(f"File not found locally, trying shared volume path...")
                        # Извлекаем относительный путь от MEDIA_ROOT image_processing_service
                        # numbered_path может быть: /app/media/output/{job_id}/numbered.png
                        # Нужно получить: output/{job_id}/numbered.png
                        if '/media/' in numbered_path:
                            relative_path = numbered_path.split('/media/')[1]
                            alt_path = f"/shared_media/{relative_path}"
                        else:
                            # Если путь уже относительный или другой формат
                            alt_path = f"/shared_media/output/{job_id}/numbered.png"
                        
                        print(f"Trying shared volume path: {alt_path}")
                        if os.path.exists(alt_path):
                            with open(alt_path, 'rb') as f:
                                file_name = f"numbered_{painting.painting_id}.png"
                                painting.painting_numbered.save(
                                    file_name,
                                    ContentFile(f.read()),
                                    save=True
                                )
                                print(f"Saved numbered image to: {painting.painting_numbered.path}")
                        else:
                            raise Exception(f"Numbered image not accessible. Tried: {numbered_path}, {alt_path}")
                except Exception as e:
                    print(f"Error saving numbered image: {e}")
                    import traceback
                    print(traceback.format_exc())
                    raise
            
            # Скачиваем colored image
            if colored_path and job_id:
                try:
                    if os.path.exists(colored_path):
                        print(f"File exists locally: {colored_path}")
                        with open(colored_path, 'rb') as f:
                            file_name = f"colored_{painting.painting_id}.png"
                            painting.painting_colored.save(
                                file_name,
                                ContentFile(f.read()),
                                save=True
                            )
                            print(f"Saved colored image to: {painting.painting_colored.path}")
                    else:
                        # Аналогично для colored image
                        if '/media/' in colored_path:
                            relative_path = colored_path.split('/media/')[1]
                            alt_path = f"/shared_media/{relative_path}"
                        else:
                            alt_path = f"/shared_media/output/{job_id}/colored.png"
                        
                        print(f"Trying shared volume path: {alt_path}")
                        if os.path.exists(alt_path):
                            with open(alt_path, 'rb') as f:
                                file_name = f"colored_{painting.painting_id}.png"
                                painting.painting_colored.save(
                                    file_name,
                                    ContentFile(f.read()),
                                    save=True
                                )
                                print(f"Saved colored image to: {painting.painting_colored.path}")
                        else:
                            raise Exception(f"Colored image not accessible. Tried: {colored_path}, {alt_path}")
                except Exception as e:
                    print(f"Error saving colored image: {e}")
                    import traceback
                    print(traceback.format_exc())
                    raise
            
            painting.status = "completed"
            painting.save()
            print(f"Painting {painting.painting_id} saved. Numbered: {painting.painting_numbered.name if painting.painting_numbered else 'None'}, Colored: {painting.painting_colored.name if painting.painting_colored else 'None'}")
            print(f"Painting {painting.painting_id} successfully processed")

        except Exception as e:
            import traceback
            print(f"Error processing painting {painting.painting_id}: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            painting.status = "failed"
            painting.save()

        return Response(
            PaintingResponseSerializer(painting).data,
            status=201
        )


class PublicPaintingFeedView(ListAPIView):
    serializer_class = PublicPaintingSerializer

    def get_queryset(self):
        queryset = Painting.objects.filter(
            is_public=True, 
            status="completed"
        )
        
        # Фильтрация по category_id если передан
        category_id = self.request.query_params.get('category_id')
        if category_id:
            try:
                category_id = int(category_id)
                if category_id > 0:
                    queryset = queryset.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass  # Если не удалось преобразовать, игнорируем фильтр
        
        return queryset.order_by("-generated_at")


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

        # Обрабатываем category_id если он передан
        if 'category_id' in request.data:
            category_id_val = request.data.get('category_id')
            if category_id_val and category_id_val != 'undefined' and category_id_val != '':
                try:
                    category_id = int(category_id_val)
                    if category_id > 0:
                        painting.category_id = category_id
                except (ValueError, TypeError):
                    pass  # Если не удалось преобразовать, оставляем текущее значение

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
        queryset = Painting.objects.filter(user_id=user_id)
        
        # Фильтрация по is_saved если передан параметр saved_only
        saved_only = self.request.query_params.get('saved_only')
        if saved_only and saved_only.lower() == 'true':
            queryset = queryset.filter(is_saved=True)
        
        return queryset.order_by("-generated_at")
    

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