from collections import deque

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

from my_evil_twin.consts import (FPS, GRAVITY, JUMP_SPEED, MOVE_SPEED,
                                 TURN_SPEED, VSYNC)
from my_evil_twin.level import Level
from my_evil_twin.text_render import draw_text

LEVEL = Level.parse({
    'elements': [
        {
            'type': 'sphere',
            'center': (4.5, 1.9, 3),
            'radius': 2
        },
        {
            'type': 'rectangle',
            'pos1': (0, 0, 0),
            'pos2': (2, 1, 4)
        },
        {
            'type': 'floor',
            'pos1': (-10, -10),
            'pos2': (10, 10)
        },
        {
            'type': 'wall_z',
            'x_min': -10,
            'x_max': 10,
            'y_min': 0,
            'y_max': 5,
            'z': 10,
            'direction': -1
        },
        {
            'type': 'wall_z',
            'x_min': -10,
            'x_max': 10,
            'y_min': 0,
            'y_max': 5,
            'z': -10,
            'direction': 1
        },
        {
            'type': 'wall_x',
            'z_min': -10,
            'z_max': 10,
            'y_min': 0,
            'y_max': 5,
            'x': 10,
            'direction': -1
        },
        {
            'type': 'wall_x',
            'z_min': -10,
            'z_max': 10,
            'y_min': 0,
            'y_max': 5,
            'x': -10,
            'direction': 1
        },
        {
            'type': 'deep_line_x',
            'x_min': -10,
            'x_max': -5,
            'z_min': -2,
            'z_max': 2,
            'equation': '-x - 5'
        },
        {
            'type': 'deep_line_z',
            'x_min': -2,
            'x_max': 2,
            'z_min': -10,
            'z_max': -5,
            'equation': '-x - 5'
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

window = pygame.display.set_mode((1280, 720), OPENGL | DOUBLEBUF, vsync=VSYNC)
pygame.display.set_caption('My Evil Twin')

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

fps_vals = deque(maxlen=240)

keys_pressed: set[int] = set()

mouse_rel = pygame.Vector2()
while running:
    mouse_rel.update(0, 0)

    delta = clock.tick(FPS) / 1000.0
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEMOTION:
            mouse_rel += event.rel
        elif event.type == KEYDOWN:
            keys_pressed.add(event.key)
            if event.key == K_SPACE:
                if on_ground:
                    velocity.y = JUMP_SPEED
                    on_ground = False
        elif event.type == KEYUP:
            keys_pressed.discard(event.key)

    movement = pygame.Vector2()
    if K_w in keys_pressed:
        movement.y = MOVE_SPEED
    if K_s in keys_pressed:
        movement.y = -MOVE_SPEED
    if K_a in keys_pressed:
        movement.x = MOVE_SPEED
    if K_d in keys_pressed:
        movement.x = -MOVE_SPEED
    movement.rotate_ip(rotation.y)
    velocity.x = movement.x
    velocity.z = movement.y

    fps = 1 / delta if delta else 1000
    fps_vals.append(fps)
    fps_smooth_value = sum(fps_vals) / len(fps_vals)
    min_fps = min(fps_vals)

    rotation.x += mouse_rel.y * TURN_SPEED
    rotation.y += mouse_rel.x * TURN_SPEED
    if rotation.x > 90:
        rotation.x = 90
    elif rotation.x < -90:
        rotation.x = -90

    velocity.y += GRAVITY * delta

    collided = False # Definitely always bound, but Pylance doesn't seem to know that
    for i in range(3):
        position[i] += velocity[i] * delta
        if position.y < -100:
            on_ground = False
            position.update(0, 0, -5)
            velocity.update(0, 0, 0)
            rotation.update(0, 0)
        collided, new_position = LEVEL.collide(position)
        if new_position.y != position.y:
            if new_position.y > position.y:
                on_ground = True
            position.y = new_position.y
            velocity.y = 0
        else:
            on_ground = False
        if new_position.x != position.x:
            position.x = new_position.x
            velocity.x = 0
        if new_position.z != position.z:
            position.z = new_position.z
            velocity.z = 0

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

    draw_text(f'FPS/MIN: {fps_smooth_value:.1f}/{min_fps:.1f}', 2, 2, Color(255, 255, 255))
    draw_text(f'X/Y/Z: {position.x:.1f}/{position.y:.1f}/{position.z:.1f}', 2, 12, Color(255, 255, 255))
    draw_text(f'SX/SY/SZ: {velocity.x:.1f}/{velocity.y:.1f}/{velocity.z:.1f}', 2, 22, Color(255, 255, 255))
    draw_text(f'COLLIDING/GROUND: {collided}/{on_ground}', 2, 32, Color(255, 255, 255))

    glDisable(GL_TEXTURE_2D)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()

    pygame.display.flip()


LEVEL.close()
pygame.quit()
