"""
Шарики!
Лучшая игра, которую вы когда-либо видели, явно не эта.
Наслаждайтесь!
"""

# Импортирование библиотек.
import pygame
from pygame.draw import *
from random import randint

# Инициализация и первичная настройка pygame.
pygame.init()

FPS = 120
screen_w = 1600
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
    Задает случайные скорости.
    :param min_speed: Минимальная скорость.
    :param max_speed: Максимальная скорость.
    :return: speed_x, speed_y.
    """
    return randint(min_speed, max_speed) * (randint(0, 1) * 2 - 1), \
        randint(min_speed, max_speed) * (randint(0, 1) * 2 - 1)


def new_ball(balls):
    """
    Создает новый шар, не пересекающий старые.
    :param balls: Список шаров.
    :return: Список следующих параметров шара:
    [0] = x, [1] = y, [2] = r, [3] = color, [4] = speed_x, [5] = speed_y, [6] - is_clicked, [7] - is_strange.
    """
    intersection = True
    x, y, r = 0, 0, 0
    while intersection:
        x = randint(100, 1100)
        y = randint(100, 800)
        r = randint(25, 50)
        intersection = False
        for ball in balls:
            if (ball[0] - x) ** 2 + (ball[1] - y) ** 2 <= (ball[2] + r) ** 2:
                intersection = True
    color = COLORS[randint(0, 5)]

    speed_x, speed_y = random_speed()           # Скорости по осям x и y.
    is_clicked = False                          # Кликнули ли на шарик.
    is_strange = randint(0, randint(0, 1))      # Задает новый тип поведения, если 1.
    return [x, y, r, color, speed_x, speed_y, is_clicked, is_strange]


def show_moves(index, balls):
    """
    Реализует движение шаров. Если шар кликнут, создает новый.
    :index: Индекс изменившегося шара.
    :param balls: Список шаров.
    """
    ball = balls[index]
    if not ball[6]:
        if ball[7]:
            ball[2] = randint(max(10, ball[2] - 1), min(50, ball[2] + 1))
            ball[4] = randint(max(-12, ball[4] - 1), min(ball[4] + 1, 12))
            ball[5] = randint(max(-12, ball[5] - 1), min(ball[5] + 1, 12))
        ball[0] += ball[4]
        ball[1] += ball[5]
        circle(screen, ball[3], (ball[0], ball[1]), ball[2])
    else:
        balls[index] = new_ball(balls)


def check_collisions_with_walls(ball):
    """
    Проверяет столкновения с границами экрана.
    :param ball: Шар, который проверяется.
    """
    while ball[0] + ball[4] - screen_w > -ball[2] or ball[0] + ball[4] < ball[2] or \
            ball[1] + ball[5] - screen_h > -ball[2] or ball[1] + ball[5] < ball[2]:
        ball[4], ball[5] = random_speed()


def check_collisions_with_balls(index, balls):
    """
    Проверяет столкновения с другими шариками.
    :param index: Индекс шарика, у с которым проверяется.
    :param balls: Массив шаров.
    """
    ball1 = balls[index]
    for j in range(len(balls)):
        ball2 = balls[j]
        if i != j and (ball1[0] - ball2[0]) ** 2 + (ball1[1] - ball2[1]) ** 2 <= (ball1[2] + ball2[2]) ** 2:
            ball1[4], ball2[4] = ball2[4], ball1[4]
            ball1[5], ball2[5] = ball2[5], ball1[5]
            ball1[0] += ball1[4]
            ball1[1] += ball1[5]
            ball2[0] += ball2[4]
            ball2[1] += ball2[5]
            break


def click(click_event, ball):
    """
    Проверяет, попал ли клик мышки в мишень.
    :param click_event: Событие клика.
    :param ball: Объект, на котором проверяется клик.
    :return: True или False.
    """
    mouse_x = click_event.pos[0]
    mouse_y = click_event.pos[1]
    return (ball[0] - mouse_x) ** 2 + (ball[1] - mouse_y) ** 2 <= ball[2] ** 2


def score_counter(click_event, balls, score):
    """
    Считает очки.
    :param click_event: Событие клика.
    :param balls: Список шаров.
    :param score: Очки.
    :return: Очки.
    """
    for ball in balls:
        if click(click_event, ball):
            ball[6] = True
            score += 2*ball[7] + 1              # Добавляет очки в зависимости от типа шара.
            break
    return score


# Оснвные переменные.
ball_number = 15                                # Количество шаров (НЕ БОЛЬШЕ 15).
score_int = 0                                   # Очки.

# Список шаров и его изначальное пополнение.
list_of_balls = []
for i in range(ball_number):
    list_of_balls.append(new_ball(list_of_balls))

# Основная исполняющая часть.
pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            score_int = score_counter(event, list_of_balls, score_int)

    for i in range(len(list_of_balls)):
        ball = list_of_balls[i]
        check_collisions_with_balls(i, list_of_balls)
        check_collisions_with_walls(ball)
        show_moves(i, list_of_balls)

    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()

print(f"Игра окончена.\nПоздравляю! Вы набрали {score_int} очков.")
