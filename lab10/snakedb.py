import pygame
import random
import psycopg2
import sys

pygame.init()


c = psycopg2.connect(
    host="localhost",
    database="snake_game", 
    user="danelabyddin", 
    password="2006")
cur = c.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS u (n VARCHAR(50) PRIMARY KEY, l INT)")
cur.execute("CREATE TABLE IF NOT EXISTS sc (n VARCHAR(50), p INT, l INT)")
c.commit()


n = input("Username: ")
cur.execute("SELECT l FROM u WHERE n=%s", (n,))
r = cur.fetchone()
if r:
    l = r[0]
else:
    l = 1
    cur.execute("INSERT INTO u VALUES (%s,%s)", (n,l))
    c.commit()


w = 600
hgt = 600
cell = 20
screen = pygame.display.set_mode((w,hgt))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()


BLACK = (0,0,0)
GREEN = (0,200,0)
RED = (200,0,0)
WHITE = (255,255,255)
YELLOW = (255,255,0)
ORANGE = (255,140,0)

#змейка и направление
snake = [(10,10)]
dx = 1
dy = 0

score = 0
speed = 5 + l
pause = False
game_over = False
show_level_text = 0

font = pygame.font.SysFont(None,30)
big_font = pygame.font.SysFont(None,60)

#появление еды
def spawn_food():
    while True:
        x = random.randint(0,(w//cell)-1)
        y = random.randint(0,(hgt//cell)-1)
        if (x,y) not in snake:
            break
    weight = random.choice([1,2,5])
    if weight == 1: color = RED
    elif weight == 2: color = ORANGE
    else: color = YELLOW
    timer = random.randint(60,120)
    return x,y,weight,color,timer

food_x,food_y,food_w,food_c,food_timer = spawn_food()

while True:
    screen.fill(BLACK)

    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            cur.execute("INSERT INTO sc VALUES (%s,%s,%s)", (n,score,l))
            c.commit()
            pygame.quit()
            sys.exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_UP and dy != 1: dx,dy = 0,-1
            if e.key == pygame.K_DOWN and dy != -1: dx,dy = 0,1
            if e.key == pygame.K_LEFT and dx != 1: dx,dy = -1,0
            if e.key == pygame.K_RIGHT and dx != -1: dx,dy = 1,0
            if e.key == pygame.K_p:
                cur.execute("INSERT INTO sc VALUES (%s,%s,%s)", (n,score,l))
                c.commit()
                pause = not pause
            if e.key == pygame.K_q:
                cur.execute("INSERT INTO sc VALUES (%s,%s,%s)", (n,score,l))
                c.commit()
                pygame.quit()
                sys.exit()

    if pause: continue

    #движение
    head_x,head_y = snake[0]
    head_x += dx
    head_y += dy
    head = (head_x,head_y)
    snake.insert(0,head)

    #столкновение со стеной или с собой
    if head_x < 0 or head_x >= w//cell or head_y < 0 or head_y >= hgt//cell or head in snake[1:]:
        cur.execute("INSERT INTO sc VALUES (%s,%s,%s)", (n,score,l))
        c.commit()
        pygame.quit()
        sys.exit()

    #съели еду
    if (head_x,head_y) == (food_x,food_y):
        score += food_w
        if score % 4 == 0:
            l += 1
            speed += 1
            show_level_text = 30
            cur.execute("UPDATE u SET l=%s WHERE n=%s",(l,n))
            c.commit()
        food_x,food_y,food_w,food_c,food_timer = spawn_food()
    else:
        snake.pop()

    #таймер исчезновения еды
    food_timer -= 1
    if food_timer <= 0:
        food_x,food_y,food_w,food_c,food_timer = spawn_food()

    #рисуем змейку
    for x,y in snake:
        pygame.draw.rect(screen,GREEN,(x*cell,y*cell,cell,cell))

    #рисуем еду
    pygame.draw.rect(screen,food_c,(food_x*cell,food_y*cell,cell,cell))

    #текст очков и уровня
    text = font.render(f"Score: {score}   Level: {l}", True, WHITE)
    screen.blit(text,(10,10))

    #всплывающий текст
    if show_level_text > 0:
        level_text = big_font.render("LEVEL UP!",True,YELLOW)
        screen.blit(level_text,(w//2-120,hgt//2-30))
        show_level_text -= 1

    pygame.display.update()
    clock.tick(speed)
