from dataclasses import dataclass

from extractor import SHA256Extractor


class MemoryStorage(dict):
    def commit(self):
        pass


class ConstantGenerator:
    def __init__(self, cell):
        self.cell = cell

    def generate(self, world, point):
        return [(point, self.cell)]


class RandomGenerator:
    def __init__(self, extractor):
        self.extractor = extractor

    def generate(self, world, point):
        fill = self.extractor.float(point.q, point.v, point.w)
        return [(
            point,
            Cell(Color(1.0, 1.0, 1.0, fill)),
        )]


class FractalNoiseGenerator:
    def __init__(self, levels, extractor):
        self.levels = levels
        self.extractor = extractor

    def generate(self, world, point):
        for d in range(self.levels):
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
            for point, cell in self.generator.generate(self, point):
                self.storage[point] = cell
            self.storage.commit()
        return self.storage[point]


@dataclass(frozen=True)
class Color:
    r: float
    g: float
    b: float
    a: float


@dataclass(frozen=True)
class Cell:
    color: Color


default_world = World(
    storage=MemoryStorage(),
    generator=RandomGenerator(
        extractor=SHA256Extractor(b'pineapple seed'),
    ),
)
