import colorsys

import numpy as np
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
from my_evil_twin import text_render

from my_evil_twin.consts import GRAVITY, JUMP_SPEED, MOVE_SPEED, TURN_SPEED
from my_evil_twin.draw import _draw_circle, draw_circle
from my_evil_twin.level import Level
from my_evil_twin.text_render import draw_text, draw_text_shadow

LEVEL = Level.parse({
    'elements': [
        {
            'type': 'sphere',
            'center': (4.5, 0.5, 3),
            'radius': 2
        },
        {
            'type': 'rectangle',
            'pos1': (0, 0, 0),
            'pos2': (2, 1, 4)
        }
    ]
})

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

resize_view(window.get_width(), window.get_height())

LEVEL.draw_compile()

glClearColor(0.5, 0.5, 1.0, 1.0)
# glEnable(GL_MULTISAMPLE) # TBD
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

rotation = pygame.Vector2()
velocity = pygame.Vector3()
position = pygame.Vector3(0, 0, -5)

pygame.event.set_grab(True)
pygame.mouse.set_visible(False)

clock = pygame.time.Clock()

running = True

on_ground = False

mouse_rel = pygame.Vector2()
while running:
    mouse_rel.update(0, 0)

    delta = clock.tick(75) / 1000.0
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEMOTION:
            mouse_rel += event.rel
        elif event.type == KEYDOWN:
            if event.key == K_w:
                velocity.z = MOVE_SPEED
            elif event.key == K_s:
                velocity.z = -MOVE_SPEED
            elif event.key == K_a:
                velocity.x = MOVE_SPEED
            elif event.key == K_d:
                velocity.x = -MOVE_SPEED
            elif event.key == K_SPACE:
                if on_ground:
                    velocity.y = JUMP_SPEED
                    on_ground = False
        elif event.type == KEYUP:
            if event.key in (K_w, K_s):
                velocity.z = 0
            elif event.key in (K_a, K_d):
                velocity.x = 0

    rotation.x += mouse_rel.y * TURN_SPEED
    rotation.y += mouse_rel.x * TURN_SPEED
    if rotation.x > 90:
        rotation.x = 90
    elif rotation.x < -90:
        rotation.x = -90
    velocity.y += GRAVITY * delta
    position += velocity.rotate_y(-rotation.y) * delta
    if position.y < 0:
        on_ground = True
        position.y = 0
        velocity.y = 0
    collided, position = LEVEL.collide(position)
    if collided:
        on_ground = True
        velocity.y = 0

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # type: ignore

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glRotatef(rotation.x, 1, 0, 0)
    glRotatef(rotation.y + 180, 0, 1, 0)
    glTranslatef(-position.x, -position.y - 1.8, -position.z)

    glDepthMask(True)
    glEnable(GL_DEPTH_TEST)

    LEVEL.draw(rotation)

    glClear(GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, 320, 180, 0, 100, 300)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glTranslatef(0, 0, -200)
    glEnable(GL_TEXTURE_2D)

    if delta == 0:
        fps_text = 'FPS: >1000'
    else:
        fps_text = f'FPS: {1 / delta:.2f}'
    draw_text(fps_text, 2, 2, Color(255, 255, 255))
    draw_text(f'X/Y/Z: {position.x:.1f}/{position.y:.1f}/{position.z:.1f}', 2, 12, Color(255, 255, 255))

    glDisable(GL_TEXTURE_2D)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()

    pygame.display.flip()


LEVEL.close()
pygame.quit()
