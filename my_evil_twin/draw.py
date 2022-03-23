import math
from typing import cast

from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.math import Vector2, Vector3

from my_evil_twin.utils import y_to_color

FULL_CIRCLE = 2 * math.pi
_circle_display_lists: dict[tuple[float, int, int], int] = {}


def draw_rectangle(pos1: Vector3, pos2: Vector3, color: int = 0) -> None:
    # Bottom face
    glBegin(GL_POLYGON)
    glColor3f(*y_to_color(pos1.y + color))
    glVertex3f(pos1.x, pos1.y, pos1.z)
    glVertex3f(pos2.x, pos1.y, pos1.z)
    glVertex3f(pos2.x, pos1.y, pos2.z)
    glVertex3f(pos1.x, pos1.y, pos2.z)
    glEnd()

    # Top face
    glBegin(GL_POLYGON)
    glColor3f(*y_to_color(pos2.y + color))
    glVertex3f(pos1.x, pos2.y, pos1.z)
    glVertex3f(pos2.x, pos2.y, pos1.z)
    glVertex3f(pos2.x, pos2.y, pos2.z)
    glVertex3f(pos1.x, pos2.y, pos2.z)
    glEnd()

    # Side face 1
    glBegin(GL_POLYGON)
    glColor3f(*y_to_color(pos1.y + color))
    glVertex3f(pos1.x, pos1.y, pos1.z)
    glVertex3f(pos2.x, pos1.y, pos1.z)
    glColor3f(*y_to_color(pos2.y + color))
    glVertex3f(pos2.x, pos2.y, pos1.z)
    glVertex3f(pos1.x, pos2.y, pos1.z)
    glEnd()

    # Side face 2
    glBegin(GL_POLYGON)
    glColor3f(*y_to_color(pos1.y + color))
    glVertex3f(pos1.x, pos1.y, pos1.z)
    glVertex3f(pos1.x, pos1.y, pos2.z)
    glColor3f(*y_to_color(pos2.y + color))
    glVertex3f(pos1.x, pos2.y, pos2.z)
    glVertex3f(pos1.x, pos2.y, pos1.z)
    glEnd()

    # Side face 3
    glBegin(GL_POLYGON)
    glColor3f(*y_to_color(pos1.y + color))
    glVertex3f(pos2.x, pos1.y, pos1.z)
    glVertex3f(pos2.x, pos1.y, pos2.z)
    glColor3f(*y_to_color(pos2.y + color))
    glVertex3f(pos2.x, pos2.y, pos2.z)
    glVertex3f(pos2.x, pos2.y, pos1.z)
    glEnd()

    # Side face 4
    glBegin(GL_POLYGON)
    glColor3f(*y_to_color(pos1.y + color))
    glVertex3f(pos1.x, pos1.y, pos2.z)
    glVertex3f(pos2.x, pos1.y, pos2.z)
    glColor3f(*y_to_color(pos2.y + color))
    glVertex3f(pos2.x, pos2.y, pos2.z)
    glVertex3f(pos1.x, pos2.y, pos2.z)
    glEnd()


def draw_circle(center: Vector3, rotation: Vector2, radius: float, resolution: int, color: int = 0) -> None:
    glPushMatrix()
    glTranslatef(center.x, center.y, center.z)
    glRotatef(-rotation.y - 180, 0, 1, 0)
    glRotatef(-rotation.x, 1, 0, 0)

    lists_key = (radius, resolution, color)
    if lists_key not in _circle_display_lists:
        display_list = cast(int, glGenLists(1))
        glNewList(display_list, GL_COMPILE)
        _draw_circle(center, radius, resolution, color)
        glEndList()
        _circle_display_lists[lists_key] = display_list
    glCallList(_circle_display_lists[lists_key])

    glPopMatrix()


def _draw_circle(center: Vector3, radius: float, resolution: int, color: int) -> None:
    angle_change = FULL_CIRCLE / resolution

    glBegin(GL_POLYGON)
    angle = 0
    while angle < FULL_CIRCLE:
        x = math.cos(angle) * radius
        y = math.sin(angle) * radius
        glColor3f(*y_to_color(center.y + y + color))
        glVertex2f(x, y)
        angle += angle_change
    glEnd()


def clear_circle_display_lists() -> None:
    for lists_key in _circle_display_lists:
        glDeleteLists(_circle_display_lists[lists_key], 1)
    _circle_display_lists.clear()
