# Импортирование библиотек
import math
from random import randint as rnd
from random import choice
import pygame

pygame.font.init()
my_font = pygame.font.SysFont('Sans Serif MS', 48)

# Количество кадров в секунду
FPS = 30

# Цвета игры
RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

# Разрешение окна игры
WIDTH = 1440
HEIGHT = 810

# Константы и переменные
Gravity = 1
score = 0


class Ball:
    def __init__(self, screen: pygame.Surface, obj):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = obj.x - 10
        self.y = obj.y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30
        self.wall_hit_counter = 0

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 1440x810).
        """
        if self.wall_hit_counter > 4:
            self.vx = 0
            self.vy = 0
            self.live = 0
        else:
            if self.x + self.vx + self.r > WIDTH or self.x + self.vx - self.r < 0:
                self.vx *= -0.5
                self.vy *= 0.7
            if self.y - self.vy + self.r > HEIGHT - 10:
                self.vy *= -0.5
                self.vx *= 0.7
                self.wall_hit_counter += 1
            self.x += self.vx
            self.y -= self.vy
            self.vy -= Gravity

    def draw(self):
        if self.live:
            pygame.draw.circle(
                self.screen,
                self.color,
                (self.x, self.y),
                self.r
            )

    def hit_test(self, obj):
        """Функция проверяет, сталкивается ли данный объект с целью, описываемой в объекте obj.

        Args:
            obj: Объект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.r + obj.r) ** 2 > (self.x - obj.x - obj.vx) ** 2 + (self.y - obj.y - obj.vy) ** 2:
            obj.live = 0
            return True
        return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.x = 20
        self.y = HEIGHT - 150
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen, gun)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targeting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1] - self.y) / (event.pos[0] - self.x))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        length = self.f2_power + 10
        width = 7
        pygame.draw.polygon(screen, self.color, [(self.x, self.y),
                            (self.x + length * math.cos(self.an), self.y + length * math.sin(self.an)),
                            (self.x + length * math.cos(self.an) + width * math.sin(self.an),
                            self.y + length * math.sin(self.an) - width * math.cos(self.an)),
                            (self.x + width * math.sin(self.an), self.y - width * math.cos(self.an))])

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = (150 - self.f2_power, 150 + self.f2_power, 150 - self.f2_power)
        else:
            self.color = GREY


class Target:
    def __init__(self, screen: pygame.Surface):
        """ Конструктор класса target
        """
        self.screen = screen
        self.x = rnd(int(0.4 * WIDTH), int(0.7 * WIDTH))
        self.y = rnd(int(0.4 * HEIGHT), int(0.7 * HEIGHT))
        self.vx = 3 * choice([1, -1]) * rnd(1, 5)
        self.vy = 3 * choice([1, -1]) * rnd(1, 5)
        self.r = rnd(WIDTH // 150, WIDTH // 50)
        self.live = 1
        self.points = 0
        self.color = RED


    def new_target(self):
        """ Инициализация новой цели. """
        self.x = rnd(int(0.4 * WIDTH), int(0.7 * WIDTH))
        self.y = rnd(int(0.4 * HEIGHT), int(0.7 * HEIGHT))
        self.r = rnd(WIDTH // 150, WIDTH // 50)
        self.vx = rnd(1, 2) * 3
        self.vy = rnd(1, 2) * 3

    def hit(self, score, points=1):
        """Попадание шарика в цель."""
        self.points += points
        score += points
        return score

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def move(self):
        if self.x + self.vx + self.r > WIDTH or self.x + self.vx - self.r < 0.3 * WIDTH:
            self.vx *= -1
            self.vy *= -1
        if self.y + self.vy + self.r > 0.8 * HEIGHT or self.y + self.vy - self.r < 20:
            self.vy *= -1
            self.vx *= -1
        self.x += self.vx
        self.y += self.vy


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)

target_number = 3
targets = []
for i in range(target_number):
    targets.append(Target(screen))

finished = False

while not finished:
    screen.fill(WHITE)
    score_text = my_font.render(f'Очки: {score}', False, (0, 0, 0))
    balls_text = my_font.render(f'Шаров запущено: {bullet}', False, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(balls_text, (10, 60))

    gun.draw()
    for t in targets:
        t.draw()
    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targeting(event)

    for b in balls:
        b.move()
        for t in targets:
            if b.hit_test(t):
                score = t.hit(score)
                t.new_target()
    for t in targets:
        t.move()
    gun.power_up()

pygame.quit()
