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