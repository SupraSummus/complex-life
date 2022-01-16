from extractor import HashExtractor
import pytest


@pytest.mark.parametrize('count', [
    0, 1,
    30, 31, 32, 33,
    254, 255, 256, 257, 258,
])
def test_hash_extractor_get_bytes_count(count):
    extractor = HashExtractor()
    assert extractor.hash.digest_size == 32
    assert len(extractor.get_bytes(0, count)) == count


def test_hash_extractor_is_deterministic():
    assert HashExtractor(b'seed').get_bytes(123, 456) == \
        HashExtractor(b'seed').get_bytes(123, 456)
