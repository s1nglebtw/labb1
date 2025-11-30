from .base import Material

class oboi(Material):
    def calculate(self):
        return self._base_calculate("Обои")

    def __repr__(self):
        return f"oboi(площадь={self.area}, unit_area={self.unit_area})"

    def __eq__(self, other):
        return isinstance(other, oboi) and self.area == other.area