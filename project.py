import pygame
import sys
import random

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dodge bullets")

black = (0, 0, 0)
white = (255, 255, 255)

# Загрузка изображений
player_image = pygame.image.load('../pythonProject4/img_3.png')
bullet_image = pygame.image.load('img_2.png')

# Игрок
player_hitbox_width = 40
player_hitbox_height = 40
player_pos = [width // 2, height // 2]
player_speed = 5

# Загрузка изображений


# Пули
bullet_hitbox_size = (20, 20)
bullet_speed = 5
bullet_list = []

player_image = pygame.transform.scale(player_image, (player_hitbox_width, player_hitbox_height))  # Масштабируем изображение игрока

bullet_image = pygame.transform.scale(bullet_image, bullet_hitbox_size)  # Масштабируем изображение пули

# Функция для создания новой пули
def create_bullet(target_pos, difficulty):
    x_pos = random.randint(0, width - bullet_hitbox_size[0])
    y_pos = 0  # Начинаем с верхней части экрана
    angle = (target_pos[0] - x_pos, target_pos[1] - y_pos)
    if difficulty == 'easy':
        bullet_speed_mod = bullet_speed * 1  # Легкий уровень
    elif difficulty == 'medium':
        bullet_speed_mod = bullet_speed * 1.5  # Средний уровень
    elif difficulty == 'hard':
        bullet_speed_mod = bullet_speed * 2  # Сложный уровень
    bullet_list.append([x_pos, y_pos, angle, bullet_speed_mod])

# Функция для обновления позиций пуль
def update_bullets():
    new_bullet_list = []
    for bullet in bullet_list:
        dx, dy = bullet[2]
        length = (dx**2 + dy**2) ** 0.5
        if length > 0:  # Избегаем деления на ноль
            dx = (dx / length) * bullet[3]
            dy = (dy / length) * bullet[3]
            bullet[0] += dx
            bullet[1] += dy
            if bullet[1] <= height and 0 <= bullet[0] <= width:
                new_bullet_list.append(bullet)
    return new_bullet_list

# Функция для проверки столкновений
def check_collision(player_pos, bullet_list):
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_hitbox_width, player_hitbox_height)
    for bullet in bullet_list:
        bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_hitbox_size[0], bullet_hitbox_size[1])
        if player_rect.colliderect(bullet_rect):
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

        # Заливаем экран фоном
        screen.fill(black)
        background = pygame.image.load('background2.jpg')
        background = pygame.transform.scale(background, (width, height))
        screen.blit(background, (0, 0))

        # Обновляем позицию игрока
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT]:
            player_pos[0] += player_speed
        if keys[pygame.K_UP]:
            player_pos[1] -= player_speed
        if keys[pygame.K_DOWN]:
            player_pos[1] += player_speed

        # Убедитесь, что игрок остается в пределах экрана
        player_pos[0] = max(0, min(player_pos[0], width - player_hitbox_width))
        player_pos[1] = max(0, min(player_pos[1], height - player_hitbox_height))

        # Создаем пули
        if random.randint(1, 20) == 1:
            create_bullet(player_pos, difficulty)

        # Обновляем позиции пуль
        bullet_list[:] = update_bullets()  # Обновляем список пуль

        # Проверяем на столкновения
        if check_collision(player_pos, bullet_list):
            game_over()

        # Рисуем игрока (изображение)
        player_rect = player_image.get_rect(center=(player_pos[0] + player_hitbox_width // 2, player_pos[1] + player_hitbox_height // 2))
        screen.blit(player_image, player_rect)

        # Рисуем пули (изображения)
        for bullet in bullet_list:
            bullet_rect = bullet_image.get_rect(center=(bullet[0] + bullet_hitbox_size[0] // 2, bullet[1] + bullet_hitbox_size[1] // 2))
            screen.blit(bullet_image, bullet_rect)

        pygame.display.flip()

        # Устанавливаем частоту кадров
        pygame.time.Clock().tick(60)

def game_over():
    global play_button  # Объявляем переменную как глобальную
    play_button = pygame.Rect(width // 2 - 75, height // 2 - 25, 150, 50)  # Определяем play_button
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

        # Кнопка для возврата в главное меню
        pygame.draw.rect(screen, white, play_button)
        font = pygame.font.Font(None, 36)
        play_text = font.render("Играть", True, black)
        play_text_rect = play_text.get_rect(center=play_button.center)
        screen.blit(play_text, play_text_rect)

        pygame.display.flip()

# Запуск главного меню
main_menu()

pygame.quit()