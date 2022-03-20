import math
from typing import Optional

import numpy as np
import numpy.typing as npt
from my_evil_twin.objects.math2 import fma
from my_evil_twin.objects.matrix4c import (PROPERTY_AFFINE, PROPERTY_IDENTITY,
                                           PROPERTY_ORTHONORMAL,
                                           PROPERTY_PERSPECTIVE,
                                           PROPERTY_TRANSLATION)

ZERO = np.zeros((4, 4), np.float32)

IDENTITY = np.identity(4, np.float32)


def zero(mat: 'Matrix4f') -> None:
    mat.value[:] = ZERO


def identity(mat: 'Matrix4f') -> None:
    mat.value[:] = IDENTITY


class Matrix4f:
    value: npt.NDArray[np.float32]
    properties: int

    def __init__(self, value: Optional[npt.NDArray[np.float32]] = None) -> None:
        if value is None:
            value = np.zeros((4, 4), dtype=np.float32)
        self.value = value
        self.properties = 0

    @classmethod
    def identity(cls) -> 'Matrix4f':
        self = Matrix4f()
        value = self.value
        value[0, 0] = 1.0
        value[1, 1] = 1.0
        value[2, 2] = 1.0
        value[3, 3] = 1.0
        self.properties = PROPERTY_IDENTITY | PROPERTY_AFFINE | PROPERTY_TRANSLATION | PROPERTY_ORTHONORMAL
        return self

    def set_perspective(self, fovy: float, aspect: float, z_near: float, z_far: float) -> 'Matrix4f':
        value = self.value
        value[:] = ZERO
        h = math.tan(fovy * 0.5)
        value[0, 0] = 1.0 / (h * aspect)
        value[1, 1] = 1.0 / h
        far_inf = z_far > 0 and math.isinf(z_far)
        near_inf = z_near > 0 and math.isinf(z_near)
        if far_inf:
            e = 1e-6
            value[2, 2] = e - 1.0
            value[3, 2] = (e - 2.0) * z_near
        elif near_inf:
            e = 1e-6
            value[2, 2] = 1.0 - e
            value[3, 2] = (2.0 - e) * z_far
        else:
            value[2, 2] = (z_far + z_near) / (z_near - z_far)
            value[3, 2] = (z_far + z_far) * z_near / (z_near - z_far)
        value[2, 3] = -1.0
        self.properties = PROPERTY_PERSPECTIVE
        return self

    def set_translation(self, x: float, y: float, z: float) -> 'Matrix4f':
        self.value[3, 0] = x
        self.value[3, 1] = y
        self.value[3, 2] = z
        self.properties &= ~(PROPERTY_PERSPECTIVE | PROPERTY_IDENTITY)
        return self

    def rotation_x(self, ang: float) -> 'Matrix4f':
        sin = math.sin(ang)
        cos = math.cos(ang)
        if not (self.properties & PROPERTY_IDENTITY):
            self.value[:] = IDENTITY
        self.value[1, 1] = cos
        self.value[1, 2] = sin
        self.value[2, 1] = -sin
        self.value[2, 2] = cos
        self.properties = PROPERTY_AFFINE | PROPERTY_ORTHONORMAL
        return self

    def rotate_x(self, ang: float) -> 'Matrix4f':
        if self.properties & PROPERTY_IDENTITY:
            return self.rotation_x(ang)
        elif self.properties & PROPERTY_TRANSLATION:
            x = self.value[3, 0]
            y = self.value[3, 1]
            z = self.value[3, 2]
            return self.rotation_x(ang).set_translation(x, y, z)
        self._rotate_x(ang)
        return self

    def _rotate_x(self, ang: float) -> None:
        value = self.value
        sin = math.sin(ang)
        cos = math.cos(ang)
        lm10 = value[1, 0]
        lm11 = value[1, 1]
        lm12 = value[1, 2]
        lm13 = value[1, 3]
        lm20 = value[2, 0]
        lm21 = value[2, 1]
        lm22 = value[2, 2]
        lm23 = value[2, 3]
        value[2, 0] = fma(lm10, -sin, lm20 * cos)
        value[2, 1] = fma(lm11, -sin, lm21 * cos)
        value[2, 2] = fma(lm12, -sin, lm22 * cos)
        value[2, 3] = fma(lm13, -sin, lm23 * cos)
        value[1, 0] = fma(lm10, cos, lm20 * sin)
        value[1, 1] = fma(lm11, cos, lm21 * sin)
        value[1, 2] = fma(lm12, cos, lm22 * sin)
        value[1, 3] = fma(lm13, cos, lm23 * sin)
        value[0, 0] = value[0, 0]
        value[0, 1] = value[0, 1]
        value[0, 2] = value[0, 2]
        value[0, 3] = value[0, 3]
        value[3, 0] = value[3, 0]
        value[3, 1] = value[3, 1]
        value[3, 2] = value[3, 2]
        value[3, 3] = value[3, 3]
        self.properties &= ~(PROPERTY_PERSPECTIVE | PROPERTY_IDENTITY | PROPERTY_TRANSLATION)

    def rotation_y(self, ang: float) -> 'Matrix4f':
        sin = math.sin(ang)
        cos = math.cos(ang)
        if not (self.properties & PROPERTY_IDENTITY):
            self.value[:] = IDENTITY
        self.value[0, 0] = cos
        self.value[0, 2] = -sin
        self.value[2, 0] = sin
        self.value[2, 2] = cos
        self.properties = PROPERTY_AFFINE | PROPERTY_ORTHONORMAL
        return self

    def rotate_y(self, ang: float) -> 'Matrix4f':
        if self.properties & PROPERTY_IDENTITY:
            return self.rotation_y(ang)
        elif self.properties & PROPERTY_TRANSLATION:
            x = self.value[3, 0]
            y = self.value[3, 1]
            z = self.value[3, 2]
            return self.rotation_y(ang).set_translation(x, y, z)
        self._rotate_y(ang)
        return self

    def _rotate_y(self, ang: float) -> None:
        value = self.value
        sin = math.sin(ang)
        cos = math.cos(ang)
        nm00 = fma(value[0, 0], cos, value[2, 0] * -sin)
        nm01 = fma(value[0, 1], cos, value[2, 1] * -sin)
        nm02 = fma(value[0, 2], cos, value[2, 2] * -sin)
        nm03 = fma(value[0, 3], cos, value[2, 3] * -sin)
        value[2, 0] = fma(value[0, 0], sin, value[2, 0] * cos)
        value[2, 1] = fma(value[0, 1], sin, value[2, 1] * cos)
        value[2, 2] = fma(value[0, 2], sin, value[2, 2] * cos)
        value[2, 3] = fma(value[0, 3], sin, value[2, 3] * cos)
        value[0, 0] = nm00
        value[0, 1] = nm01
        value[0, 2] = nm02
        value[0, 3] = nm03
        value[1, 0] = value[1, 0]
        value[1, 1] = value[1, 1]
        value[1, 2] = value[1, 2]
        value[1, 3] = value[1, 3]
        value[3, 0] = value[3, 0]
        value[3, 1] = value[3, 1]
        value[3, 2] = value[3, 2]
        value[3, 3] = value[3, 3]
        self.properties &= ~(PROPERTY_PERSPECTIVE | PROPERTY_IDENTITY | PROPERTY_TRANSLATION)

    def translation(self, x: float, y: float, z: float) -> 'Matrix4f':
        value = self.value
        if not (self.properties & PROPERTY_IDENTITY):
            value[:] = IDENTITY
        value[3, 0] = x
        value[3, 1] = y
        value[3, 2] = z
        self.properties = PROPERTY_AFFINE | PROPERTY_TRANSLATION | PROPERTY_ORTHONORMAL
        return self

    def translate(self, x: float, y: float, z: float) -> 'Matrix4f':
        if self.properties & PROPERTY_IDENTITY:
            return self.translation(x, y, z)
        self._translate_generic(x, y, z)
        return self

    def _translate_generic(self, x: float, y: float, z: float) -> None:
        value = self.value
        value[3, 0] = fma(value[0, 0], x, fma(value[1, 0], y, fma(value[2, 0], z, value[3, 0])))
        value[3, 1] = fma(value[0, 1], x, fma(value[1, 1], y, fma(value[2, 1], z, value[3, 1])))
        value[3, 2] = fma(value[0, 2], x, fma(value[1, 2], y, fma(value[2, 2], z, value[3, 2])))
        value[3, 3] = fma(value[0, 3], x, fma(value[1, 3], y, fma(value[2, 3], z, value[3, 3])))
        self.properties &= ~(PROPERTY_PERSPECTIVE | PROPERTY_IDENTITY)

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        result = f'Matrix4f({self.value!r})'
        if self.properties:
            return result + f'._properties({self.properties!r})'
        return result
