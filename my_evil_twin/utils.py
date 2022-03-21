from importlib import resources
from typing import cast

from OpenGL.GL import *


def get_shader(type: int, package: resources.Package, resource: resources.Resource) -> int:
    shader = cast(int, glCreateShader(type))
    glShaderSource(shader, resources.read_text(package, resource))
    glCompileShader(shader)
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        message = cast(bytes, glGetShaderInfoLog(shader)).decode()
        raise RuntimeError(f'Failed to compile {resource}: {message}')
    return shader
