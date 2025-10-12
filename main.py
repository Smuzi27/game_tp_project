import pygame
import sys
import random
#пупупу

pygame.init()

WIDTH, HEIGHT = 2000, 600 #времено, чтобы видеть уровень
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

        # Декор
        self.clouds = [(random.randint(0, self.world_width), random.randint(50, 200)) for _ in range(8)]
        self.trees = [(120 * i, height - 150) for i in range(16)]

    def draw_background(self):
        # Облака
        for x, y in self.clouds:
            pygame.draw.ellipse(self.screen, (255, 255, 255), (x - self.camera_x, y, 120, 60))
        # Деревья
        for x, y in self.trees:
            pygame.draw.rect(self.screen, (101, 67, 33), (x - self.camera_x, y, 20, 60))
            pygame.draw.circle(self.screen, (34, 139, 34), (x - self.camera_x + 10, y), 30)

    def draw(self):
        self.draw_background()

        # Платформы
        for platform in self.platforms:
            rect = platform.move(-self.camera_x, 0)
            pygame.draw.rect(self.screen, (80, 80, 80), rect)

        # Здание вуза
        finish_rect = self.finish.move(-self.camera_x, 0)
        pygame.draw.rect(self.screen, (200, 180, 255), finish_rect)
        pygame.draw.rect(self.screen, (100, 0, 150), finish_rect, 3)
        font = pygame.font.Font(None, 24)
        text = font.render("ВУЗ", True, (0, 0, 0))
        self.screen.blit(text, (finish_rect.x + 20, finish_rect.y + 40))

class Player:
    def __init__(self, x, y):
        self.image = pygame.Surface((60, 30), pygame.SRCALPHA)
        self.draw_bus()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_y = 0
        self.on_ground = False
        self.lives = 3

    def draw_bus(self):
        # Корпус
        pygame.draw.rect(self.image, (255, 215, 0), (0, 0, 60, 30), border_radius=5)
        # Окна
        pygame.draw.rect(self.image, (173, 216, 230), (10, 5, 15, 10))
        pygame.draw.rect(self.image, (173, 216, 230), (35, 5, 15, 10))
        # Колёса
        pygame.draw.circle(self.image, (0, 0, 0), (15, 28), 6)
        pygame.draw.circle(self.image, (0, 0, 0), (45, 28), 6)

    def handle_input(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -15
            self.on_ground = False
            if self.jump_sound:
                self.jump_sound.play()

level = Level(screen, WIDTH, HEIGHT)
if __name__ == "__main__":
    main()

