import pygame

pygame.init()

#размеры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

#цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#заливка фона
screen.fill(WHITE)

#текущие настройки
current_color = BLACK
tool = "brush"         # brush, eraser, rect, circle, square, tri_right, tri_eq, rhombus
brush_size = 5
drawing = False
start_pos = None

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #нажали мышь
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

        #отпустили мышь
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            x1, y1 = start_pos
            x2, y2 = end_pos

            #прямоугольник
            if tool == "rect":
                pygame.draw.rect(screen, current_color,
                                 (x1, y1, x2 - x1, y2 - y1), 2)

            #круг
            if tool == "circle":
                radius = int(((x2 - x1)**2 + (y2 - y1)**2) ** 0.5 / 2)
                center = ((x1 + x2) // 2, (y1 + y2) // 2)
                pygame.draw.circle(screen, current_color, center, radius, 2)

            #квадрат
            if tool == "square":
                side = min(abs(x2 - x1), abs(y2 - y1))
                pygame.draw.rect(screen, current_color,
                                 (x1, y1, side, side), 2)

            #прямоугольный треугольник
            if tool == "tri_right":
                points = [(x1, y1), (x1, y2), (x2, y2)]
                pygame.draw.polygon(screen, current_color, points, 2)

            #рпавносторонний треугольник
            if tool == "tri_eq":
                side = abs(x2 - x1)
                h = int((3**0.5 / 2) * side)
                points = [
                    (x1, y2),
                    (x1 + side, y2),
                    (x1 + side / 2, y2 - h)
                ]
                pygame.draw.polygon(screen, current_color, points, 2)

            #ромб
            if tool == "rhombus":
                w = abs(x2 - x1)
                h = abs(y2 - y1)
                points = [
                    (x1 + w // 2, y1),        # верх
                    (x2, y1 + h // 2),        # право
                    (x1 + w // 2, y2),        # низ
                    (x1, y1 + h // 2)         # лево
                ]
                pygame.draw.polygon(screen, current_color, points, 2)

        #выбор инструмента и цвета
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                tool = "brush"
            if event.key == pygame.K_e:
                tool = "eraser"
            if event.key == pygame.K_r:
                tool = "rect"
            if event.key == pygame.K_c:
                tool = "circle"
            if event.key == pygame.K_s:
                tool = "square"
            if event.key == pygame.K_t:
                tool = "tri_right"
            if event.key == pygame.K_q:
                tool = "tri_eq"
            if event.key == pygame.K_h:
                tool = "rhombus"

            #цвета
            if event.key == pygame.K_1:
                current_color = RED
            if event.key == pygame.K_2:
                current_color = GREEN
            if event.key == pygame.K_3:
                current_color = BLUE

            #очистка экрана
            if event.key == pygame.K_SPACE:
                screen.fill(WHITE)

    #кисть и ластик в движении
    if drawing and tool == "brush":
        pygame.draw.circle(screen, current_color, pygame.mouse.get_pos(), brush_size)

    if drawing and tool == "eraser":
        pygame.draw.circle(screen, WHITE, pygame.mouse.get_pos(), brush_size)

    pygame.display.update()

pygame.quit()
