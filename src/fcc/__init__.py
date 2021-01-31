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

    def __add__(self, other):
        if isinstance(other, Vector):
            return self.bimap((lambda a, b: a + b), other)
        else:
            raise ValueError()

    def __sub__(self, other):
        if isinstance(other, Vector):
            return self.bimap((lambda a, b: a - b), other)
        else:
            raise ValueError()

    def __mul__(self, other):
        return self.map(lambda a: a * other)

    def __truediv__(self, other):
        return self.map(lambda a: a / other)

    def __floordiv__(self, other):
        return self.map(lambda a: a // other)

    def __mod__(self, other):
        return self.map(lambda a: a % other)

    def map(self, f):
        return Vector(
            f(self.q),
            f(self.v),
            f(self.w),
        )

    def bimap(self, f, other):
        return Vector(
            f(self.q, other.q),
            f(self.v, other.v),
            f(self.w, other.w),
        )

    def distance(self, other):
        delta = self - other
        return max(map(abs, (
            delta.q,
            delta.v,
            delta.w,
            delta.x,
            delta.y,
            delta.z,
            delta.q + delta.v + delta.w,
        )))

    def as_tuple(self):
        return (self.q, self.v, self.w)

    @classmethod
    @property
    def zero(cls):
        return cls(0, 0, 0)


zero = Vector.zero


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
