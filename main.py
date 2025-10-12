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

SUBJECT_QUESTIONS = {
    "ЦГ": [
        ("Вы увидели в социальной сети шокирующее видео с громким заголовком, которое быстро набирает популярность. Что следует сделать в первую очередь, чтобы проверить достоверность этой информации?", ["Найти первоисточник видео, проверить его на независимых новостных сайтах и в факт-чекинговых сервисах", "Сразу поделиться видео у себя на странице, чтобы предупредить друзей", "Поверить информации, так как видео набрало много просмотров и комментариев"], 1),
        ("Какое действие является самым безопасным при получении письма от незнакомого банка с просьбой «срочно перейти по ссылке и подтвердить данные вашей карты»?", ["Перейти по ссылке и ввести данные, чтобы проверить, настоящий ли это банк", "Ответить на письмо и спросить, кто отправитель", "Не переходить по ссылке, удалить письмо и, если есть беспокойство, позвонить в свой банк по официальному номеру с сайта"], 3),
        ("Что означает аббревиатура CSV (Comma-Separated Values), часто используемая для хранения данных?", ["Это специализированная база данных, которую можно открыть только в дорогих программах", "Это текстовый формат, где данные разделены запятыми, и его можно открыть в обычном текстовом редакторе или Excel", "Это формат для хранения зашифрованных и защищенных паролем файлов"], 2),
    ],
    "Дискретная математика": [
        ("Пусть A = {1, 2, 3}, B = {3, 4, 5}. Чему равно множество A ∩ B (пересечение A и B)?", ["{1, 2, 3, 4, 5}", "{3}", "{1, 2}"], 2),
        ("Для любого универсального множества U и любого множества A, каково будет результат операции A ∪ ∅ (объединение A с пустым множеством)?", ["U (универсальное множество)", "∅ (пустое множество)", "A"], 3),
        ("Даны множества X = {a, b, c} и Y = {c, d, e}. Чему равно множество X \ Y (разность X и Y)?", ["{a, b}", "{c}", "{a, b, d, e}"], 1),
    ],
    "Линейная алгебра": [
        ("Что является необходимым условием для умножения двух матриц A и B (чтобы произведение A·B было определено)?", ["Матрицы A и B должны быть квадратными одного размера", "Количество строк матрицы A должно равняться количеству столбцов матрицы B", " Количество столбцов матрицы A должно равняться количеству строк матрицы"], 3),
        ("Чему равен определитель произведения двух квадратных матриц A и B одного порядка?", ["det(A·B) = det(A) + det(B)", "det(A·B) = det(A) · det(B)", "det(A·B) = det(A) - det(B)"], 2),
        ("Если для квадратной матрицы A существует обратная матрица A⁻¹, то какое из следующих равенств является верным?", ["A · A⁻¹ = A⁻¹ · A = E, где E — единичная матрица", "A · A⁻¹ = 0 (нулевая матрица)", "A · A⁻¹ = A"], 1),
    ]
}

def draw_menu(selected_tab):
    screen.fill(color_sky)
    title = FONT.render("Маршрутка до Вышки", True, (0, 0, 0))
    screen.blit(title, (WIDTH // 2 - 140, 150))

    options = ["Начать игру", "О разработчиках", "Выход"]
    for i, opt in enumerate(options):
        color = (255, 255, 255) if i == selected_tab else (220, 220, 220)
        pygame.draw.rect(screen, color, (WIDTH // 2 - 120, 250 + i * 60, 240, 40))
        text = FONT.render(opt, True, (0, 0, 0))
        screen.blit(text, (WIDTH // 2 - 100, 260 + i * 60))
    pygame.display.flip()

def draw_developers():
    screen.fill((240, 240, 255))
    title = FONT.render("О разработчиках", True, (0, 0, 0))
    devs = [
        "Гребенник Артур",
        "Денисов Сергей",
        "Таранова Виталина",
         "Егоров Даниил",
        "Маркелов Матвей"
    ]
    screen.blit(title, (WIDTH // 2 - 120, 100))
    for i, d in enumerate(devs):
        screen.blit(FONT.render(d, True, (0, 0, 0)), (WIDTH // 2 - 120, 200 + i * 40))
    screen.blit(FONT.render("Нажмите ESC, чтобы вернуться", True, (80, 80, 80)), (WIDTH // 2 - 200, 400))
    pygame.display.flip()

def draw_victory_screen(player):
    screen.fill((200, 255, 200))
    text = FONT.render("ПОБЕДА!", True, (0, 100, 0))
    msg = FONT.render("Вы успешно дошли до Вышки и сдали тест!", True, (0, 0, 0))
    screen.blit(text, (WIDTH // 2 - 80, 200))
    screen.blit(msg, (WIDTH // 2 - 280, 260))
    screen.blit(FONT.render("Нажмите Enter, чтобы вернуться в меню", True, (0, 0, 0)), (WIDTH // 2 - 300, 350))
    pygame.display.flip()

    if player.victory_sound:
        player.victory_sound.play()

def draw_game_over():
    screen.fill((255, 200, 200))
    text = FONT.render("ПОРАЖЕНИЕ!", True, (100, 0, 0))
    msg = FONT.render("Маршрутка не доехала до Вышки...", True, (0, 0, 0))
    screen.blit(text, (WIDTH // 2 - 100, 200))
    screen.blit(msg, (WIDTH // 2 - 220, 260))
    screen.blit(FONT.render("Нажмите Enter, чтобы попробовать снова", True, (0, 0, 0)), (WIDTH // 2 - 320, 350))
    pygame.display.flip()

def draw_subject_selection():
    screen.fill((240, 240, 255))
    text = FONT.render("Выберите предмет:", True, (0, 0, 0))
    subjects = ["ЦГ", "Дискра", "Лианал"]
    screen.blit(text, (WIDTH // 2 - 100, 150))
    for i, subj in enumerate(subjects):
        pygame.draw.rect(screen, (200, 200, 255), (WIDTH // 2 - 100, 220 + i * 60, 200, 40))
        screen.blit(FONT.render(f"{i+1}) {subj}", True, (0, 0, 0)), (WIDTH // 2 - 80, 230 + i * 60))
    pygame.display.flip()


level = Level(screen, WIDTH, HEIGHT)
if __name__ == "__main__":
    main()
