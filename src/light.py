from dataclasses import dataclass

from fcc import Vector, sphere, neighbour_diffs


resloution = 4
directions = sphere(resolution)

max_light_level = 31
max_transmittance = 7
max_reflectance = 7
max_luminance = 7


@dataclass(frozen=True)
class LightDirection:
    direction: Vector

    def dependencies(self, cell):
        deps = []
        deps += self._incoming(self.direction, cell.reflectance * max_light_level, max_reflectance)
        deps += self._incoming(-self.direction, cell.transmittance * max_light_level, max_transmittance)
        return deps

    def update(cell):
        return cell

    def _nonzero_products(self, direction, max_value, div_value):
        for neighbour, in_direction in product(neighbour_diffs, ):
            pass
