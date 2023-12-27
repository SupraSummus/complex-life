from dataclasses import dataclass
from itertools import product

import pygame

from fcc import Vector
from world import World, default_world


@dataclass
class Shader:
    world: World
    scale: float
    y: int = 0

    def __call__(self, x, y):
        coord = Vector.from_cartesian(
            x / self.scale,
            self.y,
            y / self.scale,
        )
        cell = self.world.get_cell(coord)
        return cell.transmittance / 7 * 255


if __name__ == '__main__':
    pygame.init()

    shader = Shader(
        world=default_world,
        scale=5,
        y=0,
    )

    size = width, height = (800, 600)
    screen = pygame.display.set_mode(size)
    screen.fill((255, 0, 0))
    for x, y in product(range(width), range(height)):
        v = shader(x, y)
        if v < 0:
            screen.set_at((x, y), (0, 0, 255))
            assert False
        elif v > 255:
            screen.set_at((x, y), (255, 0, 0))
            assert False
        else:
            screen.set_at((x, y), (v, v, v))
    pygame.display.flip()

    pygame.event.set_allowed(None)  # allow all
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
