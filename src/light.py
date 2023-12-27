from dataclasses import dataclass

from fcc import Vector, neighbour_diffs, sphere

resloution = 4
directions = sphere(resolution)

max_light_level = 31
max_transmittance = 7
max_reflectance = 7
max_luminance = 7


class LightDirection:
    local_dependencies = ('reflectance', 'transmittance')

    def __init__(self, direction):
        self.direction = direction

    def dependencies(self, local_dependencies):
        reflectance, transmittance = local_dependencies
        deps = []
        deps += self._nonzero_products(self.direction, reflectance * max_light_level, max_reflectance)
        deps += self._nonzero_products(-self.direction, transmittance * max_light_level, max_transmittance)
        return deps

    def update(self, local_dependencies, dependencies):
        return cell

    def _nonzero_products(self, direction, max_value, div_value):
        for neighbour, in_direction in product(neighbour_diffs, ):
            pass
