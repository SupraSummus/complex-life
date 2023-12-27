import pytest

from octree import z_order


def qube(x, y, z, size):
    points = set()
    for i in range(size):
        for j in range(size):
            for k in range(size):
                points.add((x + i, y + j, z + k))
    return points


@pytest.mark.parametrize(('location', 'sequential'), [
    ((0, 0, 0), 0),
    ((1, 0, 0), 1),
    ((1, 1, 1), 7),

    ((2, 0, 0), 8),
    ((3, 0, 0), 9),
    ((3, 1, 1), 15),
])
def test_examples(location, sequential):
    assert z_order.order(location) == sequential
    assert tuple(z_order.point(sequential)) == location


@pytest.mark.parametrize(('offset', 'size'), [
    ((0, 0, 0), 1),
    ((0, 0, 0), 16),
    ((16, 256, 32), 16),
])
def test_order_is_continous(offset, size):
    points = qube(*offset, size)
    seqs = set(z_order.order(p) for p in points)
    assert len(seqs) == size ** 3
    assert max(seqs) - min(seqs) == size ** 3 - 1
