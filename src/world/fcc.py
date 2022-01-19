
@dataclass(frozen=True)
class FractalNoiseGeneratorFCC:
    layer_count: int
    extractor: Extractor

    def __call__(self, world, point):
        components = []
        for layer in range(self.layer_count):
            chunk_position, chunk_offset, chunk_length = self.get_chunk(layer, point)
            distance_weight_sum = 0
            middle_v = 0
            v = 0
            neighbours = [
                Vector.zero,
                Vector(0, 0, 1),
                Vector(0, 1, 0),
                Vector(0, 1, 1),
                Vector(1, 0, 0),
                Vector(1, 0, 1),
                Vector(1, 1, 0),
                Vector(1, 1, 1),
            ]
            for chunk_neighbour in neighbours:
                chunk_representative = chunk_neighbour * chunk_length
                distance = chunk_offset.distance(chunk_representative)
                distance_weight = max(chunk_length - distance, 0) / chunk_length
                distance_weight_sum += distance_weight
                v += self.get_chunk_value(layer, chunk_position + chunk_neighbour) * distance_weight
            middle_v = self.get_chunk_value(layer, chunk_position, middle=True)
            components.append((v + (1 - distance_weight_sum) * middle_v, self.get_feature_amplitude(layer)))
        v, max_v = map(sum, zip(*components))
        yield (
            point,
            Cell.air if v / max_v < 0.5 else Cell.ground,
        )

    @lru_cache(maxsize=1024)
    def get_chunk(self, layer, point):
        chunk_length = self.get_feature_length(layer)
        chunk_position = point // chunk_length
        chunk_offset = point % chunk_length
        return chunk_position, chunk_offset, chunk_length

    @lru_cache(maxsize=1024)
    def get_chunk_value(self, layer, chunk_position, middle=False):
        feature_amplitude = self.get_feature_amplitude(layer)
        return self.extractor.float(
            layer, middle,
            *chunk_position.as_tuple(),
        ) * feature_amplitude

    def get_feature_length(self, layer):
        return 1.5**layer

    def get_feature_amplitude(self, layer):
        return 1.5**layer