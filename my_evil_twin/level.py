from typing import Literal, Optional, TypedDict

from OpenGL.GL import *
from pygame import Vector2, Vector3
from typing_extensions import NotRequired

from my_evil_twin.draw import draw_circle

JsonVector2 = tuple[float, float]
JsonVector3 = tuple[float, float, float]

Sphere = tuple[Vector3, float]


class JsonElement(TypedDict):
    type: Literal['sphere']
    center: NotRequired[JsonVector3]
    radius: NotRequired[float]


class LevelJson(TypedDict):
    elements: list[JsonElement]


class Level:
    draw_list: Optional[int]
    spheres: list[Sphere]

    def __init__(self, spheres: list[Sphere]) -> None:
        self.spheres = spheres
        self.draw_list = None

    @classmethod
    def parse(cls, level: LevelJson) -> 'Level':
        elements = level['elements']
        spheres = []
        for element in elements:
            if element['type'] == 'sphere':
                assert 'center' in element and 'radius' in element, 'Required arguments center and radius missing'
                spheres.append((Vector3(element['center']), element['radius']))
        return Level(spheres)

    def draw_compile(self):
        if self.draw_list is not None:
            glDeleteLists(self.draw_list, 1)
        self.draw_list = glGenLists(1)
        glNewList(self.draw_list, GL_COMPILE)
        glEndList()

    def draw(self, rotation: Vector2):
        if self.draw_list is None:
            self.draw_compile()
        glCallList(self.draw_list)
        for sphere in self.spheres:
            draw_circle(sphere[0], rotation, sphere[1], 30)

    def close(self) -> None:
        if self.draw_list is not None:
            glDeleteLists(self.draw_list, 1)
