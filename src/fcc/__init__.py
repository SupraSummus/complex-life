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
    x: int
    y: int
    z: int
    a: int

    @property
    def cartesian(self):
        return (
            (self.q + self.w/2 + self.v/2) * CELL_DEPTH,
            self.v * CELL_HEIGHT,
            (self.w + self.v/3) * CELL_WIDTH,
        )

    def add(self, other):
        return Vector(
            q=self.q + other.q,
            v=self.v + other.v,
            w=self.w + other.w,
            x=self.x + other.x,
            y=self.y + other.y,
            z=self.z + other.z,
            a=self.a + other.a,
        )

zero = Vector(0, 0, 0, 0, 0, 0, 0)


def sphere(radius: int) -> list[Vector]:
    for q, v, w in product(
        range(-radius + 1, radius),
        range(-radius + 1, radius),
        range(-radius + 1, radius),
    ):
        derrived_coords = (-q - v, -v - w, -w - q, -q - v - w)
        if all(
            x > -radius and x < radius
            for x in derrived_coords
        ):
            yield Vector(q, v, w, *derrived_coords)


neighbour_diffs = tuple(sorted(set(sphere(2)) - set(sphere(1))))
assert len(neighbour_diffs) == 12


faces = []
for neighbour in neighbour_diffs:
    face = []
    for neighbours_neighbour in neighbour_diffs:
        neighbours_neighbour = neighbours_neighbour.add(neighbour)
        if neighbours_neighbour in neighbour_diffs:
            face.append(neighbours_neighbour)
    face = sorted(face)
    print(face)
    assert len(face) == 4
    faces.append(face)
assert len(faces) == 12
