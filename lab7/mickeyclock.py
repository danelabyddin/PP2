import pygame
import datetime
pygame.init()
screen = pygame.display.set_mode((1400, 1050))
pygame.display.set_caption("Mickey Clock")

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

clock_face = pygame.image.load("base_micky.jpg")
minute_hand = pygame.image.load("minute.png") 
second_hand = pygame.image.load("second.png")

screen_center_x = 700
screen_center_y = 525
face_center_x = clock_face.get_width() // 2
face_center_y = clock_face.get_height() // 2

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    current_time = datetime.datetime.now()
    minutes = current_time.minute
    seconds = current_time.second
    
    m_angle = -((minutes + seconds/60) * 6)
    s_angle = -(seconds * 6)
    
    screen.fill(white)
    screen.blit(clock_face, (screen_center_x - face_center_x, screen_center_y - face_center_y))
    
    rotated_minute = pygame.transform.rotate(minute_hand, m_angle)
    minute_rect = rotated_minute.get_rect(center=(screen_center_x, screen_center_y))
    screen.blit(rotated_minute, minute_rect)
    
    rotated_second = pygame.transform.rotate(second_hand, s_angle)
    second_rect = rotated_second.get_rect(center=(screen_center_x, screen_center_y))
    screen.blit(rotated_second, second_rect)
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()