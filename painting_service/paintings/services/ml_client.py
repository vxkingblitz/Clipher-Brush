import requests
import json


class MlClient:
    @staticmethod
    def process_painting(painting, palette):
        # Если палитра None, передаем пустой список или None в JSON
        palette_json = json.dumps(palette) if palette is not None else json.dumps(None)
        
        print(f"Sending request to image_processing_service with palette: {palette_json[:100] if palette_json else 'None'}...")
        
        # Проверяем, что файл доступен
        if not painting.photo or not hasattr(painting.photo, 'file'):
            raise Exception("Painting photo file is not available")
        
        try:
            response = requests.post(
                "http://image-processing-service:8004/process/",
                files={
                    "image": painting.photo.file
                },
                data={
                    "palette": palette_json
                },
                timeout=120
            )
            
            print(f"Image processing service response status: {response.status_code}")
            print(f"Image processing service response: {response.text[:200]}")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request to image_processing_service failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response status: {e.response.status_code}")
                print(f"Response text: {e.response.text}")
            raise
