PALETTE_OBJECTS = []


import os
import math
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
from sklearn.cluster import MiniBatchKMeans
from scipy.interpolate import splprep, splev
from scipy.spatial import cKDTree

# ================== ПАРАМЕТРЫ ПО УМОЛЧАНИЮ ==================
DEFAULT_SLIC_SEGMENTS = 70000
DEFAULT_SLIC_COMPACTNESS = 0.2
DEFAULT_MIN_REGION_AREA = 550 
DEFAULT_LINE_COLOR = (230, 230, 230)
DEFAULT_LINE_THICKNESS = 1
DEFAULT_SCALE_MAX = 3000
DEFAULT_MAX_COLORS = 20
DEFAULT_COLOR_TRESHHOLD = 50

# ================== УТИЛИТЫ ==================
def resize_max_side(img, max_side):
    h, w = img.shape[:2]
    if max(h, w) <= max_side:
        return img
    scale = max_side / max(h, w)
    return cv2.resize(img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)

def hex_to_bgr(hex_str):
    h = hex_str.lstrip("#")
    if len(h) == 3:
        h = "".join([c*2 for c in h])
    r = int(h[0:2],16)
    g = int(h[2:4],16)
    b = int(h[4:6],16)
    return (b,g,r)

def extract_dominant_colors(image, n_colors, color_threshold=DEFAULT_COLOR_TRESHHOLD):
    pixels = image.reshape(-1, 3)
    sample_size = min(5000, len(pixels))
    indices = np.random.choice(len(pixels), sample_size, replace=False)
    sample_pixels = pixels[indices]

    kmeans = MiniBatchKMeans(n_clusters=min(n_colors * 2, 50), random_state=42, batch_size=512)
    kmeans.fit(sample_pixels)
    colors = kmeans.cluster_centers_.astype(np.int16)

    dist_matrix = np.sqrt(((colors[:, None, :] - colors[None, :, :]) ** 2).sum(axis=2))
    merged_colors = []
    used = np.zeros(len(colors), dtype=bool)

    for i in range(len(colors)):
        if used[i]:
            continue
        group = np.where((dist_matrix[i] <= color_threshold) & (~used))[0]
        used[group] = True
        merged_colors.append(colors[group].mean(axis=0).astype(int))

    if len(merged_colors) > n_colors:
        labels = kmeans.labels_
        weights = [np.sum(np.isin(labels, np.where(dist_matrix[i] <= color_threshold)[0])) for i in range(len(merged_colors))]
        top_idx = np.argsort(weights)[-n_colors:]
        merged_colors = [merged_colors[i] for i in top_idx]

    return [tuple(c) for c in merged_colors]

def find_closest_palette_colors(dominant_colors, palette_objects):
    palette_bgr = np.array([hex_to_bgr(obj['colorHex']) for obj in palette_objects], dtype=np.int16)
    tree = cKDTree(palette_bgr)

    dom_arr = np.array(dominant_colors, dtype=np.int16)
    _, idxs = tree.query(dom_arr, k=1)

    result_colors = [tuple(palette_bgr[i]) for i in idxs]
    result_objects = [palette_objects[i] for i in idxs]
    result_codes = [palette_objects[i]['code'] for i in idxs]

    return result_colors, result_objects, result_codes

def find_best_neighbor(idx_img, comp_mask, exclude_color, max_iter=6):
    kernel = np.ones((3,3), np.uint8)
    comp_mask = comp_mask.astype(np.uint8)

    for it in range(1, max_iter+1):
        dil = cv2.dilate(comp_mask, kernel, iterations=it)
        border = (dil.astype(bool)) & (~comp_mask.astype(bool))
        if not np.any(border):
            continue

        neighbor_vals = idx_img[border]
        neighbor_vals = neighbor_vals[neighbor_vals != exclude_color]
        if neighbor_vals.size > 0:
            best = np.bincount(neighbor_vals).argmax()
            return int(best)
    return None

def reassign_small_regions(idx_img, num_colors, min_area):
    h, w = idx_img.shape
    clean = idx_img.copy()

    for color in np.unique(idx_img):
        mask = (idx_img == color).astype(np.uint8)
        if mask.sum() == 0:
            continue

        n_comp, labels_cc, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
        for lab in range(1, n_comp):
            area = stats[lab, cv2.CC_STAT_AREA]
            if area < min_area:
                comp_mask = (labels_cc == lab)
                best_neigh = find_best_neighbor(idx_img, comp_mask, exclude_color=color, max_iter=6)
                if best_neigh is not None:
                    clean[comp_mask] = best_neigh
                else:
                    vals, cnts = np.unique(idx_img, return_counts=True)
                    vals = vals[vals != color]
                    if vals.size > 0:
                        clean[comp_mask] = vals[np.argmax(cnts[vals != color])]
    return clean

def draw_spline_contours(sub_idx, color_img, line_color=(0,0,0), thickness=1):
    h, w = sub_idx.shape
    out_line = np.full_like(color_img, 255)
    out_color = color_img.copy()

    for uid in np.unique(sub_idx):
        if uid < 0: continue
        mask = (sub_idx == uid).astype(np.uint8)
        contours,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours: continue

        for cnt in contours:
            if len(cnt) < 5:
                cv2.fillPoly(out_color, [cnt], (200,200,200))
                continue
            pts = cnt[:,0,:].astype(np.float32)
            fill_color = tuple(map(int, color_img[mask>0][0])) if mask.any() else (200,200,200)
            
            # Ограничиваем размер контура для больших изображений (предотвращаем проблемы с памятью)
            MAX_CONTOUR_POINTS = 5000
            if len(pts) > MAX_CONTOUR_POINTS:
                # Упрощаем контур, используя approxPolyDP для уменьшения количества точек
                epsilon = 0.02 * cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, epsilon, True)
                pts = cnt[:,0,:].astype(np.float32)
                # Если все еще слишком много точек, просто рисуем без сплайна
                if len(pts) > MAX_CONTOUR_POINTS:
                    cv2.fillPoly(out_color, [cnt], fill_color)
                    cv2.polylines(out_line, [cnt], True, line_color, thickness)
                    continue
            
            try:
                tck,u = splprep([pts[:,0], pts[:,1]], s=0.5, per=True)
                # Ограничиваем количество точек сплайна (максимум 15000 точек)
                spline_points = min(len(pts) * 3, 15000)
                u_new = np.linspace(0, 1, spline_points)
                x_new, y_new = splev(u_new, tck)
                spline_pts = np.stack([x_new, y_new], axis=1).astype(np.int32)
                cv2.fillPoly(out_color, [spline_pts], fill_color)
                cv2.polylines(out_line, [spline_pts], True, line_color, thickness, lineType=cv2.LINE_AA)
            except Exception as e:
                # В случае ошибки просто используем исходный контур
                cv2.fillPoly(out_color, [pts.astype(np.int32)], fill_color)
                cv2.polylines(out_line, [pts.astype(np.int32)], True, line_color, thickness)
    return out_color, out_line

def catmull_rom_spline(P, n_points=100):
    P = np.array(P)
    if len(P) < 2:
        return P

    def tj(ti, Pi, Pj, alpha=0.5):
        return ((np.sum((Pj - Pi)**2))**0.5)**alpha + ti

    t = [0]
    for i in range(1,len(P)):
        t.append(tj(t[i-1], P[i-1], P[i]))
    t = np.array(t)

    curve = []
    for i in range(len(P)-1):
        t0, t1 = t[i], t[i+1]
        p0, p1 = P[i], P[i+1]
        for s in np.linspace(0,1,n_points//(len(P)-1)):
            pt = (1-s)*p0 + s*p1
            curve.append(pt)
    return np.array(curve).astype(np.int32)

def add_global_splines(sub_idx, num_splines=5, thickness=5):
    h, w = sub_idx.shape
    next_sub_id = sub_idx.max() + 1

    for _ in range(num_splines):
        num_pts = np.random.randint(4,7)
        pts = [[np.random.randint(0,w), np.random.randint(0,h)] for _ in range(num_pts)]
        cr_pts = catmull_rom_spline(pts, n_points=300)
        line_mask = np.zeros_like(sub_idx, dtype=np.uint8)
        cv2.polylines(line_mask, [cr_pts], isClosed=False, color=255, thickness=thickness)
        sub_idx[line_mask>0] = next_sub_id
        next_sub_id += 1

    return sub_idx

def create_final_image_with_frame(main_image, frame_thickness=1):
    """Создает финальное изображение только с серой рамкой (без легенды)"""
    # Добавляем серую рамку вокруг основного изображения
    h, w = main_image.shape[:2]
    framed_image = np.full((h + 2*frame_thickness, w + 2*frame_thickness, 3), 
                          fill_value=200, dtype=np.uint8)  # Серый цвет
    framed_image[frame_thickness:frame_thickness+h, 
                frame_thickness:frame_thickness+w] = main_image
    
    return framed_image

def add_legend_to_image(main_image, used_palette_idxs, selected_colors_bgr, map_palette_to_num, font_path=None):
    """Добавляет легенду с цветами внизу изображения"""
    h, w = main_image.shape[:2]
    
    # Параметры легенды
    legend_padding = 15
    frame_thickness = 1
    num_colors = len(used_palette_idxs)
    
    # Адаптивные параметры в зависимости от количества цветов
    if num_colors <= 15:
        # Мало цветов - можно сделать крупнее
        rect_size = max(30, int(h * 0.03))
        items_per_row = min(8, num_colors)
        spacing = 10
        text_font_scale = 0.6
    elif num_colors <= 30:
        # Среднее количество - средний размер
        rect_size = max(25, int(h * 0.025))
        items_per_row = min(10, num_colors)
        spacing = 8
        text_font_scale = 0.5
    elif num_colors <= 50:
        # Много цветов - компактнее
        rect_size = max(20, int(h * 0.02))
        items_per_row = min(12, num_colors)
        spacing = 6
        text_font_scale = 0.45
    else:
        # Очень много цветов - очень компактно
        rect_size = max(18, int(h * 0.018))
        items_per_row = min(15, num_colors)
        spacing = 5
        text_font_scale = 0.4
    
    text_height = int(rect_size * text_font_scale)
    
    # Рассчитываем размеры легенды
    num_rows = (num_colors + items_per_row - 1) // items_per_row
    
    # Ширина одного элемента (квадрат + текст)
    # Для компактного режима уменьшаем ширину текста
    if num_colors > 30:
        legend_item_width = rect_size + 60
    else:
        legend_item_width = rect_size + 80
    
    # Высота легенды
    legend_height = num_rows * (rect_size + text_height + spacing) + 2 * legend_padding
    
    # Создаем новое изображение с легендой внизу
    new_h = h + 2*frame_thickness + legend_height
    new_w = w + 2*frame_thickness
    result_image = np.full((new_h, new_w, 3), fill_value=255, dtype=np.uint8)  # Белый фон
    
    # Добавляем серую рамку вокруг основного изображения
    result_image[frame_thickness:frame_thickness+h, 
                frame_thickness:frame_thickness+w] = main_image
    
    # Рисуем разделительную линию между изображением и легендой
    line_y = frame_thickness + h
    result_image[line_y:line_y+2, frame_thickness:frame_thickness+w] = [200, 200, 200]
    
    # Конвертируем в PIL для рисования текста
    result_pil = Image.fromarray(result_image)
    draw = ImageDraw.Draw(result_pil)
    
    # Шрифт для легенды (адаптивный)
    if num_colors > 50:
        legend_font_size = max(10, int(rect_size * 0.4))
    elif num_colors > 30:
        legend_font_size = max(12, int(rect_size * 0.45))
    else:
        legend_font_size = max(14, int(rect_size * 0.5))
    try:
        if font_path:
            legend_font = ImageFont.truetype(font_path, legend_font_size)
        else:
            legend_font = ImageFont.load_default()
    except:
        legend_font = ImageFont.load_default()
    
    # Рисуем элементы легенды
    legend_start_y = frame_thickness + h + 2 + legend_padding
    
    for i, pal_idx in enumerate(used_palette_idxs):
        row = i // items_per_row
        col = i % items_per_row
        
        # Позиция элемента
        x = frame_thickness + legend_padding + col * (legend_item_width + spacing)
        y = legend_start_y + row * (rect_size + text_height + spacing)
        
        # Цветной квадрат
        b, g, r = selected_colors_bgr[pal_idx]
        draw.rectangle([x, y, x + rect_size, y + rect_size], fill=(r, g, b), outline=(0, 0, 0), width=1)
        
        # Текст рядом с квадратом
        palette_info = map_palette_to_num[pal_idx]
        # Если есть код, показываем "номер - код", иначе только номер
        if 'code' in palette_info:
            text = f"{palette_info['number']} - {palette_info['code']}"
        else:
            text = str(palette_info['number'])
        text_x = x + rect_size + 5
        text_y = y + (rect_size - text_height) // 2
        
        draw.text((text_x, text_y), text, fill=(0, 0, 0), font=legend_font)
    
    # Конвертируем обратно в OpenCV формат
    result_image_bgr = cv2.cvtColor(np.array(result_pil), cv2.COLOR_RGB2BGR)
    
    return result_image_bgr

def create_legend_image(used_palette_idxs, selected_colors_bgr, map_palette_to_num, image_height, font_path=None):
    """Создает отдельное изображение легенды"""
    legend_padding = 10
    rect_size = max(30, int(image_height * 0.03))
    text_height = int(rect_size * 0.8)
    spacing = 5
    
    # Рассчитываем размеры легенды
    items_per_row = min(8, len(used_palette_idxs))  # Максимум 8 элементов в строке
    num_rows = (len(used_palette_idxs) + items_per_row - 1) // items_per_row
    
    legend_item_width = rect_size + 100  # Ширина одного элемента (квадрат + текст)
    legend_width = items_per_row * legend_item_width + (items_per_row - 1) * spacing + 2 * legend_padding
    legend_height = num_rows * (rect_size + text_height + spacing) + 2 * legend_padding
    
    # Создаем изображение для легенды
    legend_image = np.full((legend_height, legend_width, 3), 255, dtype=np.uint8)  # Белый фон
    legend_pil = Image.fromarray(legend_image)
    legend_draw = ImageDraw.Draw(legend_pil)
    
    # Используем меньший шрифт для легенды
    legend_font_size = 22
    try:
        if font_path:
            legend_font = ImageFont.truetype(font_path, legend_font_size)
        else:
            legend_font = ImageFont.load_default()
    except:
        legend_font = ImageFont.load_default()
    
    # Рисуем элементы легенды
    for i, pal_idx in enumerate(used_palette_idxs):
        row = i // items_per_row
        col = i % items_per_row
        
        x = legend_padding + col * (legend_item_width + spacing)
        y = legend_padding + row * (rect_size + text_height + spacing)
        
        # Цветной квадрат
        b, g, r = selected_colors_bgr[pal_idx]
        legend_draw.rectangle([x, y, x + rect_size, y + rect_size], fill=(r, g, b), outline=(0, 0, 0))
        
        # Текст под квадратом
        palette_info = map_palette_to_num[pal_idx]
        # Если есть код, показываем "номер - код", иначе только номер
        if 'code' in palette_info:
            text = f"{palette_info['number']} - {palette_info['code']}"
        else:
            text = str(palette_info['number'])
        text_bbox = legend_draw.textbbox((0, 0), text, font=legend_font)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = x + (rect_size - text_width) // 2
        text_y = y + rect_size + 5
        
        legend_draw.text((text_x, text_y), text, fill=(0, 0, 0), font=legend_font)
    
    # Конвертируем обратно в OpenCV формат
    legend_image_bgr = cv2.cvtColor(np.array(legend_pil), cv2.COLOR_RGB2BGR)
    
    return legend_image_bgr

# ================== MAIN FUNCTION ==================
def process_image(
    input_image_path: str,
    output_numbered_path: str,
    output_colored_path: str,
    output_legend_path: str,
    palette_objects: list = None,
    max_colors: int = None,
    scale_max: int = None,
    slic_segments: int = None,
    slic_compactness: float = None,
    min_region_area: int = None,
    line_color: tuple = None,
    line_thickness: int = None,
    color_threshold: int = None,
    font_path: str = None
):
    """
    Обрабатывает изображение и создает раскраску по номерам.
    
    Args:
        input_image_path: Путь к входному изображению
        output_numbered_path: Путь для сохранения изображения с номерами
        output_colored_path: Путь для сохранения цветного изображения
        output_legend_path: Путь для сохранения легенды
        palette_objects: Список объектов палитры с полями 'id', 'colorHex', 'code'
        max_colors: Максимальное количество цветов (по умолчанию DEFAULT_MAX_COLORS)
        scale_max: Максимальный размер стороны изображения (по умолчанию DEFAULT_SCALE_MAX)
        slic_segments: Количество сегментов для SLIC (по умолчанию DEFAULT_SLIC_SEGMENTS)
        slic_compactness: Компактность SLIC (по умолчанию DEFAULT_SLIC_COMPACTNESS)
        min_region_area: Минимальная площадь региона (по умолчанию DEFAULT_MIN_REGION_AREA)
        line_color: Цвет линий (по умолчанию DEFAULT_LINE_COLOR)
        line_thickness: Толщина линий (по умолчанию DEFAULT_LINE_THICKNESS)
        color_threshold: Порог для объединения цветов (по умолчанию DEFAULT_COLOR_TRESHHOLD)
        font_path: Путь к шрифту (опционально, используется дефолтный если не указан)
    
    Returns:
        dict: Словарь с путями к созданным файлам
    """
    # Используем переданную палитру или дефолтную
    if palette_objects is None:
        palette_objects = PALETTE_OBJECTS
    
    if not palette_objects:
        raise ValueError("palette_objects пуст. Нужно заполнить список словарей с 'colorHex', 'code', 'id'")
    
    # Устанавливаем параметры по умолчанию если не указаны
    max_colors = max_colors or DEFAULT_MAX_COLORS
    scale_max = scale_max or DEFAULT_SCALE_MAX
    slic_segments = slic_segments or DEFAULT_SLIC_SEGMENTS
    slic_compactness = slic_compactness or DEFAULT_SLIC_COMPACTNESS
    min_region_area = min_region_area or DEFAULT_MIN_REGION_AREA
    line_color = line_color or DEFAULT_LINE_COLOR
    line_thickness = line_thickness or DEFAULT_LINE_THICKNESS
    color_threshold = color_threshold or DEFAULT_COLOR_TRESHHOLD
    
    # Загружаем изображение
    img_bgr = cv2.imread(input_image_path)
    if img_bgr is None:
        raise FileNotFoundError(f"File {input_image_path} not found")
    
    img_bgr = resize_max_side(img_bgr, scale_max)
    h, w = img_bgr.shape[:2]
    
    # Адаптивно уменьшаем количество сегментов для больших изображений (предотвращаем проблемы с памятью)
    total_pixels = h * w
    if total_pixels > 5_000_000:  # Если изображение больше 5М пикселей
        # Пропорционально уменьшаем количество сегментов
        scale_factor = 5_000_000 / total_pixels
        slic_segments = max(10000, int(slic_segments * scale_factor))

    # Извлекаем доминирующие цвета
    dominant_colors = extract_dominant_colors(img_bgr, max_colors, color_threshold)
    selected_colors_bgr, selected_objects, _ = find_closest_palette_colors(dominant_colors, palette_objects)
    palette = np.array(selected_colors_bgr, dtype=np.uint8)
    K_COLORS = len(palette)

    # SLIC сегментация
    slic = cv2.ximgproc.createSuperpixelSLIC(
        img_bgr, 
        algorithm=cv2.ximgproc.SLICO,
        region_size=max(5, int(math.sqrt(h * w / max(1, slic_segments)))),
        ruler=float(slic_compactness)
    )
    slic.iterate(10)
    labels_slic = slic.getLabels().astype(np.int32)

    # Цвета суперпикселей
    flat_labels = labels_slic.ravel()
    b = img_bgr[:,:,0].ravel()
    g = img_bgr[:,:,1].ravel()
    r = img_bgr[:,:,2].ravel()
    
    # Безопасное вычисление максимальной метки (избегаем переполнения)
    max_label = int(labels_slic.max())
    num_labels = max_label + 1
    
    # Используем более эффективное вычисление для избежания проблем с памятью
    counts = np.bincount(flat_labels, minlength=num_labels).astype(np.float32)
    counts_safe = np.where(counts == 0, 1.0, counts)
    
    mean_b = np.bincount(flat_labels, weights=b.astype(np.float64), minlength=num_labels) / counts_safe
    mean_g = np.bincount(flat_labels, weights=g.astype(np.float64), minlength=num_labels) / counts_safe
    mean_r = np.bincount(flat_labels, weights=r.astype(np.float64), minlength=num_labels) / counts_safe
    mean_colors = np.stack([mean_b, mean_g, mean_r], axis=1).astype(np.float32)
    
    # Оптимизированное вычисление расстояний (избегаем создания огромного массива)
    palette_float = palette.astype(np.float32)
    best_idx_per_label = np.zeros(num_labels, dtype=np.int32)
    
    # Вычисляем расстояния блоками для экономии памяти
    chunk_size = min(1000, num_labels)  # Обрабатываем по 1000 меток за раз
    for i in range(0, num_labels, chunk_size):
        end_idx = min(i + chunk_size, num_labels)
        chunk_colors = mean_colors[i:end_idx, None, :]  # (chunk_size, 1, 3)
        chunk_diffs = np.linalg.norm(chunk_colors - palette_float[None, :, :], axis=2)  # (chunk_size, K_COLORS)
        best_idx_per_label[i:end_idx] = np.argmin(chunk_diffs, axis=1).astype(np.int32)
    
    idx_img = best_idx_per_label[labels_slic]

    # Переприсваиваем маленькие регионы по палитрам до построения subregion
    clean_idx = reassign_small_regions(idx_img, K_COLORS, min_region_area)
    clean_color_img = palette[clean_idx]

    # Создаем subregion_idx
    subregion_idx = -1 * np.ones_like(clean_idx, dtype=np.int32)
    next_sub_id = 0
    subregion_centroids = {}
    used_palette_idxs = sorted(list(set(clean_idx.flatten())))
    # Проверяем, есть ли коды в палитре (если используется набор маркеров)
    has_codes = any('code' in obj for obj in selected_objects if isinstance(obj, dict))
    map_palette_to_num = {}
    for i, old_idx in enumerate(used_palette_idxs):
        palette_info = {'number': i+1}
        # Добавляем код только если он есть в объекте палитры
        if has_codes and isinstance(selected_objects[old_idx], dict) and 'code' in selected_objects[old_idx]:
            palette_info['code'] = selected_objects[old_idx]['code']
        map_palette_to_num[old_idx] = palette_info

    for pal_idx in used_palette_idxs:
        mask = (clean_idx == pal_idx).astype(np.uint8)
        if mask.sum() == 0:
            continue
        n_comp, labels_cc, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity=8)
        for lab in range(1, n_comp):
            area = stats[lab, cv2.CC_STAT_AREA]
            comp_mask = (labels_cc == lab)
            if area < min_region_area:
                best_neigh = find_best_neighbor(clean_idx, comp_mask, exclude_color=pal_idx, max_iter=6)
                if best_neigh is not None:
                    clean_idx[comp_mask] = best_neigh
                    continue
            subregion_idx[comp_mask] = next_sub_id

            mask_uint8 = (comp_mask).astype(np.uint8)
            if mask_uint8.sum() == 0:
                continue
            if mask_uint8.sum() == 1:
                ys, xs = np.nonzero(mask_uint8)
                cx, cy = int(xs[0]), int(ys[0])
            else:
                dt = cv2.distanceTransform(mask_uint8, distanceType=cv2.DIST_L2, maskSize=5)
                minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(dt)
                if maxVal > 0:
                    cx, cy = int(maxLoc[0]), int(maxLoc[1])
                else:
                    ys, xs = np.nonzero(comp_mask)
                    cx, cy = int(xs.mean()), int(ys.mean())

            subregion_centroids[next_sub_id] = (cx, cy, pal_idx)
            next_sub_id += 1

    # Рисуем сплайновые заливки и линии
    colored_spline_img, line_art_spline = draw_spline_contours(
        subregion_idx, 
        clean_color_img, 
        line_color=line_color, 
        thickness=line_thickness
    )

    # PIL для текста
    numbered_pil = Image.fromarray(cv2.cvtColor(line_art_spline.copy(), cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(numbered_pil)
    font_size = 12
    try:
        if font_path:
            font = ImageFont.truetype(font_path, font_size)
        else:
            font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()

    for sub_id, (cx, cy, pal_idx) in subregion_centroids.items():
        palette_info = map_palette_to_num.get(pal_idx, {'number': 0, 'code': '000'})
        text = str(palette_info['number'])
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        pos = (int(cx - tw//2), int(cy - th//2))
        shadow_pos = (pos[0]+1, pos[1]+1)
        draw.text(shadow_pos, text, fill=(200, 200, 200), font=font)
        draw.text(pos, text, fill=(70, 70, 70), font=font)

    # Создаем отдельное изображение для легенды (для обратной совместимости)
    legend_image = create_legend_image(used_palette_idxs, selected_colors_bgr, map_palette_to_num, h, font_path)
    
    # Создаем финальное изображение с легендой внизу
    main_image_bgr = cv2.cvtColor(np.array(numbered_pil), cv2.COLOR_RGB2BGR)
    # Добавляем легенду прямо внизу изображения с цифрами
    final_image = add_legend_to_image(main_image_bgr, used_palette_idxs, selected_colors_bgr, map_palette_to_num, font_path)
    
    # Создаем директории для выходных файлов если их нет
    os.makedirs(os.path.dirname(output_numbered_path), exist_ok=True)
    os.makedirs(os.path.dirname(output_colored_path), exist_ok=True)
    os.makedirs(os.path.dirname(output_legend_path), exist_ok=True)
    
    # Сохраняем результаты
    cv2.imwrite(output_numbered_path, final_image)
    cv2.imwrite(output_legend_path, legend_image)
    cv2.imwrite(output_colored_path, colored_spline_img)
    
    return {
        "numbered_image": output_numbered_path,
        "colored_image": output_colored_path,
        "legend_image": output_legend_path,
    }