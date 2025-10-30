import pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Music Player")

white = (255, 255, 255)
black = (0, 0, 0)

font = pygame.font.Font(None, 36)

songs = ["shokkyzdar.mp3", "Almatytyni.mp3", "Belyerozy.mp3"]
n = 0
play = False

clock = pygame.time.Clock()
run = True

while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_p:
                if not play:
                    pygame.mixer.music.load(songs[n])
                    pygame.mixer.music.play()
                    play = True
            if e.key == pygame.K_s:
                pygame.mixer.music.stop()
                play = False
            if e.key == pygame.K_n:
                n = (n + 1) % 3
                if play:
                    pygame.mixer.music.load(songs[n])
                    pygame.mixer.music.play()
            if e.key == pygame.K_b:
                n = (n - 1) % 3
                if play:
                    pygame.mixer.music.load(songs[n])
                    pygame.mixer.music.play()
    
    screen.fill(white)
    
    t = font.render(f"Now: {songs[n]}", True, black)
    screen.blit(t, (50, 100))
    
    c = font.render("P=Play S=Stop N=Next B=Back", True, black)
    screen.blit(c, (50, 200))
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
