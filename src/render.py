from pprint import pprint

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from fcc import sphere, neighbour_diffs, ball, Vector
from world import default_world


def draw_cell(coords, cell, quadric):
    glPushMatrix()
    xyz = coords.cartesian
    glTranslatef(*xyz)

    if cell.transmittance > 0:
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
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    # Enable Light One
    glLightfv(GL_LIGHT0, GL_POSITION, (1.0, 1.0, 0.0, 0.0))	 # light direction
    glEnable(GL_LIGHT0)

    quadric = gluNewQuadric()

    gluPerspective(60, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0, 0, -15)
    glRotatef(15, 1, 0, 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotatef(1, 0, 1, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        #for i in range(15):
        #    print(i, len(sphere(i)))
        #3/0

        for c in ball(6):
            draw_cell(c, default_world.get_cell(c), quadric)

        for diff in neighbour_diffs:
            draw_connection(Vector.zero, diff)

        pygame.display.flip()
        pygame.time.wait(1000//60)


main()
