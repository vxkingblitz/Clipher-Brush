import json
import os
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from django.conf import settings
from .image_processor import run_image_processing
from common.responses import success_response


class ProcessImageView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        image = request.FILES.get("image")
        palette_raw = request.data.get("palette")

        if not image:
            return success_response(
                {"error": "image is required"},
                status=400
            )

        # Палитра может быть None (используется дефолтная)
        palette = None
        if palette_raw:
            try:
                palette_parsed = json.loads(palette_raw)
                # Если это не None и не пустой список, используем его
                if palette_parsed is not None:
                    palette = palette_parsed
            except json.JSONDecodeError as e:
                print(f"Error parsing palette JSON: {e}, palette_raw: {palette_raw}")
                # Если ошибка парсинга, используем None (дефолтная палитра)
                palette = None
        
        print(f"Processing image: {image.name}, palette: {len(palette) if palette else 'default (None)'}")

        input_path = settings.MEDIA_ROOT / "input" / image.name
        os.makedirs(input_path.parent, exist_ok=True)

        with open(input_path, "wb+") as f:
            for chunk in image.chunks():
                f.write(chunk)

        result = run_image_processing(
            input_image_path=str(input_path),
            palette_objects=palette,
            output_dir=str(settings.MEDIA_ROOT / "output")
        )

        return success_response(result, status=201)
