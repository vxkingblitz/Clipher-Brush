import os
import uuid
import cv2

from .web_colors_impruved import process_image


def run_image_processing(
    input_image_path: str,
    palette_objects: list,
    output_dir: str
) -> dict:
    job_id = str(uuid.uuid4())
    job_dir = os.path.join(output_dir, job_id)
    os.makedirs(job_dir, exist_ok=True)

    numbered_path = os.path.join(job_dir, "numbered.png")
    colored_path = os.path.join(job_dir, "colored.png")
    legend_path = os.path.join(job_dir, "legend.jpg")

    process_image(
        input_image_path=input_image_path,
        output_numbered_path=numbered_path,
        output_colored_path=colored_path,
        output_legend_path=legend_path,
        palette_objects=palette_objects
    )

    return {
        "job_id": job_id,
        "numbered_image": numbered_path,
        "colored_image": colored_path,
        "legend_image": legend_path,
    }
