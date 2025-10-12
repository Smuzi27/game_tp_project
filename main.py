import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 1000, 600  # времено, чтобы видеть уровень
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Маршрутка в Вышку")

SKY_BLUE = (135, 206, 235)
ROAD_GRAY = (50, 50, 50)

FONT = pygame.font.Font(None, 36)
clock = pygame.time.Clock()


class Level:
    def __init__(self, width, height):
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

        self.clouds = [[random.randint(0, self.world_width),
                        random.randint(50, 200),
                        random.uniform(0.3, 0.8)] for _ in range(6)]

        self.trees = [(120 * i, height - 150) for i in range(16)]

        self.obstacles = [
            pygame.Rect(400, height - 120, 40, 20),
            pygame.Rect(950, height - 120, 60, 20),
            pygame.Rect(1450, height - 120, 50, 20),
            pygame.Rect(1200, height - 120, 50, 20)
        ]

        try:
            self.emblem = pygame.image.load("assets/logo_hse.jpg")
            self.emblem = pygame.transform.scale(self.emblem, (80, 80))
        except:
            self.emblem = None


    def update(self):
        # Движение облаков (лево → право, зацикливается)
        for cloud in self.clouds:
            cloud[0] += cloud[2]
            if cloud[0] - self.camera_x > self.world_width + 200:
                cloud[0] = -200

    def draw_background(self, screen):
        # Облака
        for x, y, _ in self.clouds:
            pygame.draw.ellipse(screen, (255, 255, 255), (x - self.camera_x, y, 120, 60))
        # Деревья
        for x, y in self.trees:
            pygame.draw.rect(screen, (101, 67, 33), (x - self.camera_x, y, 20, 60))
            pygame.draw.circle(screen, (34, 139, 34), (x - self.camera_x + 10, y), 30)

    def draw(self, screen):
        self.draw_background(screen)
        for platform in self.platforms:
            pygame.draw.rect(screen, (80, 80, 80), platform.move(-self.camera_x, 0))
        for obs in self.obstacles:
            pygame.draw.rect(screen, (200, 50, 50), obs.move(-self.camera_x, 0))
        finish_rect = self.finish.move(-self.camera_x, 0)
        pygame.draw.rect(screen, (200, 180, 255), finish_rect)
        pygame.draw.rect(screen, (100, 0, 150), finish_rect, 3)
        if self.emblem:
            screen.blit(self.emblem, (finish_rect.x, finish_rect.y))
        else:
            screen.blit(FONT.render("ВШЭ", True, (0, 0, 0)), (finish_rect.x + 20, finish_rect.y + 40))


class Player:
    def __init__(self, x, y):
        self.image = pygame.Surface((60, 30), pygame.SRCALPHA)
        self.draw_bus()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_y = 0
        self.on_ground = False
        self.lives = 3
        # Звуки (наличие звуковых файлов)
        try:
            self.jump_sound = pygame.mixer.Sound("assets/jump.wav")
            self.hit_sound = pygame.mixer.Sound("assets/hit.wav")
            self.victory_sound = pygame.mixer.Sound("assets/win.wav")
        except:
            self.jump_sound = None
            self.hit_sound = None
            self.victory_sound = None

    def draw_bus(self):
        # Корпус
        pygame.draw.rect(self.image, (255, 215, 0), (0, 0, 60, 30), border_radius=5)
        # Окна
        pygame.draw.rect(self.image, (173, 216, 230), (10, 5, 15, 10))
        pygame.draw.rect(self.image, (173, 216, 230), (35, 5, 15, 10))
        # Колёса
        pygame.draw.circle(self.image, (0, 0, 0), (15, 28), 8)
        pygame.draw.circle(self.image, (0, 0, 0), (45, 28), 8)

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

    def apply_gravity(self):
        self.vel_y += 0.8
        if self.vel_y > 12:
            self.vel_y = 12
        self.rect.y += self.vel_y
        if self.rect.bottom >= HEIGHT - 100:
            self.rect.bottom = HEIGHT - 100
            self.vel_y = 0
            self.on_ground = True

    def check_collision(self, platforms, obstacles):
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.vel_y > 0 and self.rect.bottom <= platform.bottom:
                    self.rect.bottom = platform.top
                    self.vel_y = 0
                    self.on_ground = True
        for obs in obstacles:
            if self.rect.colliderect(obs):
                self.rect.x -= 50
                self.lives -= 1
                if self.hit_sound:
                    self.hit_sound.play()
                if self.lives < 0:
                    self.lives = 0

    def draw(self, screen, camera_x):
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y))



SUBJECT_QUESTIONS = {
    "ЦГ": [
        (
        "Вы увидели в социальной сети шокирующее видео с громким заголовком, которое быстро набирает популярность. Что следует сделать в первую очередь, чтобы проверить достоверность этой информации?",
        ["Найти первоисточник видео, проверить его на независимых новостных сайтах и в факт-чекинговых сервисах",
         "Сразу поделиться видео у себя на странице, чтобы предупредить друзей",
         "Поверить информации, так как видео набрало много просмотров и комментариев"], 1),
        (
        "Какое действие является самым безопасным при получении письма от незнакомого банка с просьбой «срочно перейти по ссылке и подтвердить данные вашей карты»?",
        ["Перейти по ссылке и ввести данные, чтобы проверить, настоящий ли это банк",
         "Ответить на письмо и спросить, кто отправитель",
         "Не переходить по ссылке, удалить письмо и, если есть беспокойство, позвонить в свой банк по официальному номеру с сайта"],
        3),
        ("Что означает аббревиатура CSV (Comma-Separated Values), часто используемая для хранения данных?",
         ["Это специализированная база данных, которую можно открыть только в дорогих программах",
          "Это текстовый формат, где данные разделены запятыми, и его можно открыть в обычном текстовом редакторе или Excel",
          "Это формат для хранения зашифрованных и защищенных паролем файлов"], 2),
    ],
    "Дискра": [
        ("Пусть A = {1, 2, 3}, B = {3, 4, 5}. Чему равно множество A ∩ B (пересечение A и B)?",
         ["{1, 2, 3, 4, 5}", "{3}", "{1, 2}"], 2),
        (
        "Для любого универсального множества U и любого множества A, каково будет результат операции A ∪ ∅ (объединение A с пустым множеством)?",
        ["U (универсальное множество)", "∅ (пустое множество)", "A"], 3),
        ("Даны множества X = {a, b, c} и Y = {c, d, e}. Чему равно множество X \ Y (разность X и Y)?",
         ["{a, b}", "{c}", "{a, b, d, e}"], 1),
    ],
    "Линал": [
        ("Что является необходимым условием для умножения двух матриц A и B (чтобы произведение A·B было определено)?",
         ["Матрицы A и B должны быть квадратными одного размера",
          "Количество строк матрицы A должно равняться количеству столбцов матрицы B",
          " Количество столбцов матрицы A должно равняться количеству строк матрицы"], 3),
        ("Чему равен определитель произведения двух квадратных матриц A и B одного порядка?",
         ["det(A·B) = det(A) + det(B)", "det(A·B) = det(A) · det(B)", "det(A·B) = det(A) - det(B)"], 2),
        (
        "Если для квадратной матрицы A существует обратная матрица A⁻¹, то какое из следующих равенств является верным?",
        ["A · A⁻¹ = A⁻¹ · A = E, где E — единичная матрица", "A · A⁻¹ = 0 (нулевая матрица)", "A · A⁻¹ = A"], 1),
    ]
}


def draw_menu(selected_tab):
    screen.fill(SKY_BLUE)
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
        screen.blit(FONT.render(f"{i + 1}) {subj}", True, (0, 0, 0)), (WIDTH // 2 - 80, 230 + i * 60))
    pygame.display.flip()


def run_test(subject):
    questions = SUBJECT_QUESTIONS[subject]
    correct = 0
    for q, options, answer in questions:
        asking = True
        while asking:
            screen.fill((255, 255, 240))
            screen.blit(FONT.render(q, True, (0, 0, 0)), (50, 150))
            for i, opt in enumerate(options):
                screen.blit(FONT.render(f"{i + 1}) {opt}", True, (0, 0, 0)), (80, 220 + i * 40))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                        chosen = int(event.unicode) - 1
                        if chosen == answer:
                            correct += 1
                        asking = False
                        break
    return correct >= len(questions) / 2


def main():
    level = Level(WIDTH, HEIGHT)
    player = Player(50, HEIGHT - 150)
    state = "menu"
    selected_tab = 0
    subject = None
    victory = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if state == "menu":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_tab = (selected_tab - 1) % 3
                    elif event.key == pygame.K_DOWN:
                        selected_tab = (selected_tab + 1) % 3
                    elif event.key == pygame.K_RETURN:
                        if selected_tab == 0:
                            state = "game"
                        elif selected_tab == 1:
                            state = "about"
                        elif selected_tab == 2:
                            pygame.quit()
                            sys.exit()

            elif state == "about":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    state = "menu"

            elif state == "subject_select":
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                        subject = ["ЦГ", "Дискра", "Линал"][int(event.unicode) - 1]
                        victory = run_test(subject)
                        state = "victory" if victory else "game_over"

            elif state in ["victory", "game_over"]:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    state = "menu"
                    player = Player(50, HEIGHT - 150)
                    level = Level(WIDTH, HEIGHT)

        if state == "menu":
            draw_menu(selected_tab)
        elif state == "about":
            draw_developers()
        elif state == "game":
            keys = pygame.key.get_pressed()
            player.handle_input(keys)
            player.apply_gravity()
            player.check_collision(level.platforms, level.obstacles)
            level.update()

            if player.lives <= 0:
                state = "game_over"
            if player.rect.colliderect(level.finish):
                state = "subject_select"

            level.camera_x = max(0, min(player.rect.centerx - WIDTH // 2, level.world_width - WIDTH))
            screen.fill(SKY_BLUE)
            pygame.draw.rect(screen, ROAD_GRAY, (0, HEIGHT - 100, WIDTH, 100))
            level.draw(screen)
            player.draw(screen, level.camera_x)
            screen.blit(FONT.render(f"Жизни: {player.lives}", True, (0, 0, 0)), (10, 10))
            pygame.display.flip()
            clock.tick(60)
        elif state == "subject_select":
            draw_subject_selection()
        elif state == "victory":
            draw_victory_screen(player)
        elif state == "game_over":
            draw_game_over()


if __name__ == "__main__":
    main()
