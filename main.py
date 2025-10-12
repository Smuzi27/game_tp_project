import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Маршрутка к вузу")

# Основные цвета
SKY_BLUE = (135, 206, 235)
ROAD_GRAY = (50, 50, 50)

clock = pygame.time.Clock()


def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(SKY_BLUE)
        pygame.draw.rect(screen, ROAD_GRAY, (0, HEIGHT - 100, WIDTH, 100))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
