import enum

from pygame import Vector3


class Direction(enum.Enum):
    LEFT     = (Vector3(-1, 0,  0),)
    RIGHT    = (Vector3( 1, 0,  0),)
    FORWARD  = (Vector3( 0, 0,  1),)
    BACKWARD = (Vector3( 0, 0, -1),)

    def __init__(self, unit: Vector3) -> None:
        self.unit: Vector3 = unit
