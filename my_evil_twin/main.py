from collections import deque

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

from my_evil_twin.consts import (FPS, GRAVITY, JUMP_SPEED, MOVE_SPEED,
                                 TURN_SPEED, VSYNC)
from my_evil_twin.draw import clear_circle_display_lists
from my_evil_twin.level_data import LEVEL
from my_evil_twin.text_render import draw_text

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

window = pygame.display.set_mode((1280, 720), OPENGL | DOUBLEBUF | RESIZABLE, vsync=VSYNC)
pygame.display.set_caption('My Evil Twin')

resize_view(window.get_width(), window.get_height())

LEVEL.draw_compile()

glClearColor(0.5, 0.5, 1.0, 1.0)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

rotation = pygame.Vector2()
velocity = pygame.Vector3()
position = pygame.Vector3(0, 0, -5)

pygame.event.set_grab(True)
pygame.mouse.set_visible(False)
mouse_owned = True

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
            if mouse_owned:
                mouse_rel += event.rel
        elif event.type == KEYDOWN:
            keys_pressed.add(event.key)
            if event.key == K_SPACE:
                if on_ground:
                    velocity.y = JUMP_SPEED
                    on_ground = False
            elif event.key == K_ESCAPE:
                pygame.mouse.set_visible(True)
                pygame.event.set_grab(False)
                mouse_owned = False
        elif event.type == KEYUP:
            keys_pressed.discard(event.key)
            if event.key == K_F11:
                pygame.display.toggle_fullscreen()
                resize_view(window.get_width(), window.get_height())
        elif event.type == MOUSEBUTTONDOWN:
            pygame.event.set_grab(True)
            pygame.mouse.set_visible(False)
            mouse_owned = True
        elif event.type == VIDEORESIZE:
            resize_view(event.w, event.h)

    movement = pygame.Vector2()
    if K_w in keys_pressed:
        movement.y += MOVE_SPEED
    if K_s in keys_pressed:
        movement.y -= MOVE_SPEED
    if K_a in keys_pressed:
        movement.x += MOVE_SPEED
    if K_d in keys_pressed:
        movement.x -= MOVE_SPEED
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

    collided = False
    for i in range(3):
        position[i] += velocity[i] * delta
        if position.y < -100:
            on_ground = False
            position.update(0, 0, -5)
            velocity.update(0, 0, 0)
            rotation.update(0, 0)
        collided_this_time, new_position = LEVEL.collide(position)
        collided = collided or collided_this_time
        if i == 1:
            if new_position.y != position.y:
                if new_position.y > position.y:
                    on_ground = True
                position.y = new_position.y
                velocity.y = 0
            else:
                on_ground = False
        if i == 0:
            if new_position.x != position.x:
                position.x = new_position.x
                velocity.x = 0
        if i == 2:
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
    glOrtho(0, screen_size.x / 4, screen_size.y / 4, 0, 100, 300)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glTranslatef(0, 0, -200)
    glEnable(GL_TEXTURE_2D)

    draw_text(f'FPS/MIN: {fps_smooth_value:.1f}/{min_fps:.1f}', 2, 2, Color(255, 255, 255))
    draw_text(f'X/Y/Z: {position.x:.1f}/{position.y:.1f}/{position.z:.1f}', 2, 12, Color(255, 255, 255))
    draw_text(f'VX/VY/VZ: {velocity.x:.1f}/{velocity.y:.1f}/{velocity.z:.1f}', 2, 22, Color(255, 255, 255))
    draw_text(f'COLLIDING/GROUND: {collided}/{on_ground}', 2, 32, Color(255, 255, 255))

    glDisable(GL_TEXTURE_2D)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()

    pygame.display.flip()


LEVEL.close()
clear_circle_display_lists()
pygame.quit()
