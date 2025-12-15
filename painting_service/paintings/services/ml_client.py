import requests
import json


class MlClient:
    @staticmethod
    def process_painting(painting, palette):
        response = requests.post(
            "http://image_processing_service:8000/process/",
            files={
                "image": painting.photo.file
            },
            data={
                "palette": json.dumps(palette)
            },
            timeout=120
        )

        response.raise_for_status()
        return response.json()
