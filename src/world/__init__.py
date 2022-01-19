from dataclasses import dataclass
from functools import lru_cache

from extractor import Extractor, SHA256Extractor
from fcc import Vector


class MemoryStorage(dict):
    def commit(self):
        pass



class World:
    def __init__(
        self,
        storage,
        generator,
    ):
        self.storage = storage
        self.generator = generator

    def get_cell(self, point, generate=True):
        if point not in self.storage:
            if not generate:
                return None
            for point, cell in self.generator(self, point):
                self.storage[point] = cell
            self.storage.commit()
        return self.storage[point]


@dataclass(frozen=True)
class Cell:
    transmittance: int = 0  # 0-7
    reflectance: int = 0  # 0-7
    luminance: int = 0  # 0-7


Cell.air = Cell(
    transmittance=7,
)
Cell.ground = Cell(
    reflectance=1,
)
Cell.light_source = Cell(
    luminance=7,
)


default_world = World(
    storage=MemoryStorage(),
    generator=FractalNoiseGenerator(
        layer_count=4,
        extractor=SHA256Extractor(b'pineapple seed'),
    ),
)
