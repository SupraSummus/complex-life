def location_to_sequential(x, y, z):
    seq = 0
    i = 0
    while True:
        m = 2 ** (i * 3)
        seq += (x % 2) * m
        seq += (y % 2) * m * 2
        seq += (z % 2) * m * 4
        x //= 2
        y //= 2
        z //= 2
        i += 1
        if x == 0 and y == 0 and z == 0:
            break
    return seq


class Octree:
    def init(self, height):
        self.height = height

    @property
    def span(self):
        return 2 ** self.height

    def get_node(self, x, y, z):
        lx = x // self.span
        ly = y // self.span
        lz = z // self.span

        return self.nodes

    def get_node_index(self, x, y, z):
        return (
            (x & (2 ** self.height - 1))
            | ((y & (2 ** self.height - 1)) << self.height)
            | ((z & (2 ** self.height - 1)) << (self.height * 2))
        )


class OctreeCache:
    def __init__(self, max_size=1024):
        self.max_size = max_size
        self.cache = {}
