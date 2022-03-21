import math

from OpenGL.GL import *
from pygame.math import Vector2, Vector3

from my_evil_twin.utils import y_to_color

FULL_CIRCLE = 2 * math.pi


def draw_circle(center: Vector3, rotation: Vector2, radius: float, resolution: int) -> None:
    glPushMatrix()
    glTranslatef(center.x, center.y, center.z)
    glRotatef(-rotation.y, 0, 1, 0)
    glRotatef(-rotation.x, 1, 0, 0)

    _draw_circle(center, radius, resolution)

    glPopMatrix()


def _draw_circle(center: Vector3, radius: float, resolution: int) -> None:
    angle_change = FULL_CIRCLE / resolution

    glBegin(GL_POLYGON)
    angle = 0
    while angle < FULL_CIRCLE:
        x = math.cos(angle) * radius
        y = math.sin(angle) * radius
        glColor3f(*y_to_color(center.y + y))
        glVertex2f(x, y)
        angle += angle_change
    glEnd()
