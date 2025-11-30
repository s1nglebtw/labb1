import math
def calculate(area, roll_width, roll_length, roll_price): # принимаем значения из основной программы
    roll_area = roll_width * roll_length # считаем площадь рулона
    rolls_needed = math.ceil(area / roll_area) # площадь комнаты делим на площадь рулона + округляем в большую сторону
    total_cost = rolls_needed * roll_price # итоговая цена за все рулоны
    return {
        "материал": "Обои",
        "площадь": area,
        "rolls_needed": rolls_needed,
        "стоимость": round(total_cost, 2) # округляем цену до 2 знаков
    }