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
player_hitbox_width = 30  # Размер хитбокса игрока
player_hitbox_height = 30
player_pos = [width // 2, height // 2]
player_speed = 5

player_image = pygame.image.load("i.png")
player_image = pygame.transform.scale(player_image, (player_size, player_size))

# Пули
bullet_size = (20, 10)
bullet_hitbox_size = (15, 5)  # Размер хитбокса пули
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