import math
def calculate(area, tile_size, tiles_per_box, box_price): # принимаем значения из основной программы
    plitka_area = (tile_size / 100) ** 2  # перевод из см² в м²
    total_tiles = area / plitka_area # рассчет общего кол-ва плиток
    boxes_needed = math.ceil(total_tiles / tiles_per_box) # рассчет кол-ва коробок 
    total_cost = boxes_needed * box_price # рассчет общей стоимости
    return {
        "материал": "Плитка",
        "площадь": area,
        "boxes_needed": boxes_needed,
        "стоимость": round(total_cost, 2)
    }
