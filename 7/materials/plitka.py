from .base import Material

class plitka(Material):
    def calculate(self):
        return self._base_calculate("Плитка")

    def __repr__(self):
        return f"plitka(площадь={self.area}, tile_area={self.unit_area})"

    def __eq__(self, other):
        return isinstance(other, plitka) and self.unit_area == other.unit_area
