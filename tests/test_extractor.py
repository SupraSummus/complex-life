from extractor import HashExtractor, FloatExtractor
import pytest


@pytest.fixture(params=[
    HashExtractor(),
    FloatExtractor(HashExtractor()),
    FloatExtractor(HashExtractor(), sample_bytes=0),
], ids=[
    'HashExtractor',
    'FloatExtractor',
    'FloatExtractor_zero',
])
def extractor(request):
    return request.param


@pytest.fixture(params=[
    0, 1, 10, 100,
])
def offset(request):
    return request.param


@pytest.fixture(params=[
    0, 1, 10, 100,
])
def count(request):
    return request.param


def test_hash_extractor_getitem_count(extractor, offset, count):
    assert len(extractor[offset:offset + count]) == count


def test_hash_extractor_getitem_is_associative(extractor, offset, count):
    assert extractor[offset:offset + count] == \
        extractor[offset:offset + count // 2] + \
        extractor[offset + count // 2:offset + count]


def test_hash_extractor_getitem_single(extractor, offset):
    if extractor.item_type == bytes:
        assert extractor[offset] == extractor[offset:offset + 1][:1]
    else:
        assert extractor[offset] == extractor[offset:offset + 1][0]
