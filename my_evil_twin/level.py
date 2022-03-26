from typing import Callable, Literal, Optional, TypedDict, Union

from OpenGL.GL import *
from pygame.math import Vector2, Vector3
from typing_extensions import NotRequired

from my_evil_twin.draw import draw_circle, draw_rectangle
from my_evil_twin.utils import set_local_color_offset, y_to_color

JsonVector2 = tuple[float, float]
JsonVector3 = tuple[float, float, float]

Sphere = tuple[Literal['sphere'], Vector3, float]
Rectangle = tuple[Literal['rectangle'], Vector3, Vector3]
Floor = tuple[Literal['floor'], Vector2, Vector2, float, float]
WallZ = tuple[Literal['wall_z'], float, float, float, float, float, float, int]
WallX = tuple[Literal['wall_x'], float, float, float, float, float, float, int]
DeepLineX = tuple[Literal['deep_line_x'], float, float, float, float, Callable[[float], float], float]
DeepLineZ = tuple[Literal['deep_line_z'], float, float, float, float, Callable[[float], float], float]
LevelElement = Optional[Union[Sphere, Rectangle, Floor, WallZ, WallX, DeepLineX, DeepLineZ]]


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


class JsonWallZ(TypedDict):
    type: Literal['wall_z']
    x_min: float
    x_max: float
    y_min: float
    y_max: float
    z: float
    thickness: NotRequired[float]
    direction: int


class JsonWallX(TypedDict):
    type: Literal['wall_x']
    z_min: float
    z_max: float
    y_min: float
    y_max: float
    x: float
    thickness: NotRequired[float]
    direction: int


class JsonDeepLineX(TypedDict):
    type: Literal['deep_line_x']
    x_min: float
    x_max: float
    z_min: float
    z_max: float
    equation: str
    thickness: NotRequired[float]


class JsonDeepLineZ(TypedDict):
    type: Literal['deep_line_z']
    x_min: float
    x_max: float
    z_min: float
    z_max: float
    equation: str
    thickness: NotRequired[float]


JsonElement = Optional[Union[JsonSphere, JsonRectangle, JsonFloor, JsonWallZ, JsonWallX, JsonDeepLineX, JsonDeepLineZ]]


class LevelJson(TypedDict):
    spawn: NotRequired[Union[JsonVector3, JsonVector2]]
    elements: list[JsonElement]


def compile_to_function(equ_code: str) -> Callable[[float], float]:
    return eval(f'lambda x: {equ_code}')


class Level:
    spheres: list[Sphere]
    elems: list[LevelElement]
    draw_list: Optional[int]
    spawn: Vector3

    def __init__(self, spheres: list[Sphere], elems: list[LevelElement], spawn: Vector3) -> None:
        self.spheres = spheres
        self.elems = elems
        self.draw_list = None
        self.spawn = spawn

    @classmethod
    def parse(cls, level: LevelJson) -> 'Level':
        if 'spawn' in level:
            if len(level['spawn']) == 3:
                spawn = Vector3(level['spawn'])
            else:
                spawn = Vector3(level['spawn'][0], 0, level['spawn'][1])
        else:
            spawn = Vector3(0, 0, -5)
        elements = level['elements']
        spheres: list[Sphere] = []
        elems: list[LevelElement] = []
        for element in elements:
            if element is None:
                elems.append(None)
                continue
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
            elif element['type'] == 'wall_z':
                elems.append((
                    'wall_z',
                    element['x_min'],
                    element['x_max'],
                    element['y_min'],
                    element['y_max'],
                    element['z'],
                    element.get('thickness', 1),
                    element['direction']
                ))
            elif element['type'] == 'wall_x':
                elems.append((
                    'wall_x',
                    element['z_min'],
                    element['z_max'],
                    element['y_min'],
                    element['y_max'],
                    element['x'],
                    element.get('thickness', 1),
                    element['direction']
                ))
            elif element['type'] == 'deep_line_x':
                elems.append((
                    'deep_line_x',
                    element['x_min'],
                    element['x_max'],
                    element['z_min'],
                    element['z_max'],
                    compile_to_function(element['equation']),
                    element.get('thickness', 1)
                ))
            elif element['type'] == 'deep_line_z':
                elems.append((
                    'deep_line_z',
                    element['x_min'],
                    element['x_max'],
                    element['z_min'],
                    element['z_max'],
                    compile_to_function(element['equation']),
                    element.get('thickness', 1)
                ))
        return Level(spheres, elems, spawn)

    def draw_compile(self):
        if self.draw_list is not None:
            glDeleteLists(self.draw_list, 1)
        self.draw_list = glGenLists(1)
        glNewList(self.draw_list, GL_COMPILE)
        for (i, elem) in enumerate(self.elems):
            if elem is None:
                continue
            set_local_color_offset(2 * i)
            if elem[0] == 'rectangle':
                draw_rectangle(elem[1], elem[2], i)
            elif elem[0] == 'floor':
                glBegin(GL_POLYGON)
                glColor3f(*y_to_color(elem[3]))
                glVertex3f(elem[1].x, elem[3], elem[1].y)
                glVertex3f(elem[1].x, elem[3], elem[2].y)
                glVertex3f(elem[2].x, elem[3], elem[2].y)
                glVertex3f(elem[2].x, elem[3], elem[1].y)
                glEnd()
            elif elem[0] == 'wall_z':
                glBegin(GL_POLYGON)
                glColor3f(*y_to_color(elem[3]))
                glVertex3f(elem[1], elem[3], elem[5])
                glVertex3f(elem[2], elem[3], elem[5])
                glColor3f(*y_to_color(elem[4]))
                glVertex3f(elem[2], elem[4], elem[5])
                glVertex3f(elem[1], elem[4], elem[5])
                glEnd()
            elif elem[0] == 'wall_x':
                glBegin(GL_POLYGON)
                glColor3f(*y_to_color(elem[3]))
                glVertex3f(elem[5], elem[3], elem[1])
                glVertex3f(elem[5], elem[3], elem[2])
                glColor3f(*y_to_color(elem[4]))
                glVertex3f(elem[5], elem[4], elem[2])
                glVertex3f(elem[5], elem[4], elem[1])
                glEnd()
            elif elem[0] == 'deep_line_x':
                x = elem[1]
                while True:
                    next_x = min(x + 1, elem[2])
                    if x == next_x:
                        break
                    y = elem[5](x)
                    next_y = elem[5](next_x)
                    glBegin(GL_POLYGON)
                    glColor3f(*y_to_color(y))
                    glVertex3f(x, y, elem[3])
                    glVertex3f(x, y, elem[4])
                    glColor3f(*y_to_color(next_y))
                    glVertex3f(next_x, next_y, elem[4])
                    glVertex3f(next_x, next_y, elem[3])
                    glEnd()
                    x = next_x
            elif elem[0] == 'deep_line_z':
                z = elem[3]
                while True:
                    next_z = min(z + 1, elem[4])
                    if z == next_z:
                        break
                    y = elem[5](z)
                    next_y = elem[5](next_z)
                    glBegin(GL_POLYGON)
                    glColor3f(*y_to_color(y))
                    glVertex3f(elem[1], y, z)
                    glVertex3f(elem[2], y, z)
                    glColor3f(*y_to_color(next_y))
                    glVertex3f(elem[2], next_y, next_z)
                    glVertex3f(elem[1], next_y, next_z)
                    glEnd()
                    z = next_z
        glEndList()

    def draw(self, rotation: Vector2):
        if self.draw_list is None:
            self.draw_compile()
        glCallList(self.draw_list)
        for (i, sphere) in enumerate(self.spheres):
            set_local_color_offset(len(self.elems) + 2 * i)
            draw_circle(sphere[1], rotation, sphere[2], 30)

    def reset_draw_list(self) -> None:
        if self.draw_list is not None:
            glDeleteLists(self.draw_list, 1)
        self.draw_list = None

    def close(self) -> None:
        self.reset_draw_list()

    def is_colliding(self, position: Vector3) -> Optional[LevelElement]:
        for sphere in self.spheres:
            if sphere[1].distance_squared_to(position) < sphere[2] * sphere[2]:
                return sphere
        for elem in self.elems:
            if elem is None:
                continue
            if elem[0] == 'rectangle':
                if (
                    elem[1].x - 0.1 < position.x < elem[2].x + 0.1
                    and elem[1].y <= position.y < elem[2].y
                    and elem[1].z - 0.1 < position.z < elem[2].z + 0.1
                ):
                    return elem
            elif elem[0] == 'floor':
                if (
                    elem[3] - elem[4] < position.y < elem[3]
                    and elem[1].x < position.x < elem[2].x
                    and elem[1].y < position.z < elem[2].y
                ):
                    return elem
            elif elem[0] == 'wall_z':
                if elem[7] < 0:
                    check = elem[5] - 0.1 < position.z < elem[5] + elem[6]
                else:
                    check = elem[5] - elem[6] < position.z < elem[5] + 0.1
                if (
                    check
                    and elem[1] < position.x < elem[2]
                    and elem[3] - 0.1 < position.y < elem[4] - 0.1
                ):
                    return elem
            elif elem[0] == 'wall_x':
                if elem[7] < 0:
                    check = elem[5] - 0.1 < position.x < elem[5] + elem[6]
                else:
                    check = elem[5] - elem[6] < position.x < elem[5] + 0.1
                if (
                    check
                    and elem[1] < position.z < elem[2]
                    and elem[3] - 0.1 < position.y < elem[4] - 0.1
                ):
                    return elem
            elif elem[0] == 'deep_line_x':
                y = elem[5](position.x)
                if (
                    elem[1] < position.x < elem[2]
                    and elem[3] < position.z < elem[4]
                    and y - elem[6] < position.y < y
                ):
                    return elem
            elif elem[0] == 'deep_line_z':
                y = elem[5](position.z)
                if (
                    elem[1] < position.x < elem[2]
                    and elem[3] < position.z < elem[4]
                    and y - elem[6] < position.y < y
                ):
                    return elem

    def move_out_of_collision(self, elem: LevelElement, position: Vector3) -> Vector3:
        if elem is None:
            return position
        if elem[0] == 'sphere':
            rel = (position - elem[1]).normalize()
            return elem[1] + rel * elem[2]
        elif elem[0] == 'rectangle':
            dest = Vector3(position.x, elem[2].y, position.z)
            dist = elem[2].y - position.y
            if position.x - elem[1].x < dist:
                dest = Vector3(elem[1].x - 0.1, position.y, position.z)
                dist = position.x - elem[1].x
            if elem[2].x - position.x < dist:
                dest = Vector3(elem[2].x + 0.1, position.y, position.z)
                dist = elem[2].x - position.x
            if position.z - elem[1].z < dist:
                dest = Vector3(position.x, position.y, elem[1].z - 0.1)
                dist = position.z - elem[1].z
            if elem[2].z - position.z < dist:
                dest = Vector3(position.x, position.y, elem[2].z + 0.1)
                dist = elem[2].z - position.z
            return dest
        elif elem[0] == 'floor':
            return Vector3(position.x, elem[3], position.z)
        elif elem[0] == 'wall_z':
            return Vector3(position.x, position.y, elem[5] + elem[7] * 0.1)
        elif elem[0] == 'wall_x':
            return Vector3(elem[5] + elem[7] * 0.1, position.y, position.z)
        elif elem[0] == 'deep_line_x':
            return Vector3(position.x, elem[5](position.x), position.z)
        elif elem[0] == 'deep_line_z':
            return Vector3(position.x, elem[5](position.z), position.z)
        else:
            raise RuntimeError(f"Invalid level element type: {elem[0]}")

    def collide(self, position: Vector3) -> tuple[bool, Vector3]:
        for i in range(3):
            elem = self.is_colliding(position)
            if elem is None:
                return (i > 0, position)
            position = self.move_out_of_collision(elem, position)
        return (True, position)
