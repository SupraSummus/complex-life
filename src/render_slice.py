from itertools import product
import pygame
from dataclasses import dataclass

from fcc import Vector
from world import default_world, World


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
        return cell.color.a
        # return 0 if cell.color.a < 0.5 else 0.999


if __name__ == '__main__':
    pygame.init()

    shader = Shader(
        world=default_world,
        scale=10,
    )

    size = width, height = (800, 600)
    screen = pygame.display.set_mode(size)
    screen.fill((255, 0, 0))
    for x, y in product(range(width), range(height)):
        v = int(shader(x, y) * 256)
        screen.set_at((x, y), (v, v, v))
    pygame.display.flip()

    pygame.event.set_allowed(None)  # allow all
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
