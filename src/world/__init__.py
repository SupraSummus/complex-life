from dataclasses import dataclass
from random import random


class MemoryStorage(dict):
    def commit(self):
        pass


class ConstantGenerator:
    def __init__(self, cell):
        self.cell = cell

    def generate(self, world, point):
        return [(point, self.cell)]


class RandomGenerator:
    def generate(self, world, point):
        return [(
            point,
            Cell(Color(random(), random(), random(), round(random()))),
        )]


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
