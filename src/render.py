from pprint import pprint

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from fcc import sphere, zero, neighbour_diffs, Vector
from world import World, RandomGenerator, MemoryStorage, Cell


def draw_cell(coords, cell, quadric):
    glPushMatrix()
    glTranslatef(*coords.cartesian)

    glBegin(GL_LINES)
    for end, color in [
        ((0.1, 0, 0), (1, 0, 0)),
        ((0, 0.1, 0), (0, 1, 0)),
        ((0, 0, 0.1), (0, 0, 1)),
    ]:
        glColor3f(*color)
        glVertex3f(0, 0, 0)
        glVertex3fv(end)
    glEnd()

    if cell.color.a:
        glColor4f(cell.color.r, cell.color.g, cell.color.b, cell.color.a)
        gluSphere(quadric, 0.5, 16, 16)

    glPopMatrix()


def draw_connection(coords, diff):
    glPushMatrix()
    glTranslatef(*coords.cartesian)
    glBegin(GL_LINES)
    glColor3f(1.0, 1.0, 1.0)
    glVertex3f(0, 0, 0)
    glVertex3fv(diff.cartesian)
    glEnd()
    glPopMatrix()


assert len(neighbour_diffs) == 12, f"each cell has {len(neighbour_diffs)} neighbours"
pprint(neighbour_diffs)
for diff in neighbour_diffs:
    d = sum(v**2 for v in diff.cartesian) ** 0.5 - 1.0
    if d > 0.001 or d < -0.001:
        print(diff, diff.cartesian, d)
        assert False


def main():
    world = World(
        storage=MemoryStorage(),
        generator=RandomGenerator(),
    )

    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.1, 0.1, 0.1, 1.0))		# Setup The Ambient Light
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.1, 0.1, 0.1, 1.0))		# Setup The Diffuse Light
    glLightfv(GL_LIGHT0, GL_POSITION, (0.0, 10.0, 0.0, 1.0))	# Position The Light
    glEnable(GL_LIGHT0)					# Enable Light One

    quadric = gluNewQuadric()
    #gluQuadricDrawStyle(quadric, GLU_LINE)

    gluPerspective(60, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0, 0, -5)
    glRotatef(15, 1, 0, 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotatef(0.1, 0, 1, 0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        for c in sphere(3):
            draw_cell(c, world.get_cell(c), quadric)

        for diff in neighbour_diffs:
            draw_connection(zero, diff)

        pygame.display.flip()
        pygame.time.wait(1000//60)


main()
