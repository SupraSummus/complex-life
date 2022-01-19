
class ZOrder:
    def __init__(self, dim):
        self.dim = dim

    def order(self, point) -> int:
        order = 0
        for i in range(self.dim):
            assert point[i] >= 0
            shift = i
            v = point[i]
            while v != 0:
                order |= (v & 1) << shift
                v >>= 1
                shift += self.dim
        return order

    def point(self, order: int):
        assert order >= 0
        point = [0] * self.dim
        shift = 0
        while order != 0:
            for i in range(self.dim):
                point[i] |= (order & 1) << shift
                order >>= 1
            shift += 1
        return point


z_order = ZOrder(3)


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
