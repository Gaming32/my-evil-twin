from typing import cast

from OpenGL.GL import *

import my_evil_twin
from my_evil_twin.consts import FLOAT_SIZE
from my_evil_twin.utils import get_shader


def init_graphics() -> tuple[int, int, int, int, int]:
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)

    vertex_shader = get_shader(GL_VERTEX_SHADER, my_evil_twin, 'shader.vert')
    fragment_shader = get_shader(GL_FRAGMENT_SHADER, my_evil_twin, 'vertexcolor.frag')

    shader_program = cast(int, glCreateProgram())
    glAttachShader(shader_program, vertex_shader)
    glAttachShader(shader_program, fragment_shader)
    glBindFragDataLocation(shader_program, 0, 'fragColor')
    glLinkProgram(shader_program)
    if not glGetProgramiv(shader_program, GL_LINK_STATUS):
        raise RuntimeError(glGetProgramInfoLog(shader_program))
    glUseProgram(shader_program)

    pos_attrib = glGetAttribLocation(shader_program, 'position')
    glEnableVertexAttribArray(pos_attrib)
    glVertexAttribPointer(pos_attrib, 3, GL_FLOAT, False, 6 * FLOAT_SIZE, 0)

    col_attrib = glGetAttribLocation(shader_program, 'color')
    glEnableVertexAttribArray(col_attrib)
    glVertexAttribPointer(col_attrib, 3, GL_FLOAT, False, 6 * FLOAT_SIZE, 3 * FLOAT_SIZE)
    return vao, vbo, vertex_shader, fragment_shader, shader_program
