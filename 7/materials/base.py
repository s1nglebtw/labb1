from abc import ABC, abstractmethod
import math

class Material(ABC):

    def __init__(self, area, price, unit_area):
        self.area = area
        self.price = price
        self.unit_area = unit_area

    # ====== MANAGED АТРИБУТЫ ======

    @property
    def area(self):
        return self._area

    @area.setter
    def area(self, value):
        if value <= 0:
            raise ValueError("Площадь должна быть больше 0")
        self._area = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value <= 0:
            raise ValueError("Цена должна быть больше 0")
        self._price = value

    @property
    def unit_area(self):
        return self._unit_area

    @unit_area.setter
    def unit_area(self, value):
        if value <= 0:
            raise ValueError("Площадь единицы должна быть больше 0")
        self._unit_area = value

    # ====== ОБЩИЙ РАСЧЁТ ======

    def _base_calculate(self, name):
        units = math.ceil(self.area / self.unit_area)
        return {
            "материал": name,
            "площадь": self.area,
            "кол-во": units,
            "стоимость": units * self.price
        }

    @abstractmethod
    def calculate(self):
        pass

    # ====== 2 DUNDER-МЕТОДА ======

    def __str__(self):
        return f"{self.__class__.__name__}(area={self.area}, price={self.price})"

    def __len__(self):
        return math.ceil(self.area / self.unit_area)
