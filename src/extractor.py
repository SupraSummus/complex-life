from hashlib import sha256
from functools import lru_cache


class Extractor:
    """Randomness extractor"""

    WORD_BYTES = 8
    MAX_INT = 1 << (WORD_BYTES * 8)
    BYTE_ORDER = 'little'

    def bool(self, *inputs):
        return self.int(1, *inputs) % 2 == 0

    def float(self, *inputs):
        return self.int(self.WORD_BYTES, *inputs) / self.MAX_INT

    def int(self, byte_count, *inputs):
        return int.from_bytes(self.bytes(byte_count, *inputs), self.BYTE_ORDER)

    def bytes(self, byte_count, *inputs):
        raise NotImplementedError()

    def inputs_to_bytes(self, *inputs):
        for i in inputs:
            yield from self.input_to_bytes(i)

    def input_to_bytes(self, i):
        if i < 0:
            yield b'\x00'
            i = -i
        else:
            yield b'\x01'
        yield i.to_bytes(self.WORD_BYTES, self.BYTE_ORDER)


class SHA256Extractor(Extractor):
    """SHA2 functions are (afaik) not proved to be randomness extractors,
    but they are propably fine for our aplications."""

    def __init__(self, seed):
        self.seed = seed

    @lru_cache(maxsize=1024)
    def bytes(self, byte_count, *inputs):
        assert byte_count <= 256
        h = sha256()
        h.update(self.seed)
        for b in self.inputs_to_bytes(*inputs):
            h.update(b)
        return h.digest()[:byte_count]
