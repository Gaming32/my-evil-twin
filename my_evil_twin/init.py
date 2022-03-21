from typing import cast

from OpenGL.GL import *
import numpy as np

import my_evil_twin
from my_evil_twin.consts import FLOAT_SIZE
from my_evil_twin.utils import get_shader

MODEL = np.asarray([
  #  x,    y,   z, r, g, b
    -0.5, -0.5, 0, 1, 0, 0,
    -0.5,  0.5, 0, 1, 0, 0,
     0.5, -0.5, 0, 1, 0, 0,
    -0.5,  0.5, 0, 0, 0, 1,
     0.5,  0.5, 0, 0, 0, 1,
     0.5, -0.5, 0, 0, 0, 1
    # -0.6, -0.4, 0, 1, 0, 0,
    #  0.6, -0.4, 0, 0, 1, 0,
    #  0,    0.6, 0, 0, 0, 1,
], dtype=np.float32)


def init_graphics() -> None:
    pass
