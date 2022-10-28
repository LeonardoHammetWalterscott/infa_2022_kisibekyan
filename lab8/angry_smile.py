import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))
screen.fill((222, 222, 222))

#Тело смайлика
black = (0, 0, 0)
circle(screen, (230, 200, 0), (200, 175), 100)
circle(screen, black, (200, 175), 100, 1)

#Глаза (Левый, Правый)
circle(screen, (255, 0, 0), (150, 150), 20)
circle(screen, black, (150, 150), 20, 1)
circle(screen, black, (150, 150), 10)

circle(screen, (255, 0, 0), (250, 150), 15)
circle(screen, black, (250, 150), 15, 1)
circle(screen, black, (250, 150), 7)

#Брови
polygon(screen, black, ((105, 100), (100, 110), (175, 150), (180, 140)))
polygon(screen, black, ((220, 140), (225, 148), (300, 118), (295, 110)))

#Рот
polygon(screen, black, ((150, 200), (150, 210), (250, 210), (250, 200)))

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
pygame.quit()