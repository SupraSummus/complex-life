import hashlib


class Extractor:
    item_type = None

    def __getitem__(self, key):
        if isinstance(key, slice):
            start, stop = validate_plain_slice(key)
            offset, values = self.get(start, stop - start)
            return values[start - offset:stop - offset]
        elif isinstance(key, int):
            offset, values = self.get(key, 1)
            return values[key - offset]
        else:
            raise TypeError('key must be int or slice')

    def get(self, offset: int, count: int):
        """
        Get output including but not limited to requested range.

        Returns (start_offset, bytes).
        """
        raise NotImplementedError()


def validate_plain_slice(s):
    if s.start is None:
        start = 0
    else:
        start = s.start
    if s.stop is None or s.stop < start:
        raise ValueError('stop must be >= start')
    if s.step is not None and s.step != 1:
        raise ValueError('step must be 1')
    return start, s.stop


class HashExtractor(Extractor):
    item_type = bytes

    def __init__(self, seed=b'', hash_name='sha3-256'):
        self.hash = hashlib.new(hash_name)
        # It is crucial to use hash function with hidden state.
        # Hash functions that output all their state can be eploited with length extension attacks.
        self.hash.update(seed)

    def __getitem__(self, key):
        if isinstance(key, int):
            return super().__getitem__(slice(key, key + 1))
        else:
            return super().__getitem__(key)

    def get(self, offset: int, count: int):
        if count < 0:
            raise ValueError('count must be >= 0')
        start_i = offset // self.hash.digest_size
        end_i = (offset + count - 1) // self.hash.digest_size
        digests = [
            self.get_digest(i)
            for i in range(start_i, end_i + 1)
        ]
        return start_i * self.hash.digest_size, b''.join(digests)

    def get_digest(self, i: int):
        h = self.hash.copy()
        if i == 0:
            return h.digest()
        elif i > 0:
            h.update(b'+')
        else:
            h.update(b'-')
            i = -i
        b = i.to_bytes(8, 'little').rstrip(b'\x00')
        h.update(b)
        return h.digest()


class FloatExtractor(Extractor):
    item_type = float

    def __init__(self, bytes_extractor, sample_bytes=4):
        self.bytes_extractor = bytes_extractor
        self.sample_bytes = sample_bytes

    def get(self, offset: int, count: int):
        if count < 0:
            raise ValueError('count must be >= 0')
        if self.sample_bytes == 0:
            return offset, [0.0] * count
        offset_b, b = self.bytes_extractor.get(
            offset * self.sample_bytes,
            count * self.sample_bytes,
        )
        offset = (offset_b - 1) // self.sample_bytes + 1
        b = b[offset * self.sample_bytes - offset_b:]
        count = len(b) // self.sample_bytes
        ints = [
            int.from_bytes(b[
                i * self.sample_bytes:
                (i + 1) * self.sample_bytes
            ], 'little')
            for i in range(count)
        ]
        max_int = 2 ** (self.sample_bytes * 8)
        return offset, [v / max_int for v in ints]
