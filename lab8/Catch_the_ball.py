"""
Шарики!
Лучшая игра, которую вы когда-либо видели, явно не эта.
Наслаждайтесь!
"""

# Импортирование библиотек
import pygame
from pygame.draw import *
from random import randint

# Запрос имени
print("Добро пожаловать в нашу замечательную игру!\nВведите ваше имя: ")
# nickname = input()

# Инициализация и первичная настройка pygame
pygame.init()

FPS = 30
screen_w = 1200
screen_h = 900
screen = pygame.display.set_mode((screen_w, screen_h))

# Цвета
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


def random_speed(min_speed=2, max_speed=12):
    """
    Задает случайные скорости
    :param min_speed: Минимальная скорость
    :param max_speed: Максимальная скорость
    :return: speed_x, speed_y
    """
    return randint(min_speed, max_speed) * (randint(0, 1) * 2 - 1), \
        randint(min_speed, max_speed) * (randint(0, 1) * 2 - 1)


def new_ball(balls):
    """
    Создает новый шар, не пересекающий старые.
    :param balls: Список шаров
    :return: Список следующих параметров шара:
    [0] = x, [1] = y, [2] = r, [3] = color, [4] = speed_x, [5] = speed_y, [6] - is_hit
    """

    intersection = True
    x, y, r = 0, 0, 0
    while intersection:
        x = randint(100, 1100)
        y = randint(100, 800)
        r = randint(30, 50)
        intersection = False
        for i in range(len(balls)):
            if (balls[i][0] - x) ** 2 + (balls[i][1] - y) ** 2 <= (balls[i][2] + r) ** 2:
                intersection = True

    color = COLORS[randint(0, 5)]
    speed_x, speed_y = random_speed()
    is_hit = False
    return [x, y, r, color, speed_x, speed_y, is_hit]


def show_moves(balls):
    """
    Реализует движение шаров. Если шар кликнут, создает новый(ЕЩЕ НЕ РЕАЛИЗОВАНО).
    :param balls: Список шаров
    """
    for ball in balls:
        if not ball[6]:
            ball[0] += ball[4]
            ball[1] += ball[5]
            circle(screen, ball[3], (ball[0], ball[1]), ball[2])
        else:
            ball = new_ball(balls)
            ball[4], ball[5] = random_speed()


def check_collisions_with_walls(balls):
    """
    Проверяет столкновения с границами экрана.
    :param balls: Список шаров
    """
    for ball in balls:
        while ball[0] + ball[4] - screen_w > -ball[2] or ball[0] + ball[4] < ball[2] or \
                ball[1] + ball[5] - screen_h > -ball[2] or ball[1] + ball[5] < ball[2]:
            ball[4], ball[5] = random_speed()


def click():
    pass


# Оснвные переменные
ball_number = 10  # Количество шаров
score = 0  # Очки

# Список шаров и его изначальное пополнение
balls = []
for i in range(ball_number):
    balls.append(new_ball(balls))

# Основная исполняющая часть
pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass
    check_collisions_with_walls(balls)
    show_moves(balls)

    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()

print(f"Игра окончена.\nПоздравляю! Вы набрали {score} очков.")
