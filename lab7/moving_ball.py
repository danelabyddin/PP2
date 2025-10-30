import pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Moving Ball")

white = (255, 255, 255)
red = (255, 0, 0)
x = 400
y = 300

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        if x - 20 >= 25:
            x -= 20
    if keys[pygame.K_RIGHT]:
        if x + 20 <= 775:
            x += 20
    if keys[pygame.K_UP]:
        if y - 20 >= 25:
            y -= 20
    if keys[pygame.K_DOWN]:
        if y + 20 <= 575:
            y += 20
    
    screen.fill(white)
    
    pygame.draw.circle(screen, red, (x, y), 25)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()