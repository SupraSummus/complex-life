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

    @classmethod
    def from_cartesian(cls, x, y, z):
        v = round(y / CELL_HEIGHT)
        w = round(z / CELL_WIDTH - v/3)
        q = round(x / CELL_DEPTH - w/2 - v/2)
        return cls(round(q), round(v), round(w))

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

    def __truediv__(self, other):
        return self.map(lambda a: a / other)

    def __floordiv__(self, other):
        return self.map(lambda a: a // other)

    def map(self, f):
        return Vector(
            f(self.q),
            f(self.v),
            f(self.w),
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
