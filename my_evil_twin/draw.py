import math

from OpenGL.GL import *
from pygame.math import Vector2, Vector3

from my_evil_twin.utils import y_to_color

FULL_CIRCLE = 2 * math.pi


def draw_rectangle(pos1: Vector3, pos2: Vector3) -> None:
    # Bottom face
    glBegin(GL_POLYGON)
    glColor3f(*y_to_color(pos1.y))
    glVertex3f(pos1.x, pos1.y, pos1.z)
    glVertex3f(pos2.x, pos1.y, pos1.z)
    glVertex3f(pos2.x, pos1.y, pos2.z)
    glVertex3f(pos1.x, pos1.y, pos2.z)
    glEnd()

    # Top face
    glBegin(GL_POLYGON)
    glColor3f(*y_to_color(pos2.y))
    glVertex3f(pos1.x, pos2.y, pos1.z)
    glVertex3f(pos2.x, pos2.y, pos1.z)
    glVertex3f(pos2.x, pos2.y, pos2.z)
    glVertex3f(pos1.x, pos2.y, pos2.z)
    glEnd()

    # Side face 1
    glBegin(GL_POLYGON)
    glColor3f(*y_to_color(pos1.y))
    glVertex3f(pos1.x, pos1.y, pos1.z)
    glVertex3f(pos2.x, pos1.y, pos1.z)
    glColor3f(*y_to_color(pos2.y))
    glVertex3f(pos2.x, pos2.y, pos1.z)
    glVertex3f(pos1.x, pos2.y, pos1.z)
    glEnd()

    # Side face 2
    glBegin(GL_POLYGON)
    glColor3f(*y_to_color(pos1.y))
    glVertex3f(pos1.x, pos1.y, pos1.z)
    glVertex3f(pos1.x, pos1.y, pos2.z)
    glColor3f(*y_to_color(pos2.y))
    glVertex3f(pos1.x, pos2.y, pos2.z)
    glVertex3f(pos1.x, pos2.y, pos1.z)
    glEnd()

    # Side face 3
    glBegin(GL_POLYGON)
    glColor3f(*y_to_color(pos1.y))
    glVertex3f(pos2.x, pos1.y, pos1.z)
    glVertex3f(pos2.x, pos1.y, pos2.z)
    glColor3f(*y_to_color(pos2.y))
    glVertex3f(pos2.x, pos2.y, pos2.z)
    glVertex3f(pos2.x, pos2.y, pos1.z)
    glEnd()

    # Side face 4
    glBegin(GL_POLYGON)
    glColor3f(*y_to_color(pos1.y))
    glVertex3f(pos1.x, pos1.y, pos2.z)
    glVertex3f(pos2.x, pos1.y, pos2.z)
    glColor3f(*y_to_color(pos2.y))
    glVertex3f(pos2.x, pos2.y, pos2.z)
    glVertex3f(pos1.x, pos2.y, pos2.z)
    glEnd()


def draw_circle(center: Vector3, rotation: Vector2, radius: float, resolution: int) -> None:
    glPushMatrix()
    glTranslatef(center.x, center.y, center.z)
    glRotatef(-rotation.y - 180, 0, 1, 0)
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
