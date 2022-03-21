from typing import Literal, Optional, TypedDict, Union

from OpenGL.GL import *
from pygame.math import Vector2, Vector3
from typing_extensions import NotRequired

from my_evil_twin.draw import draw_circle, draw_rectangle

JsonVector2 = tuple[float, float]
JsonVector3 = tuple[float, float, float]

Sphere = tuple[Literal['sphere'], Vector3, float]
Rectangle = tuple[Literal['rectangle'], Vector3, Vector3]
LevelElement = Union[Sphere, Rectangle]


class JsonElement(TypedDict):
    type: Literal['sphere', 'rectangle']
    center: NotRequired[JsonVector3]
    radius: NotRequired[float]
    pos1: NotRequired[JsonVector3]
    pos2: NotRequired[JsonVector3]


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
                assert 'center' in element and 'radius' in element
                spheres.append(('sphere', Vector3(element['center']), element['radius']))
            elif element['type'] == 'rectangle':
                assert 'pos1' in element and 'pos2' in element
                elems.append(('rectangle', Vector3(element['pos1']), Vector3(element['pos2'])))
        return Level(spheres, elems)

    def draw_compile(self):
        if self.draw_list is not None:
            glDeleteLists(self.draw_list, 1)
        self.draw_list = glGenLists(1)
        glNewList(self.draw_list, GL_COMPILE)
        for elem in self.elems:
            if elem[0] == 'rectangle':
                draw_rectangle(elem[1], elem[2])
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

    def move_out_of_collision(self, elem: LevelElement, position: Vector3) -> Vector3:
        if elem[0] == 'sphere':
            rel = (position - elem[1]).normalize()
            return elem[1] + rel * elem[2]
        else:
            raise RuntimeError(f"Invalid level element type: {elem[0]}")

    def collide(self, position: Vector3) -> tuple[bool, Vector3]:
        for i in range(3):
            elem = self.is_colliding(position)
            if elem is None:
                return (i > 0, position)
            position = self.move_out_of_collision(elem, position)
        return (True, position)
