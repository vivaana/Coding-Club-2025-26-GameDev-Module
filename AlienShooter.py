import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Alien Shooter")

clock = pygame.time.Clock()
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

player_img = pygame.image.load("assets/player.png")
player_img = pygame.transform.scale(player_img, (70, 70))
