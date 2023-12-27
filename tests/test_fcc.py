import pytest

import fcc


def test_there_are_12_neighbours():
    assert len(fcc.neighbour_diffs) == 12


def test_neighbours_are_spaced_1_in_fcc_coords():
    for neighbour_diff in fcc.neighbour_diffs:
        assert neighbour_diff.length == 1


def test_neighbours_are_spaced_1_in_cartesian_coords():
    for neighbour_diff in fcc.neighbour_diffs:
        assert sum(v ** 2 for v in neighbour_diff.cartesian) == pytest.approx(1.0)


@pytest.mark.parametrize(
    "a,b,a_dot_b",
    [
        (fcc.Vector(1, 0, 0), fcc.Vector(1, 0, 0), 1),
        (fcc.Vector(-3, 0, 0), fcc.Vector(5, 0, 0), -15),
        (fcc.Vector(1, 0, 0), fcc.Vector(0, -1, 1), 0),
    ],
)
def test_dot_product_looks_sane(a, b, a_dot_b):
    assert a.dot(b) == a_dot_b


@pytest.mark.parametrize("v", fcc.neighbour_diffs)
def test_there_are_two_zero_neighbour_dot_products(v):
    assert len([
        d for d in fcc.neighbour_diffs
        if d.dot(v) == 0
    ]) == 2
