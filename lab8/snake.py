import pygame
import random

pygame.init()

# Размер окна
WIDTH = 600
HEIGHT = 600

# Размер клетки
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

# Цвета
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Начальная змейка и направление
snake = [(10, 10)]
dx = 1
dy = 0

# Функция появления еды
def spawn_food():
    while True:
        x = random.randint(0, (WIDTH // CELL) - 1)
        y = random.randint(0, (HEIGHT // CELL) - 1)
        if (x, y) not in snake:
            return (x, y)

food = spawn_food()

score = 0
level = 1
speed = 5   # начальная скорость

font = pygame.font.SysFont(None, 30)
big_font = pygame.font.SysFont(None, 60)

running = True
game_over = False
show_level_text = 0   # время показа "LEVEL UP!"

while running:
    screen.fill(BLACK)

    # Обработка клавиш
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and dy != 1:
                dx, dy = 0, -1
            elif event.key == pygame.K_DOWN and dy != -1:
                dx, dy = 0, 1
            elif event.key == pygame.K_LEFT and dx != 1:
                dx, dy = -1, 0
            elif event.key == pygame.K_RIGHT and dx != -1:
                dx, dy = 1, 0

    if not game_over:
        head_x, head_y = snake[0]
        head_x += dx
        head_y += dy

        #Столкновение со стеной
        if head_x < 0 or head_x >= WIDTH // CELL or head_y < 0 or head_y >= HEIGHT // CELL:
            game_over = True

        #Столкновение с собой
        if (head_x, head_y) in snake:
            game_over = True

        snake.insert(0, (head_x, head_y))

        # Съели еду
        if (head_x, head_y) == food:
            score += 1

            # Повышаем уровень каждое 4-е очко
            if score % 4 == 0:
                level += 1
                speed += 1       # змейка теперь быстрее
                show_level_text = 30   # показать LEVEL UP примерно на 0.5 сек

            food = spawn_food()
        else:
            snake.pop()

        # Рисуем змейку
        for x, y in snake:
            pygame.draw.rect(screen, GREEN, (x * CELL, y * CELL, CELL, CELL))

        # Рисуем еду
        fx, fy = food
        pygame.draw.rect(screen, RED, (fx * CELL, fy * CELL, CELL, CELL))

    #Текст очков и уровня
    text = font.render(f"Score: {score}   Level: {level}", True, WHITE)
    screen.blit(text, (10, 10))

    #Всплывающий текст LEVEL UP
    if show_level_text > 0:
        level_text = big_font.render("LEVEL UP!", True, YELLOW)
        screen.blit(level_text, (WIDTH//2 - 120, HEIGHT//2 - 30))
        show_level_text -= 1

    # Экран Game Over
    if game_over:
        over_text = font.render("GAME OVER (Press Q to Quit)", True, WHITE)
        screen.blit(over_text, (160, 280))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            running = False

    pygame.display.update()
    clock.tick(speed)

pygame.quit()