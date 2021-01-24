from dataclasses import dataclass
from itertools import product


CELL_DEPTH = 1.0
CELL_HEIGHT = (6.0**0.5) / 3.0
CELL_WIDTH = (3.0**0.5) / 2.0


@dataclass(frozen=True, order=True)
class Vector:
    q: int
    v: int
    w: int

    @property
    def x(self):
        return -self.q - self.v

    @property
    def y(self):
        return -self.v - self.w

    @property
    def z(self):
        return -self.w - self.q

    @property
    def cartesian(self):
        return (
            (self.q + self.w/2 + self.v/2) * CELL_DEPTH,
            self.v * CELL_HEIGHT,
            (self.w + self.v/3) * CELL_WIDTH,
        )

    def add(self, other):
        return Vector(
            self.q + other.q,
            self.v + other.v,
            self.w + other.w,
        )

    def substract(self, other):
        return Vector(
            self.q - other.q,
            self.v - other.v,
            self.w - other.w,
        )

    def distance(self, other):
        delta = self.substract(other)
        return max(map(abs, (
            delta.q,
            delta.v,
            delta.w,
            delta.q + delta.v,
            delta.q + delta.w,
            delta.v + delta.w,
            delta.q + delta.v + delta.w,
        )))

    def product(self, other):
        return Vector(
            self.v * other.w - self.w * other.v,
            self.w * other.q - self.q * other.w,
            self.q * other.v - self.v * other.q,
        )


zero = Vector(0, 0, 0)


def sphere(radius: int) -> list[Vector]:
    for q, v, w in product(
        range(-radius + 1, radius),
        range(-radius + 1, radius),
        range(-radius + 1, radius),
    ):
        vector = Vector(q, v, w)
        d = vector.distance(zero)
        if d > -radius and d < radius:
            yield vector


neighbour_diffs = tuple(sorted(set(sphere(2)) - set(sphere(1))))
assert len(neighbour_diffs) == 12
