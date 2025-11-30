from .base import Material

class Laminate(Material):
    def calculate(self):
        return self._base_calculate("Ламинат")

    def __repr__(self):
        return f"Laminate(площадь={self.area}, pack_area={self.unit_area})"

    def __eq__(self, other):
        return isinstance(other, Laminate) and self.price == other.price
