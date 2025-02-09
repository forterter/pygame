import pygame
import sys
import random
import sqlite3

pygame.init()

# Создаем или подключаемся к базе данных
conn = sqlite3.connect('coins.db')
cursor = conn.cursor()

# Создаем таблицу, если она не существует
cursor.execute('''
CREATE TABLE IF NOT EXISTS coins (
    id INTEGER PRIMARY KEY,
    total_coins INTEGER DEFAULT 0
)
''')
# Проверяем, есть ли уже запись в таблице
cursor.execute('SELECT total_coins FROM coins WHERE id = 1')
if cursor.fetchone() is None:
    cursor.execute('INSERT INTO coins (id, total_coins) VALUES (1, 0)')
    conn.commit()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dodge bullets")

black = (0, 0, 0)
white = (255, 255, 255)

# Загрузка изображений
player_image = pygame.image.load('img_3.png')
bullet_image = pygame.image.load('img_2.png')

# Игрок
player_hitbox_width = 40
player_hitbox_height = 40
player_pos = [width // 2, height // 2]
player_speed = 5

# Пули
bullet_hitbox_size = (20, 20)
bullet_speed = 5
bullet_list = []

player_image = pygame.transform.scale(player_image, (player_hitbox_width, player_hitbox_height))
bullet_image = pygame.transform.scale(bullet_image, bullet_hitbox_size)

# Переменные для монет и времени
coins = 0
survival_time = 0
clock = pygame.time.Clock()

# Функция для создания новой пули
def create_bullet(target_pos, difficulty):
    x_pos = random.randint(0, width - bullet_hitbox_size[0])
    y_pos = 0
    angle = (target_pos[0] - x_pos, target_pos[1] - y_pos)
    bullet_speed_mod = bullet_speed * (1 + (difficulty == 'medium') * 0.5 + (difficulty == 'hard') * 1)
    bullet_list.append([x_pos, y_pos, angle, bullet_speed_mod])

# Функция для обновления позиций пуль
def update_bullets():
    new_bullet_list = []
    for bullet in bullet_list:
        dx, dy = bullet[2]
        length = (dx ** 2 + dy ** 2) ** 0.5
        if length > 0:
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

        screen.fill(black)
        background = pygame.image.load('background.png')
        background = pygame.transform.scale(background, (width, height))
        screen.blit(background, (0, 0))

        # Отображаем общее количество монет
        cursor.execute('SELECT total_coins FROM coins WHERE id = 1')
        total_coins = cursor.fetchone()[0]
        font = pygame.font.Font(None, 36)
        total_coins_text = font.render(f"Всего монет: {total_coins}", True, white)
        screen.blit(total_coins_text, (10, 10))  # Отображаем в верхнем левом углу

        # Играть
        play_button = pygame.Rect(width // 2 - 75, height // 2 - 25, 150, 50)
        pygame.draw.rect(screen, white, play_button)
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
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if easy_button.collidepoint(mouse_pos):
                        game_loop(difficulty='easy')
                    elif medium_button.collidepoint(mouse_pos):
                        game_loop(difficulty='medium')
                    elif hard_button.collidepoint(mouse_pos):
                        game_loop(difficulty='hard')

        screen.fill(black)
        background = pygame.image.load('background.png')
        background = pygame.transform.scale(background, (width, height))
        screen.blit(background, (0, 0))

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

def game_loop(difficulty='easy'):
    global player_pos, bullet_list, coins, survival_time
    player_pos = [width // 2, height // 2]
    bullet_list = []
    coins = 0
    survival_time = 0
    running = True
    start_ticks = pygame.time.get_ticks()  # Начинаем отсчет времени

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
        bullet_list[:] = update_bullets()

        # Проверяем на столкновения
        if check_collision(player_pos, bullet_list):
            game_over()

        # Рисуем игрока (изображение)
        player_rect = player_image.get_rect(
            center=(player_pos[0] + player_hitbox_width // 2, player_pos[1] + player_hitbox_height // 2))
        screen.blit(player_image, player_rect)

        # Рисуем пули (изображения)
        for bullet in bullet_list:
            bullet_rect = bullet_image.get_rect(
                center=(bullet[0] + bullet_hitbox_size[0] // 2, bullet[1] + bullet_hitbox_size[1] // 2))
            screen.blit(bullet_image, bullet_rect)

        # Обновляем время выживания
        survival_time = (pygame.time.get_ticks() - start_ticks) / 1000  # Время в секундах

        # Начисляем монеты в зависимости от времени и сложности
        if difficulty == 'easy':
            coins = int(survival_time * 0.5)  # 0.5 монеты за каждую секунду
        elif difficulty == 'medium':
            coins = int(survival_time * 1.5)  # 1.5 монеты за каждую секунду
        elif difficulty == 'hard':
            coins = int(survival_time * 2.5)  # 2.5 монеты за каждую секунду

        # Отображаем общее количество монет
        cursor.execute('SELECT total_coins FROM coins WHERE id = 1')
        total_coins = cursor.fetchone()[0]
        font = pygame.font.Font(None, 36)
        total_coins_text = font.render(f"Всего монет: {total_coins}", True, white)
        screen.blit(total_coins_text, (10, 10))

        # Отображаем количество монет за текущую игру
        coins_text = font.render(f"Монеты: {coins}", True, white)
        screen.blit(coins_text, (10, 50))

        pygame.display.flip()

        clock.tick(60)

def game_over():
    global play_button
    play_button = pygame.Rect(width // 2 - 75, height // 2 - 25, 150, 50)  # Определяем play_button

    # Сохраняем монеты в базе данных
    cursor.execute('SELECT total_coins FROM coins WHERE id = 1')
    current_coins = cursor.fetchone()[0]
    new_total_coins = current_coins + coins
    cursor.execute('UPDATE coins SET total_coins = ? WHERE id = 1', (new_total_coins,))
    conn.commit()

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

        # Отображаем общее количество монет
        cursor.execute('SELECT total_coins FROM coins WHERE id = 1')
        total_coins = cursor.fetchone()[0]
        font = pygame.font.Font(None, 36)
        total_coins_text = font.render(f"Всего монет: {total_coins}", True, white)
        screen.blit(total_coins_text, (10, 10))

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
