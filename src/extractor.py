from dataclasses import dataclass
from functools import lru_cache
from hashlib import sha256
import struct
import hashlib


class BytesExtractor:
    item_type = bytes

    def get_bytes(self, offset, count):
        raise NotImplementedError()


def validate_plain_slice(s):
    if s.start is None or s.start < 0:
        raise ValueError('start must be >= 0')
    if s.stop is None or s.stop < s.start:
        raise ValueError('stop must be >= start')
    if s.step is not None and s.step != 1:
        raise ValueError('step must be 1 or unset')
    return s.start, s.stop



class HashExtractor(BytesExtractor):
    def __init__(self, seed=b'', hash_name='sha256'):
        self.hash = hashlib.new(hash_name)
        self.seed = seed

    def __getitem__(self, key):
        if isinstance(key, slice):
            start, stop = validate_plain_slice(key)
            return self.get_bytes(start, stop - start)
        elif isinstance(key, int):
            if key < 0:
                raise TypeError('key must be >= 0')
            return self.get_bytes(key, 1)
        else:
            raise TypeError('key must be int or slice')

    def get_bytes(self, offset, count):
        start_i = offset // self.hash.digest_size
        end_i = (offset + count) // self.hash.digest_size
        digests = [
            self.get_digest(i)
            for i in range(start_i, end_i + 1)
        ]
        return b''.join(digests)[
            offset - start_i * self.hash.digest_size:
            offset + count - start_i * self.hash.digest_size
        ]

    def get_digest(self, i):
        h = self.hash.copy()
        b = i.to_bytes(8, 'little').rstrip(b'\x00')
        h.update(b)
        h.update(self.seed)
        return h.digest()


class FloatExtractor:
    item_type = float

    def __init__(self, bytes_extractor, sample_bytes=4):
        self.bytes_extractor = bytes_extractor
        self.sample_bytes = sample_bytes

    def __getitem__(self, key):
        if isinstance(key, int):
            if key < 0:
                raise IndexError()
            return self.get_floats(key, 1)[0]
        elif isinstance(key, slice):
            start, stop = validate_plain_slice(key)
            return self.get_floats(start, stop - start)
        else:
            raise TypeError('key must be int or slice')

    def get_floats(self, offset, count):
        if self.sample_bytes == 0:
            return [0.0] * count
        b = self.bytes_extractor.get_bytes(
            offset * self.sample_bytes,
            count * self.sample_bytes,
        )
        ints = [
            int.from_bytes(b[i:i + self.sample_bytes], 'little')
            for i in range(0, len(b), self.sample_bytes)
        ]
        max_int = 2 ** (self.sample_bytes * 8)
        return [v / max_int for v in ints]
