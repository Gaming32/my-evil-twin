import random
from collections import deque
from typing import Optional, cast

import pygame
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective
from pygame.locals import *

from my_evil_twin.consts import (AI_TICK_TIME, ENEMY_COUNT, ENEMY_SIZE, ENEMY_SIZE_SQUARED, FPS,
                                 GRAVITY, HIDDEN_ENEMY_COUNT, JUMP_SPEED,
                                 MOVE_SPEED, TURN_SPEED, VSYNC)
from my_evil_twin.draw import clear_circle_display_lists, draw_rectangle
from my_evil_twin.level_data import LEVEL
from my_evil_twin.text_render import draw_centered_text, draw_text
from my_evil_twin.utils import (get_global_color_offset,
                                set_global_color_offset,
                                set_local_color_offset)

screen_size = pygame.Vector2()


def resize_view(width: int, height: int) -> None:
    global screen_size
    screen_size = pygame.Vector2(width, height)
    glViewport(0, 0, width, height)
    ratio = width / height
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(80, ratio, 0.01, 1000)


def respawn() -> None:
    global on_ground
    on_ground = False
    position.update(LEVEL.spawn)
    velocity.update(0, 0, 0)
    rotation.update(0, 0)


def full_reset() -> None:
    global remaining_enemies, hidden_enemies, played_once
    respawn()
    enemies[:] = [
        (*random_enemy(), pygame.Vector2(), [0])
        for _ in range(ENEMY_COUNT)
    ]
    remaining_enemies = ENEMY_COUNT + HIDDEN_ENEMY_COUNT
    hidden_enemies = HIDDEN_ENEMY_COUNT
    played_once = True


def random_enemy() -> tuple[pygame.Vector3, list[float]]:
    return pygame.Vector3(random.uniform(-20, 20), random.uniform(7, 13), random.uniform(-35, 35)), [random.uniform(0, 15.0)]


def redraw_level() -> None:
    LEVEL.reset_draw_list()
    clear_circle_display_lists()
    LEVEL.draw_compile()


def raycast() -> Optional[int]:
    direction_vector = (pygame.Vector3(0, 0, 1)
        .rotate(rotation.x, pygame.Vector3(1, 0, 0))
        .rotate(-rotation.y, pygame.Vector3(0, 1, 0))
    )
    ray = position + pygame.Vector3(0, 1.8, 0)
    for _ in range(50):
        # draw_circle(ray, rotation, 0.25, 5)
        for (eix, (enemy, _, _, _)) in enumerate(enemies):
            if enemy.distance_squared_to(ray) <= ENEMY_SIZE_SQUARED:
                return eix
        ray += direction_vector


try:
    import OpenGL_accelerate  # pyright: ignore [reportMissingImports]
except ImportError:
    print('PyOpenGL-accelerate is not installed. It is highly '
          'recommended that you install it, as it will significantly '
          'increase your framerate.')


enemies: list[tuple[pygame.Vector3, list[float], pygame.Vector2, list[int]]] = []
remaining_enemies: int = 0
hidden_enemies: int = 0
played_once = False


pygame.init()

window = pygame.display.set_mode((1280, 720), OPENGL | DOUBLEBUF | RESIZABLE, vsync=VSYNC)
pygame.display.set_caption('My Evil Twin')

resize_view(window.get_width(), window.get_height())

LEVEL.draw_compile()

glClearColor(0.5, 0.5, 1.0, 1.0)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glEnable(GL_DEPTH_TEST)

rotation = pygame.Vector2()
velocity = pygame.Vector3()
position = LEVEL.spawn.copy()

pygame.event.set_grab(True)
pygame.mouse.set_visible(False)
mouse_owned = True

clock = pygame.time.Clock()

running = True

on_ground = False

fps_vals = deque(maxlen=240)

keys_pressed: set[int] = set()

freecam = False
freecam_pos = pygame.Vector3()

ai_tick_time = 0

mouse_rel = pygame.Vector2()
while running:
    mouse_rel.update(0, 0)

    raw_delta = clock.tick(FPS) / 1000.0
    delta = min(raw_delta, 0.05)
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEMOTION:
            if mouse_owned:
                mouse_rel += event.rel
        elif event.type == KEYDOWN:
            keys_pressed.add(event.key)
            if event.key == K_SPACE:
                if not freecam:
                    if on_ground:
                        velocity.y = JUMP_SPEED
                        on_ground = False
            elif event.key == K_ESCAPE:
                pygame.mouse.set_visible(True)
                pygame.event.set_grab(False)
                mouse_owned = False
            elif event.key == K_EQUALS:
                set_global_color_offset(get_global_color_offset() + 1)
                redraw_level()
            elif event.key == K_MINUS:
                set_global_color_offset(get_global_color_offset() - 1)
                redraw_level()
            elif event.key == K_r:
                full_reset()
            elif event.key == K_g:
                freecam = not freecam
                if freecam:
                    freecam_pos = position.copy()
            elif event.key == K_1:
                rotation.y = 0
                rotation.x = 0
            elif event.key == K_2:
                rotation.y = 90
                rotation.x = 0
            elif event.key == K_3:
                rotation.y = 180
                rotation.x = 0
            elif event.key == K_4:
                rotation.y = -90
                rotation.x = 0
            elif event.key == K_5:
                rotation.y = 0
                rotation.x = 90
            elif event.key == K_6:
                rotation.y = 0
                rotation.x = -90
        elif event.type == KEYUP:
            keys_pressed.discard(event.key)
            if event.key == K_F11:
                pygame.display.toggle_fullscreen()
                resize_view(window.get_width(), window.get_height())
        elif event.type == MOUSEBUTTONDOWN:
            pygame.event.set_grab(True)
            pygame.mouse.set_visible(False)
            mouse_owned = True
            if event.button == 1:
                hit = raycast()
                if hit is not None:
                    print(hit, end=' ')
                    enemy_pos, color, enemy_vel, draw_list = enemies[hit]
                    if draw_list[0]:
                        glDeleteLists(draw_list[0], 1)
                    remaining_enemies -= 1
                    if hidden_enemies:
                        new_pos, new_color = random_enemy()
                        enemy_pos.update(new_pos)
                        enemy_vel.update(0, 0)
                        color[0] = new_color[0]
                        hidden_enemies -= 1
                        print('replaced')
                    else:
                        del enemies[hit]
                        print('gone')
                    draw_list[0] = 0
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
    if freecam:
        freecam_pos.x += movement.x * delta
        freecam_pos.z += movement.y * delta
        if K_SPACE in keys_pressed:
            freecam_pos.y += 10 * delta
        if K_LSHIFT in keys_pressed:
            freecam_pos.y -= 10 * delta
    else:
        velocity.x = movement.x
        velocity.z = movement.y

    fps = 1 / raw_delta if raw_delta else 1000
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
            respawn()
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

    ## DRAW WORLD
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glRotatef(rotation.x, 1, 0, 0)
    glRotatef(rotation.y + 180, 0, 1, 0)
    if freecam:
        glTranslatef(-freecam_pos.x, -freecam_pos.y - 1.8, -freecam_pos.z)
    else:
        glTranslatef(-position.x, -position.y - 1.8, -position.z)

    LEVEL.draw(rotation)
    ai_tick_time += delta
    while ai_tick_time > AI_TICK_TIME:
        for (enemy_pos, color, enemy_vel, draw_list) in enemies:
            if not enemy_vel:
                enemy_vel.update(pygame.Vector2(1, 0).rotate(random.uniform(-180, 180)))
            offset = (enemy_pos.xz - position.xz).as_polar()[1] - enemy_vel.as_polar()[1] + 180
            while offset > 180:
                offset -= 360
            while offset < -180:
                offset += 360
            if offset < 0:
                random_offset = random.uniform(offset, 30)
            else:
                random_offset = random.uniform(-30, offset)
            enemy_vel.rotate_ip(random_offset)
        ai_tick_time -= AI_TICK_TIME
    for (eix, (enemy_pos, color, enemy_vel, draw_list)) in enumerate(enemies):
        enemy_pos.update(pygame.Vector3(enemy_pos.x + enemy_vel.x * 3 * delta, enemy_pos.y - 0.25 * delta, enemy_pos.z + enemy_vel.y * 3 * delta))
        glPushMatrix()
        glTranslatef(enemy_pos.x, enemy_pos.y, enemy_pos.z)
        if not draw_list[0]:
            draw_list[0] = cast(int, glGenLists(1))
            glNewList(draw_list[0], GL_COMPILE)
            set_local_color_offset(color[0])
            draw_rectangle(pygame.Vector3(-0.3, -0.4, -0.3), pygame.Vector3(0.3, 0.4, 0.3))
            glEndList()
        glCallList(draw_list[0])
        glPopMatrix()
        # glBegin(GL_LINES)
        # glVertex3f(enemy_pos.x, enemy_pos.y, enemy_pos.z)
        # look_pos = pygame.Vector3(0, 0, 1).rotate(-enemy_vel.as_polar()[1] + 90, pygame.Vector3(0, 1, 0)) * 3 + enemy_pos
        # glVertex3f(look_pos.x, look_pos.y, look_pos.z)
        # glEnd()
        if enemy_pos.y <= 0:
            new_pos, new_color = random_enemy()
            enemy_pos.update(new_pos)
            enemy_vel.update(0, 0)
            color[0] = new_color[0]
            if draw_list[0]:
                glDeleteLists(draw_list[0], 1)
            draw_list[0] = 0
        if enemy_pos.distance_squared_to(position) <= ENEMY_SIZE_SQUARED:
            full_reset()
    if freecam:
        set_local_color_offset(0)
        draw_rectangle(position - pygame.Vector3(0.3, 0.0, 0.3), position + pygame.Vector3(0.3, 2.0, 0.3))
    ## END DRAW WORLD

    ## DRAW HUD
    w, h = screen_size.x / 4, screen_size.y / 4
    cx, cy = w / 2, h / 2
    glClear(GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, w, h, 0, 100, 300)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glTranslatef(0, 0, -200)
    glEnable(GL_TEXTURE_2D)

    draw_text(f'FPS/MIN: {fps_smooth_value:.1f}/{min_fps:.1f}', 2, 2, Color(255, 255, 255))
    draw_text(f'X/Y/Z: {position.x:.1f}/{position.y:.1f}/{position.z:.1f}', 2, 12, Color(255, 255, 255))
    draw_text(f'VX/VY/VZ: {velocity.x:.1f}/{velocity.y:.1f}/{velocity.z:.1f}', 2, 22, Color(255, 255, 255))
    draw_text(f'COLLIDING/GROUND: {collided}/{on_ground}', 2, 32, Color(255, 255, 255))
    draw_text(f'REMAINING: {remaining_enemies}', 2, 42, Color(255, 255, 255))

    if not remaining_enemies:
        if played_once:
            draw_centered_text('YOU WIN!', cx, cy - 14, Color(0, 200, 0))
            draw_centered_text('Press R to Play Again', cx, cy + 6, Color(0, 200, 200))
        else:
            draw_centered_text('Press R to Play', cx, cy - 14, Color(0, 200, 200))

    glDisable(GL_TEXTURE_2D)

    glLineWidth(3)
    glBegin(GL_LINES)
    glColor3f(1, 1, 1)
    glVertex2f(cx - 5, cy)
    glVertex2f(cx + 5, cy)
    glVertex2f(cx, cy - 5)
    glVertex2f(cx, cy + 5)
    glEnd()

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    ## END DRAW HUD

    pygame.display.flip()


LEVEL.close()
clear_circle_display_lists()
for (_, _, _, draw_list) in enemies:
    if draw_list[0]:
        glDeleteLists(draw_list[0], 1)
pygame.quit()
