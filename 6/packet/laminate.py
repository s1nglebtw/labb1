import math
def calculate(area, pack_area, pack_price): # принимаем значения из основной программы
    packs_needed = math.ceil(area / pack_area) # рассчет кол-ва упаковок 
    total_cost = packs_needed * pack_price # рассчет итоговой стоимости
    return {
        "материал": "Ламинат",
        "площадь": area,
        "packs_needed": packs_needed,
        "стоимость": round(total_cost, 2)
    }
