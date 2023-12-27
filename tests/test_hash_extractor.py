import pytest

from extractor import HashExtractor


@pytest.mark.parametrize('count', [
    0, 1,
    30, 31, 32, 33,
    254, 255, 256, 257, 258,
])
def test_hash_extractor_getitem_count(count):
    extractor = HashExtractor()
    assert extractor.hash.digest_size == 32
    assert len(extractor[:count]) == count


def test_hash_extractor_is_deterministic():
    assert HashExtractor(b'seed')[123:456] == \
        HashExtractor(b'seed')[123:456]


@pytest.mark.parametrize(('offset', 'count', 'returned_offset', 'returned_count'), [
    (10, 1, 0, 32),
    (63, 1, 32, 32),
    (63, 2, 32, 64),
    (40, 40, 32, 64),
    (-1, 32, -32, 64),
])
def test_get(offset, count, returned_offset, returned_count):
    extractor = HashExtractor()
    assert extractor.hash.digest_size == 32
    o, b = extractor.get(offset, count)
    assert o == returned_offset
    assert len(b) == returned_count
    assert extractor.get(returned_offset, returned_count) == (o, b)
