import os
import uuid

from .web_colors_impruved import process_image


def run_image_processing(
    input_image_path: str,
    palette_objects: list,
    output_dir: str,
    max_colors: int = None,
    scale_max: int = None
) -> dict:
    """
    Запускает обработку изображения для создания раскраски по номерам.
    
    Args:
        input_image_path: Путь к входному изображению
        palette_objects: Список объектов палитры с полями 'id', 'colorHex', 'code'
        output_dir: Директория для сохранения результатов
        max_colors: Максимальное количество цветов (опционально)
        scale_max: Максимальный размер стороны изображения (опционально)
    
    Returns:
        dict: Словарь с job_id и путями к созданным файлам
    """
    job_id = str(uuid.uuid4())
    job_dir = os.path.join(output_dir, job_id)
    os.makedirs(job_dir, exist_ok=True)

    numbered_path = os.path.join(job_dir, "numbered.png")
    colored_path = os.path.join(job_dir, "colored.png")
    legend_path = os.path.join(job_dir, "legend.jpg")

    result = process_image(
        input_image_path=input_image_path,
        output_numbered_path=numbered_path,
        output_colored_path=colored_path,
        output_legend_path=legend_path,
        palette_objects=palette_objects,
        max_colors=max_colors,
        scale_max=scale_max
    )

    return {
        "job_id": job_id,
        "numbered_image": result["numbered_image"],
        "colored_image": result["colored_image"],
        "legend_image": result["legend_image"],
    }
