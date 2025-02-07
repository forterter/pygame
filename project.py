import pygame
import sys
import random


pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dodge the targeted bullets")

black = (0, 0, 0)
white = (255, 255, 255)

# Игрок
player_size = 50
player_hitbox_width = 40  # Размер хитбокса игрока
player_hitbox_height = 40
player_pos = [width // 2, height // 2]
player_speed = 5

player_image = pygame.image.load("i.png")
player_image = pygame.transform.scale(player_image, (player_size, player_size))

# Пули
bullet_size = (20, 10)
bullet_hitbox_size = (15, 10)  # Размер хитбокса пули
bullet_speed = 5
bullet_list = []

bullet_image = pygame.image.load("meteorit.png")
bullet_image = pygame.transform.scale(bullet_image, bullet_size)

# Функция для создания новой пули
def create_bullet(target_pos, difficulty):
    x_pos = random.randint(0, width - bullet_size[0])
    y_pos = 0  # Начинаем с верхней части экрана
    angle = (target_pos[0] - x_pos, target_pos[1] - y_pos)
    if difficulty == 'easy':
        bullet_speed_mod = 3
    elif difficulty == 'medium':
        bullet_speed_mod = 5
    elif difficulty == 'hard':
        bullet_speed_mod = 7
    bullet_list.append([x_pos, y_pos, angle, bullet_speed_mod])

# Функция для обновления позиций пуль
def update_bullets():
    for bullet in bullet_list:
        dx, dy = bullet[2]
        length = (dx**2 + dy**2) ** 0.5
        dx = (dx / length) * bullet[3]
        dy = (dy / length) * bullet[3]
        bullet[0] += dx
        bullet[1] += dy
        if bullet[1] > height or bullet[0] < 0 or bullet[0] > width:
            bullet_list.remove(bullet)

# Функция для проверки столкновений
def check_collision(player_pos, bullet_list):
    for bullet in bullet_list:
        distance = ((player_pos[0] - bullet[0])**2 + (player_pos[1] - bullet[1])**2)**0.5
        if distance <= 5:
            # Проверяем, попадает ли пуля в хитбокс игрока
            if (player_pos[0] - player_hitbox_width // 2 < bullet[0] < player_pos[0] + player_hitbox_width // 2 or
                player_pos[0] - player_hitbox_width // 2 < bullet[0] + bullet_hitbox_size[0] < player_pos[0] + player_hitbox_width // 2) and \
               (player_pos[1] - player_hitbox_height // 2 < bullet[1] < player_pos[1] + player_hitbox_height // 2 or
                player_pos[1] - player_hitbox_height // 2 < bullet[1] + bullet_hitbox_size[1] < player_pos[1] + player_hitbox_height // 2):
                return True
    return False

# Функция для отображения главного меню
def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if play_button.collidepoint(mouse_pos):
                        show_difficulty_menu()

        # Добавляем фон
        screen.fill(black)
        background = pygame.image.load('background.png')
        background = pygame.transform.scale(background, (width, height))
        screen.blit(background, (0, 0))

        # Играть
        play_button = pygame.Rect(width // 2 - 75, height // 2 - 25, 150, 50)
        pygame.draw.rect(screen, white, play_button)
        font = pygame.font.Font(None, 36)
        text = font.render("Играть", True, black)
        text_rect = text.get_rect(center=play_button.center)
        screen.blit(text, text_rect)

        pygame.display.flip()


# Функция для отображения меню выбора уровня сложности
def show_difficulty_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # ЛКМ
                    mouse_pos = pygame.mouse.get_pos()
                    if easy_button.collidepoint(mouse_pos):
                        game_loop(difficulty='easy')
                    elif medium_button.collidepoint(mouse_pos):
                        game_loop(difficulty='medium')
                    elif hard_button.collidepoint(mouse_pos):
                        game_loop(difficulty='hard')

        # Заливаем экран фоном
        screen.fill(black)
        background = pygame.image.load('background.png')
        background = pygame.transform.scale(background, (width, height))
        screen.blit(background, (0, 0))

        # Кнопки для выбора уровня сложности
        easy_button = pygame.Rect(width // 4 - 75, height // 2 - 25, 150, 50)
        medium_button = pygame.Rect(width // 2 - 75, height // 2 - 25, 150, 50)
        hard_button = pygame.Rect(width * 3 // 4 - 75, height // 2 - 25, 150, 50)
        pygame.draw.rect(screen, white, easy_button)
        pygame.draw.rect(screen, white, medium_button)
        pygame.draw.rect(screen, white, hard_button)
        font = pygame.font.Font(None, 36)
        easy_text = font.render("Легкий", True, black)
        medium_text = font.render("Средний", True, black)
        hard_text = font.render("Сложный", True, black)
        easy_rect = easy_text.get_rect(center=easy_button.center)
        medium_rect = medium_text.get_rect(center=medium_button.center)
        hard_rect = hard_text.get_rect(center=hard_button.center)
        screen.blit(easy_text, easy_rect)
        screen.blit(medium_text, medium_rect)
        screen.blit(hard_text, hard_rect)

        pygame.display.flip()


# Основной игровой цикл
def game_loop(difficulty='easy'):
    global player_pos, bullet_list
    player_pos = [width // 2, height // 2]
    bullet_list = []
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        # Обновляем позицию игрока
        if keys[pygame.K_LEFT]:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT]:
            player_pos[0] += player_speed
        if keys[pygame.K_UP]:
            player_pos[1] -= player_speed
        if keys[pygame.K_DOWN]:
            player_pos[1] += player_speed

        # Убедитесь, что игрок остается в пределах экрана
        player_pos[0] = max(0, min(player_pos[0], width - player_size))
        player_pos[1] = max(0, min(player_pos[1], height - player_size))

        # Создаем пули
        if random.randint(1, 20) == 1:
            create_bullet(player_pos, difficulty)

        # Обновляем позиции пуль
        update_bullets()

        # Проверяем на столкновения
        if check_collision(player_pos, bullet_list):
            game_over()

        # Заливаем экран черным цветом
        screen.fill(black)

        # Рисуем игрока
        screen.blit(player_image, (player_pos[0], player_pos[1]))

        # Рисуем пули
        for bullet in bullet_list:
            screen.blit(bullet_image, (bullet[0], bullet[1]))

        pygame.display.flip()

        # Устанавливаем частоту кадров
        pygame.time.Clock().tick(30)

def game_over():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if play_button.collidepoint(mouse_pos):
                        show_difficulty_menu()

        # Заливаем экран фоном
        screen.fill(black)
        background = pygame.image.load('background.png')
        background = pygame.transform.scale(background, (width, height))
        screen.blit(background, (0, 0))

        # Игра окончена
        font = pygame.font.Font(None, 72)
        text = font.render("Игра окончена", True, white)
        text_rect = text.get_rect(center=(width // 2, height // 2 - 50))
        screen.blit(text, text_rect)

        # Играть
        play_button = pygame.Rect(width // 2 - 75, height // 2 + 25, 150, 50)
        pygame.draw.rect(screen, white, play_button)
        font = pygame.font.Font(None, 36)
        text = font.render("Играть", True, black)
        text_rect = text.get_rect(center=play_button.center)
        screen.blit(text, text_rect)

        pygame.display.flip()


main_menu()

pygame.quit()