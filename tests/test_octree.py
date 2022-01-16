from octree import location_to_sequential
import pytest


def qube(x, y, z, size):
    points = set()
    for i in range(size):
        for j in range(size):
            for k in range(size):
                points.add((x + i, y + j, z + k))
    return points


@pytest.mark.parametrize(('offset', 'size'), [
    ((0, 0, 0), 1),
    ((0, 0, 0), 16),
    ((16, 256, 32), 16),
])
def test_location_to_sequential_is_continous(offset, size):
    points = qube(*offset, size)
    seqs = set(location_to_sequential(x, y, z) for x, y, z in points)
    assert len(seqs) == size ** 3
    assert max(seqs) - min(seqs) == size ** 3 - 1
