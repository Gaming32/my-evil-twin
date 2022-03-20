import pygame
from pygame.locals import *
from OpenGL.GL import *


pygame.init()

window = pygame.display.set_mode((1280, 720), OPENGL | DOUBLEBUF)


clock = pygame.time.Clock()

running = True

glClearColor(0.5, 0.5, 1.0, 1.0)

while running:
    delta = clock.tick()
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    pygame.display.flip()
