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
            (self.q + self.w / 2 + self.v / 2) * CELL_DEPTH,
            self.v * CELL_HEIGHT,
            (self.w + self.v / 3) * CELL_WIDTH,
        )

    @classmethod
    def from_cartesian(cls, x, y, z):
        v = round(y / CELL_HEIGHT)
        w = round(z / CELL_WIDTH - v / 3)
        q = round(x / CELL_DEPTH - w / 2 - v / 2)
        return cls(q, v, w)

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
        return (self - other).length

    @property
    def length(self):
        return max(map(abs, (
            self.q,
            self.v,
            self.w,
            self.x,
            self.y,
            self.z,
            self.q + self.v + self.w,
        )))

    def dot(self, other):
        return sum((
            self.q * other.q,
            self.v * other.v,
            self.w * other.w,
            self.x * other.x,
            self.y * other.y,
            self.z * other.z,
        )) / 3

    def as_tuple(self):
        return (self.q, self.v, self.w)

    @property
    def full_tuple(self):
        return (self.q, self.v, self.w, self.x, self.y, self.z)


Vector.zero = Vector(0, 0, 0)


def ball(radius: int):
    for q, v, w in product(
        range(-radius, radius + 1),
        range(-radius, radius + 1),
        range(-radius, radius + 1),
    ):
        vector = Vector(q, v, w)
        d = vector.distance(Vector.zero)
        if d <= radius:
            yield vector


def sphere(radius):
    return tuple(sorted(
        set(ball(radius)) - set(ball(radius - 1))
    ))


neighbour_diffs = sphere(1)
