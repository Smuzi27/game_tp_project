import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Маршрутка к вузу")

SKY_BLUE = (135, 206, 235)
ROAD_GRAY = (50, 50, 50)

clock = pygame.time.Clock()


def main():
    running = True
    player_x = 0 #удалить потом

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            player_x += 5
        if keys[pygame.K_LEFT]:
            player_x -= 5

        # Камера следует за игроком
        level.camera_x = max(0, min(player_x - WIDTH // 2, level.world_width - WIDTH))

        screen.fill(SKY_BLUE)
        pygame.draw.rect(screen, ROAD_GRAY, (0, HEIGHT - 100, WIDTH, 100))
        level.draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


class Level:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.world_width = 2000
        self.platforms = [
            pygame.Rect(200, height - 150, 100, 20),
            pygame.Rect(500, height - 250, 150, 20),
            pygame.Rect(800, height - 200, 120, 20),
            pygame.Rect(1200, height - 180, 150, 20),
            pygame.Rect(1600, height - 220, 200, 20),
        ]
        self.finish = pygame.Rect(self.world_width - 150, height - 220, 80, 120)
        self.camera_x = 0

    def draw(self):
        for platform in self.platforms:
            rect = platform.move(-self.camera_x, 0)
            pygame.draw.rect(self.screen, (80, 80, 80), rect)

        finish_rect = self.finish.move(-self.camera_x, 0)
        pygame.draw.rect(self.screen, (200, 180, 255), finish_rect)
        pygame.draw.rect(self.screen, (100, 0, 150), finish_rect, 3)
        font = pygame.font.Font(None, 24)
        text = font.render("ВУЗ", True, (0, 0, 0))
        self.screen.blit(text, (finish_rect.x + 20, finish_rect.y + 40))


level = Level(screen, WIDTH, HEIGHT)
if __name__ == "__main__":
    main()
