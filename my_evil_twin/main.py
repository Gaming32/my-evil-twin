import math
from typing import cast

import numpy as np
import pygame
from OpenGL.GL import *
from pygame.locals import *

from my_evil_twin.consts import DEGREES_90, TURN_SPEED
from my_evil_twin.init import init_graphics
from my_evil_twin.objects.matrix4f import Matrix4f, identity
from my_evil_twin.utils import glUniformMatrix4fv2

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

screen_size = pygame.Vector2()
main_projection = Matrix4f.identity()


def resize_view(width: int, height: int) -> None:
    global screen_size
    screen_size = pygame.Vector2(width, height)
    glViewport(0, 0, width, height)
    ratio = width / height
    main_projection.set_perspective(math.radians(80), ratio, 0.01, 1000)


pygame.init()

window = pygame.display.set_mode((1280, 720), OPENGL | DOUBLEBUF)

vao, vbo, vertex_shader, fragment_shader, shader_program = init_graphics()
glBufferData(GL_ARRAY_BUFFER, MODEL, GL_STATIC_DRAW)

uni_model = glGetUniformLocation(shader_program, 'model')
model_matrix = Matrix4f.identity()
glUniformMatrix4fv2(uni_model, False, model_matrix)

uni_view = glGetUniformLocation(shader_program, 'view')
view_matrix = Matrix4f.identity().translate(0, 0, -5)
glUniformMatrix4fv2(uni_view, False, view_matrix)

uni_projection = glGetUniformLocation(shader_program, 'projection')

resize_view(window.get_width(), window.get_height())


# glClearColor(0.5, 0.5, 1.0, 1.0)
# glEnable(GL_MULTISAMPLE) # TBD

rotation = pygame.Vector2()

velocity = pygame.Vector3()
position = pygame.Vector3(0, 0, -5)

pygame.event.set_grab(True)
pygame.mouse.set_visible(False)

clock = pygame.time.Clock()

running = True

mouse_rel = pygame.Vector2()
while running:
    mouse_rel.update(0, 0)

    delta = clock.tick()
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEMOTION:
            mouse_rel += event.rel

    rotation.x += mouse_rel.y * delta * TURN_SPEED
    rotation.y += mouse_rel.x * delta * TURN_SPEED
    if rotation.x > DEGREES_90:
        rotation.x = DEGREES_90
    elif rotation.x < -DEGREES_90:
        rotation.x = -DEGREES_90

    identity(view_matrix)
    view_matrix.rotate_x(rotation.x)
    view_matrix.rotate_y(-rotation.y)
    view_matrix.translate(position.x, -position.y - 1.8, position.z)
    glUniformMatrix4fv2(uni_view, False, view_matrix)

    if mouse_rel:
        print(rotation)
        print(view_matrix)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # type: ignore

    glUniformMatrix4fv2(uni_projection, False, main_projection)

    glDepthMask(True)
    glEnable(GL_DEPTH_TEST)

    glDrawArrays(GL_TRIANGLES, 0, 6)

    pygame.display.flip()


glDeleteVertexArrays(1, (vao,))
glDeleteBuffers(1, (vbo,))
glDeleteShader(vertex_shader)
glDeleteShader(fragment_shader)
glDeleteProgram(shader_program)
pygame.quit()
