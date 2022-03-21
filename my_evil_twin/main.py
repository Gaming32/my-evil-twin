import colorsys
import math
from typing import cast

import numpy as np
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

from my_evil_twin.consts import TURN_SPEED
from my_evil_twin.init import init_graphics

MODEL = np.asarray([
    [1, -0.5, 0],
    [0, -0.5, 0],
    [0,  0.5, 0],
    [0,  0.5, 0],
    [1,  0.5, 0],
    [1, -0.5, 0],
    # -0.6, -0.4, 0, 1, 0, 0,
    #  0.6, -0.4, 0, 0, 1, 0,
    #  0,    0.6, 0, 0, 0, 1,
], dtype=np.float32)

screen_size = pygame.Vector2()


def resize_view(width: int, height: int) -> None:
    global screen_size
    screen_size = pygame.Vector2(width, height)
    glViewport(0, 0, width, height)
    ratio = width / height
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(80, ratio, 0.01, 1000)


pygame.init()

window = pygame.display.set_mode((1280, 720), OPENGL | DOUBLEBUF)

init_graphics()

resize_view(window.get_width(), window.get_height())

model = glGenLists(1)
glNewList(model, GL_COMPILE)
glBegin(GL_TRIANGLES)
for vert in MODEL:
    glVertex3f(vert[0], vert[1], vert[2])
    glColor3f(*colorsys.hsv_to_rgb((vert[1] / 15.0) % 1, 1.0, 1.0))
glEnd()
glEndList()


# glClearColor(0.5, 0.5, 1.0, 1.0)
glClearColor(0.0, 0.0, 0.0, 1.0)
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
    if delta:
        print('FPS:', 1000 / delta, '                        ', end='\r')
    else:
        print('FPS: >1000                         ', end='\r')
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEMOTION:
            mouse_rel += event.rel

    rotation.x += mouse_rel.y * delta * TURN_SPEED
    rotation.y += mouse_rel.x * delta * TURN_SPEED
    if rotation.x > 90:
        rotation.x = 90
    elif rotation.x < -90:
        rotation.x = -90

    # identity(view_matrix)
    # view_matrix.rotate_x(rotation.x)
    # view_matrix.rotate_y(rotation.y)
    # view_matrix.translate(position.x, -position.y - 1.8, position.z)
    # glUniformMatrix4fv2(uni_view, False, view_matrix)

    # if mouse_rel:
    #     print(rotation)
    #     print(view_matrix)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # type: ignore

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glRotatef(rotation.x, 1, 0, 0)
    glRotatef(rotation.y, 0, 1, 0)
    glTranslatef(position.x, -position.y - 1.8, position.z)

    # glUniformMatrix4fv2(uni_projection, False, main_projection)
    # glMatrixMode(GL_PROJECTION)
    # glLoadIdentity()
    # gluPerspective(math.radians(80), screen_size.x / screen_size.y, 0.01, 1000)

    glDepthMask(True)
    glEnable(GL_DEPTH_TEST)

    # glDrawArrays(GL_TRIANGLES, 0, 6)
    # glBegin(GL_TRIANGLES)
    # glColor3f(1, 1, 1)
    # glVertex3f(-0.5, -0.5, 0)
    # glVertex3f(-0.5, 0.5, 0)
    # glVertex3f(0.5, -0.5, 0)
    # glEnd()
    glCallList(model)

    pygame.display.flip()


glDeleteLists(model, 1)
pygame.quit()
