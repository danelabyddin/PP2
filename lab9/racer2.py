import pygame, sys
from pygame.locals import *
import random

pygame.init()

#звук столкновения
crash_sound = pygame.mixer.Sound("crash.wav")

#частота
FPS = 60
clock = pygame.time.Clock()

#цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#окно
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

#фон
road_img = pygame.image.load("AnimatedStreet.png")
road_img = pygame.transform.scale(road_img, (WIDTH, HEIGHT))

#шрифт
font = pygame.font.Font(None, 36)

#счёт монет
coins_collected = 0


#игрок
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #загружаю изображение машины игрока
        self.image = pygame.image.load("Player.png")
        self.image = pygame.transform.scale(self.image, (50, 100))
        self.rect = self.image.get_rect(center=(WIDTH // 2, 520))

    def update(self):
        #управление стрелками
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5
        if keys[K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += 5


#враг
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #загружаю машину врага
        self.image = pygame.image.load("Enemy.png")
        self.image = pygame.transform.scale(self.image, (50, 100))
        #случайная позиция появления сверху
        self.rect = self.image.get_rect(center=(random.randint(40, WIDTH - 40), 0))
        self.speed = 7  #базовая скорость врага

    def update(self):
        #движение врага вниз
        self.rect.y += self.speed
        #когда уходит за экран появляется снова сверху
        if self.rect.top > HEIGHT:
            self.rect.center = (random.randint(40, WIDTH - 40), 0)


# монета
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # загружаю картинку монеты
        self.image = pygame.image.load("coin.png")
        self.image = pygame.transform.scale(self.image, (35, 35))
        # позиция появления
        self.rect = self.image.get_rect(center=(random.randint(40, WIDTH - 40), -50))
        self.speed = 5

        # вес монеты — сколько очков она даёт
        self.weight = random.choice([1, 3, 5])

    def update(self):
        # монета падает вниз
        self.rect.y += self.speed

        # если вышла за экран появляется заново
        if self.rect.top > HEIGHT:
            self.respawn()

    def respawn(self):
        #сохраняю функцию чтобы переиспользовать
        self.rect.center = (random.randint(40, WIDTH - 40), -50)
        #новый вес монеты каждый раз
        self.weight = random.choice([1, 3, 5])


#создаём объекты
player = Player()
enemy = Enemy()
coin = Coin()

all_sprites = pygame.sprite.Group(player, enemy, coin)
enemies = pygame.sprite.Group(enemy)
coins = pygame.sprite.Group(coin)


#игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    #обновляем объекты
    all_sprites.update()

    #сстолкновение с врагом — игра окончена
    if pygame.sprite.spritecollide(player, enemies, False):
        crash_sound.play()
        print("Game Over! Coins:", coins_collected)
        pygame.time.delay(1000)
        pygame.quit()
        sys.exit()

    #столкновение с монетой
    if pygame.sprite.spritecollide(player, coins, False):
        coins_collected += coin.weight  #добавляю очки по весу монеты
        coin.respawn()  #создаю новую монету

        # каждые 10 очков увеличение скорости врага
        if coins_collected % 10 == 0:
            enemy.speed += 1

    #рисую фон
    screen.blit(road_img, (0, 0))

    #рисую объекты
    all_sprites.draw(screen)

    #вывод счёта
    text = font.render(f"Coins: {coins_collected}", True, BLACK)
    screen.blit(text, (WIDTH - text.get_width() - 10, 10))

    #обновляем экран
    pygame.display.update()
    clock.tick(FPS)
