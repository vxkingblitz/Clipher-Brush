import cv2
import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial import KDTree
from PIL import Image, ImageDraw, ImageFont
import math


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def process_image(
    input_image_path: str,
    output_numbered_path: str,
    output_colored_path: str,
    output_legend_path: str,
    palette_objects: list
):
    # ===== PALETTE =====
    palette_rgb = [
        hex_to_rgb(color["hex"] if "hex" in color else color["colorHex"])
        for color in palette_objects
    ]

    palette_codes = [
        color.get("code", str(color["id"]))
        for color in palette_objects
    ]

    # ===== LOAD IMAGE =====
    image = cv2.imread(input_image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    h, w, _ = image_rgb.shape
    pixels = image_rgb.reshape((-1, 3))

    # ===== KMEANS =====
    kmeans = KMeans(n_clusters=len(palette_rgb), random_state=42)
    labels = kmeans.fit_predict(pixels)

    centers = kmeans.cluster_centers_

    # ===== MAP TO PALETTE =====
    tree = KDTree(palette_rgb)
    _, palette_indices = tree.query(centers)

    mapped_colors = np.array([palette_rgb[i] for i in palette_indices])
    mapped_codes = [palette_codes[i] for i in palette_indices]

    recolored_pixels = mapped_colors[labels]
    recolored_image = recolored_pixels.reshape((h, w, 3)).astype(np.uint8)

    # ===== CREATE NUMBERED IMAGE =====
    gray = cv2.cvtColor(recolored_image, cv2.COLOR_RGB2GRAY)
    numbered_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)

    step = max(30, min(h, w) // 20)

    for y in range(0, h, step):
        for x in range(0, w, step):
            label = labels[y * w + x]
            code = mapped_codes[label]
            cv2.putText(
                numbered_image,
                code,
                (x + 5, y + 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 0),
                1,
                cv2.LINE_AA,
            )

    # ===== SAVE IMAGES =====
    cv2.imwrite(output_numbered_path, cv2.cvtColor(numbered_image, cv2.COLOR_RGB2BGR))
    cv2.imwrite(output_colored_path, cv2.cvtColor(recolored_image, cv2.COLOR_RGB2BGR))

    # ===== LEGEND =====
    legend_height = 50 * len(palette_rgb)
    legend = Image.new("RGB", (300, legend_height), "white")
    draw = ImageDraw.Draw(legend)

    for i, (rgb, code) in enumerate(zip(palette_rgb, palette_codes)):
        y = i * 50
        draw.rectangle([10, y + 10, 40, y + 40], fill=rgb)
        draw.text((60, y + 15), f"{code}", fill="black")

    legend.save(output_legend_path)
