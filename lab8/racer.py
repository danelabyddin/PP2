import pygame
import random
import sys

pygame.init()

#Музыка столкновения
crash_sound = pygame.mixer.Sound("crash.wav")

#Размер окна
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

clock = pygame.time.Clock()

#Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#Фон
road_img = pygame.image.load("AnimatedStreet.png")
road_img = pygame.transform.scale(road_img, (WIDTH, HEIGHT))

# Загружаем картинки машин и монеты
player_img = pygame.image.load("player.png")
player_img = pygame.transform.scale(player_img, (50, 100))

enemy_img = pygame.image.load("enemy.png")
enemy_img = pygame.transform.scale(enemy_img, (50, 100))

coin_img = pygame.image.load("coin.png")
coin_img = pygame.transform.scale(coin_img, (35, 35))

#Позиции игрока
player_x = WIDTH // 2
player_y = HEIGHT - 120

#Позиции врага
enemy_x = random.randint(40, WIDTH - 40)
enemy_y = 0

#Позиции монеты
coin_x = random.randint(40, WIDTH - 40)
coin_y = -150

# Счетчик монет
coins_collected = 0

# Шрифт
font = pygame.font.Font(None, 36)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Управление игроком
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= 5
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_img.get_width():
        player_x += 5

    # Движение врага
    enemy_y += 7
    if enemy_y > HEIGHT:
        enemy_y = 0
        enemy_x = random.randint(40, WIDTH - 40)

    # Движение монеты
    coin_y += 5
    if coin_y > HEIGHT:
        coin_y = -50
        coin_x = random.randint(40, WIDTH - 40)

    # Прямоугольники для столкновений
    player_rect = pygame.Rect(player_x, player_y, player_img.get_width(), player_img.get_height())
    enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_img.get_width(), enemy_img.get_height())
    coin_rect = pygame.Rect(coin_x, coin_y, coin_img.get_width(), coin_img.get_height())

    # Столкновение с врагом
    if player_rect.colliderect(enemy_rect):
        crash_sound.play()  # играем звук
        print("Game Over! Coins:", coins_collected)
        pygame.time.delay(1000)
        pygame.quit()
        sys.exit()

    # Собрали монету
    if player_rect.colliderect(coin_rect):
        coins_collected += 1
        coin_y = -50
        coin_x = random.randint(40, WIDTH - 40)

    # Рисуем фон дороги
    screen.blit(road_img, (0, 0))

    # Рисуем объекты
    screen.blit(player_img, (player_x, player_y))
    screen.blit(enemy_img, (enemy_x, enemy_y))
    screen.blit(coin_img, (coin_x, coin_y))

    # Текст с количеством монет
    text = font.render("Coins: " + str(coins_collected), True, BLACK)
    screen.blit(text, (WIDTH - text.get_width() - 10, 10))

    pygame.display.update()
    clock.tick(60)
