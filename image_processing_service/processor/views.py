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

        if not image or not palette_raw:
            return success_response(
                {"error": "image and palette are required"},
                status=400
            )

        palette = json.loads(palette_raw)

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
