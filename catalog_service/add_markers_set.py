#!/usr/bin/env python
"""
Скрипт для добавления набора маркеров GuangNa 120шт в базу данных.
Использует данные из PALETTE_OBJECTS из web_colors_impruved.py
"""

import os
import sys
import django

# Настройка Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'catalog_project.settings')
django.setup()

from catalog.models import MarkersSet

# Данные из web_colors_impruved.py (PALETTE_OBJECTS)
PALETTE_OBJECTS = [
    { 'id': 1, 'colorHex': '#243745', 'code': '688' },
    { 'id': 2, 'colorHex': '#F18233', 'code': '663' },
    { 'id': 3, 'colorHex': '#CDB655', 'code': '652' },
    { 'id': 4, 'colorHex': '#FAC84C', 'code': '802' },
    { 'id': 5, 'colorHex': '#A49752', 'code': '637' },
    { 'id': 6, 'colorHex': '#EDBC8A', 'code': '654' },
    { 'id': 7, 'colorHex': '#FEA54D', 'code': '725' },
    { 'id': 8, 'colorHex': '#328F70', 'code': '728' },
    { 'id': 9, 'colorHex': '#4C5739', 'code': '697' },
    { 'id': 10, 'colorHex': '#3E6968', 'code': '694' },
    { 'id': 11, 'colorHex': '#51682A', 'code': '634' },
    { 'id': 12, 'colorHex': '#395827', 'code': '676' },
    { 'id': 13, 'colorHex': '#235751', 'code': '609' },
    { 'id': 14, 'colorHex': '#825536', 'code': '620' },
    { 'id': 15, 'colorHex': '#3D3D55', 'code': '673' },
    { 'id': 16, 'colorHex': '#4E3752', 'code': '613' },
    { 'id': 17, 'colorHex': '#A75D3A', 'code': '672' },
    { 'id': 18, 'colorHex': '#88515B', 'code': '739' },
    { 'id': 19, 'colorHex': '#805964', 'code': '675' },
    { 'id': 20, 'colorHex': '#39344B', 'code': '678' },
    { 'id': 21, 'colorHex': '#38487D', 'code': '608' },
    { 'id': 22, 'colorHex': '#000000', 'code': '611' },
    { 'id': 23, 'colorHex': '#835F28', 'code': '643' },
    { 'id': 24, 'colorHex': '#283E4F', 'code': '824' },
    { 'id': 25, 'colorHex': '#757B4C', 'code': '741' },
    { 'id': 26, 'colorHex': '#308140', 'code': '740' },
    { 'id': 27, 'colorHex': '#5C7D10', 'code': '687' },
    { 'id': 28, 'colorHex': '#537658', 'code': '622' },
    { 'id': 29, 'colorHex': '#5E8A2C', 'code': '665' },
    { 'id': 30, 'colorHex': '#366962', 'code': '695' },
    { 'id': 31, 'colorHex': '#F2D215', 'code': '615' },
    { 'id': 32, 'colorHex': '#BBA46B', 'code': '638' },
    { 'id': 33, 'colorHex': '#D3B886', 'code': '731' },
    { 'id': 34, 'colorHex': '#E5BE99', 'code': '630' },
    { 'id': 35, 'colorHex': '#F4C570', 'code': '684' },
    { 'id': 36, 'colorHex': '#F3A721', 'code': '604' },
    { 'id': 37, 'colorHex': '#73476C', 'code': '832' },
    { 'id': 38, 'colorHex': '#615387', 'code': '742' },
    { 'id': 39, 'colorHex': '#C9764D', 'code': '619' },
    { 'id': 40, 'colorHex': '#8F4039', 'code': '674' },
    { 'id': 41, 'colorHex': '#9C632B', 'code': '639' },
    { 'id': 42, 'colorHex': '#BA4555', 'code': '671' },
    { 'id': 43, 'colorHex': '#446189', 'code': '650' },
    { 'id': 44, 'colorHex': '#236880', 'code': '616' },
    { 'id': 45, 'colorHex': '#444847', 'code': '693' },
    { 'id': 46, 'colorHex': '#474135', 'code': '680' },
    { 'id': 47, 'colorHex': '#4C3B5F', 'code': '607' },
    { 'id': 48, 'colorHex': '#33435E', 'code': '617' },
    { 'id': 49, 'colorHex': '#3E9159', 'code': '899' },
    { 'id': 50, 'colorHex': '#B0B945', 'code': '735' },
    { 'id': 51, 'colorHex': '#1C9489', 'code': '602' },
    { 'id': 52, 'colorHex': '#A7AD40', 'code': '727' },
    { 'id': 53, 'colorHex': '#57691C', 'code': '682' },
    { 'id': 54, 'colorHex': '#677258', 'code': '690' },
    { 'id': 55, 'colorHex': '#CAAA63', 'code': '645' },
    { 'id': 56, 'colorHex': '#DFA33B', 'code': '649' },
    { 'id': 57, 'colorHex': '#DBB37C', 'code': '625' },
    { 'id': 58, 'colorHex': '#DEB62E', 'code': '656' },
    { 'id': 59, 'colorHex': '#C08954', 'code': '644' },
    { 'id': 60, 'colorHex': '#EBC913', 'code': '603' },
    { 'id': 61, 'colorHex': '#3E888B', 'code': '820' },
    { 'id': 62, 'colorHex': '#637292', 'code': '670' },
    { 'id': 63, 'colorHex': '#306685', 'code': '823' },
    { 'id': 64, 'colorHex': '#687D78', 'code': '633' },
    { 'id': 65, 'colorHex': '#676185', 'code': '651' },
    { 'id': 66, 'colorHex': '#A9485B', 'code': '606' },
    { 'id': 67, 'colorHex': '#708179', 'code': '681' },
    { 'id': 68, 'colorHex': '#513B50', 'code': '743' },
    { 'id': 69, 'colorHex': '#BD342C', 'code': '664' },
    { 'id': 70, 'colorHex': '#C35240', 'code': '605' },
    { 'id': 71, 'colorHex': '#57472E', 'code': '679' },
    { 'id': 72, 'colorHex': '#903A53', 'code': '666' },
    { 'id': 73, 'colorHex': '#90B490', 'code': '737' },
    { 'id': 74, 'colorHex': '#6C884E', 'code': '696' },
    { 'id': 75, 'colorHex': '#5D9A5F', 'code': '614' },
    { 'id': 76, 'colorHex': '#B2B750', 'code': '648' },
    { 'id': 77, 'colorHex': '#BBAF5C', 'code': '729' },
    { 'id': 78, 'colorHex': '#5B9570', 'code': '685' },
    { 'id': 79, 'colorHex': '#CAAF4F', 'code': '733' },
    { 'id': 80, 'colorHex': '#AF6F06', 'code': '618' },
    { 'id': 81, 'colorHex': '#D0AF72', 'code': '701' },
    { 'id': 82, 'colorHex': '#C0AB80', 'code': '738' },
    { 'id': 83, 'colorHex': '#D0A849', 'code': '702' },
    { 'id': 84, 'colorHex': '#D0B16E', 'code': '683' },
    { 'id': 85, 'colorHex': '#846177', 'code': '623' },
    { 'id': 86, 'colorHex': '#CF7B7B', 'code': '612' },
    { 'id': 87, 'colorHex': '#887E86', 'code': '629' },
    { 'id': 88, 'colorHex': '#AA9C74', 'code': '853' },
    { 'id': 89, 'colorHex': '#63929A', 'code': '822' },
    { 'id': 90, 'colorHex': '#B0684D', 'code': '691' },
    { 'id': 91, 'colorHex': '#B16776', 'code': '655' },
    { 'id': 92, 'colorHex': '#6C807F', 'code': '689' },
    { 'id': 93, 'colorHex': '#C35C39', 'code': '667' },
    { 'id': 94, 'colorHex': '#78725F', 'code': '610' },
    { 'id': 95, 'colorHex': '#336880', 'code': '601' },
    { 'id': 96, 'colorHex': '#866F7C', 'code': '635' },
    { 'id': 97, 'colorHex': '#C2BC80', 'code': '730' },
    { 'id': 98, 'colorHex': '#CEB185', 'code': '703' },
    { 'id': 99, 'colorHex': '#BBB497', 'code': '706' },
    { 'id': 110, 'colorHex': '#C99865', 'code': '704' },
    { 'id': 111, 'colorHex': '#B29796', 'code': '744' },
    { 'id': 112, 'colorHex': '#BDA287', 'code': '624' },
    { 'id': 113, 'colorHex': '#81958C', 'code': '628' },
    { 'id': 114, 'colorHex': '#5A6172', 'code': '745' },
    { 'id': 115, 'colorHex': '#AB8D83', 'code': '723' },
    { 'id': 116, 'colorHex': '#847E6A', 'code': '686' },
    { 'id': 117, 'colorHex': '#FFFFFF', 'code': '600' },
    { 'id': 118, 'colorHex': '#47837B', 'code': '819' },
    { 'id': 119, 'colorHex': '#A68784', 'code': '734' },
    { 'id': 120, 'colorHex': '#BC8C88', 'code': '658' },
]


def add_markers_set():
    """Добавляет набор маркеров GuangNa 120шт в базу данных"""
    
    brand_name = "GuangNa"
    colors_amount = len(PALETTE_OBJECTS)
    
    # Проверяем, существует ли уже такой набор
    existing_set = MarkersSet.objects.filter(
        brand_name=brand_name,
        colors_amount=colors_amount
    ).first()
    
    if existing_set:
        print(f"Набор маркеров '{brand_name}, {colors_amount}шт' уже существует с ID: {existing_set.markers_set_id}")
        response = input("Хотите обновить его? (y/n): ")
        if response.lower() != 'y':
            print("Отменено.")
            return
        markers_set = existing_set
    else:
        markers_set = MarkersSet()
    
    # Подготавливаем данные цветов в формате для JSONField
    colors_data = []
    for color_obj in PALETTE_OBJECTS:
        colors_data.append({
            'id': color_obj['id'],
            'colorHex': color_obj['colorHex'],
            'code': color_obj['code']
        })
    
    # Заполняем поля модели
    markers_set.brand_name = brand_name
    markers_set.colors_amount = colors_amount
    markers_set.colors_data = colors_data
    
    # Сохраняем
    markers_set.save()
    
    print(f"✓ Набор маркеров успешно {'обновлен' if existing_set else 'добавлен'}!")
    print(f"  ID: {markers_set.markers_set_id}")
    print(f"  Бренд: {markers_set.brand_name}")
    print(f"  Количество цветов: {markers_set.colors_amount}")
    print(f"  Цветов в данных: {len(markers_set.colors_data)}")


if __name__ == '__main__':
    try:
        add_markers_set()
    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
