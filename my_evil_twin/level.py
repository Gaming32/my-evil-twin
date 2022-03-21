from typing import Literal, Optional, TypedDict, Union
from typing_extensions import NotRequired

from OpenGL.GL import *
from pygame.math import Vector2, Vector3

from my_evil_twin.draw import draw_circle, draw_rectangle
from my_evil_twin.utils import y_to_color

JsonVector2 = tuple[float, float]
JsonVector3 = tuple[float, float, float]

Sphere = tuple[Literal['sphere'], Vector3, float]
Rectangle = tuple[Literal['rectangle'], Vector3, Vector3]
Floor = tuple[Literal['floor'], Vector2, Vector2, float, float]
LevelElement = Union[Sphere, Rectangle, Floor]


class JsonSphere(TypedDict):
    type: Literal['sphere']
    center: JsonVector3
    radius: float


class JsonRectangle(TypedDict):
    type: Literal['rectangle']
    pos1: JsonVector3
    pos2: JsonVector3


class JsonFloor(TypedDict):
    type: Literal['floor']
    pos1: JsonVector2
    pos2: JsonVector2
    y: NotRequired[float]
    thickness: NotRequired[float]


JsonElement = Union[JsonSphere, JsonRectangle, JsonFloor]


class LevelJson(TypedDict):
    elements: list[JsonElement]


class Level:
    draw_list: Optional[int]
    spheres: list[Sphere]
    elems: list[LevelElement]

    def __init__(self, spheres: list[Sphere], elems: list[LevelElement]) -> None:
        self.spheres = spheres
        self.elems = elems
        self.draw_list = None

    @classmethod
    def parse(cls, level: LevelJson) -> 'Level':
        elements = level['elements']
        spheres: list[Sphere] = []
        elems: list[LevelElement] = []
        for element in elements:
            if element['type'] == 'sphere':
                spheres.append(('sphere', Vector3(element['center']), element['radius']))
            elif element['type'] == 'rectangle':
                elems.append((
                    'rectangle',
                    Vector3(element['pos1']),
                    Vector3(element['pos2'])
                ))
            elif element['type'] == 'floor':
                elems.append((
                    'floor',
                    Vector2(element['pos1']),
                    Vector2(element['pos2']),
                    element.get('y', 0),
                    element.get('thickness', 1)
                ))
        return Level(spheres, elems)

    def draw_compile(self):
        if self.draw_list is not None:
            glDeleteLists(self.draw_list, 1)
        self.draw_list = glGenLists(1)
        glNewList(self.draw_list, GL_COMPILE)
        for elem in self.elems:
            if elem[0] == 'rectangle':
                draw_rectangle(elem[1], elem[2])
            elif elem[0] == 'floor':
                glBegin(GL_POLYGON)
                glColor3f(*y_to_color(elem[3]))
                glVertex3f(elem[1].x, elem[3], elem[1].y)
                glVertex3f(elem[1].x, elem[3], elem[2].y)
                glVertex3f(elem[2].x, elem[3], elem[2].y)
                glVertex3f(elem[2].x, elem[3], elem[1].y)
                glEnd()
        glEndList()

    def draw(self, rotation: Vector2):
        if self.draw_list is None:
            self.draw_compile()
        glCallList(self.draw_list)
        for sphere in self.spheres:
            draw_circle(sphere[1], rotation, sphere[2], 30)

    def close(self) -> None:
        if self.draw_list is not None:
            glDeleteLists(self.draw_list, 1)

    def is_colliding(self, position: Vector3) -> Optional[LevelElement]:
        for sphere in self.spheres:
            if sphere[1].distance_squared_to(position) < sphere[2] * sphere[2]:
                return sphere
        for elem in self.elems:
            if elem[0] == 'rectangle':
                if (
                    elem[1].x < position.x < elem[2].x
                    and elem[1].y <= position.y < elem[2].y
                    and elem[1].z < position.z < elem[2].z
                ):
                    return elem
            elif elem[0] == 'floor':
                if (
                    elem[3] - elem[4] < position.y <= elem[3]
                    and elem[1].x < position.x < elem[2].x
                    and elem[1].y < position.z < elem[2].y
                ):
                    return elem

    def move_out_of_collision(self, elem: LevelElement, position: Vector3) -> Vector3:
        if elem[0] == 'sphere':
            rel = (position - elem[1]).normalize()
            return elem[1] + rel * elem[2]
        elif elem[0] == 'rectangle':
            dest = Vector3(position.x, elem[2].y, position.z)
            dist = elem[2].y - position.y
            if position.x - elem[1].x < dist:
                dest = Vector3(elem[1].x, position.y, position.z)
                dist = position.x - elem[1].x
            if elem[2].x - position.x < dist:
                dest = Vector3(elem[2].x, position.y, position.z)
                dist = elem[2].x - position.x
            if position.z - elem[1].z < dist:
                dest = Vector3(position.x, position.y, elem[1].z)
                dist = position.z - elem[1].z
            if elem[2].z - position.z < dist:
                dest = Vector3(position.x, position.y, elem[2].z)
                dist = elem[2].z - position.z
            return dest
        elif elem[0] == 'floor':
            return Vector3(position.x, elem[3], position.z)
        else:
            raise RuntimeError(f"Invalid level element type: {elem[0]}")

    def collide(self, position: Vector3) -> tuple[bool, Vector3]:
        for i in range(3):
            elem = self.is_colliding(position)
            if elem is None:
                return (i > 0, position)
            position = self.move_out_of_collision(elem, position)
        return (True, position)
