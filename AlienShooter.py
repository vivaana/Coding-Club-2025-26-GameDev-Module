import pygame
import sys
import random

pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Alien Shooter")

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load assets
player_img = pygame.image.load("assets/player.png")
player_img = pygame.transform.scale(player_img, (70, 70))

font = pygame.font.SysFont(None, 36)
large_font = pygame.font.SysFont(None, 64)

# ----- Classes -----

class Player:
    def __init__(self, x, y):
        self.image = player_img
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 7
        self.lives = 3
        self.move_left = False
        self.move_right = False

    def handle_keydown(self, key):
        if key in [pygame.K_LEFT, pygame.K_a]:
            self.move_left = True
        if key in [pygame.K_RIGHT, pygame.K_d]:
            self.move_right = True

    def handle_keyup(self, key):
        if key in [pygame.K_LEFT, pygame.K_a]:
            self.move_left = False
        if key in [pygame.K_RIGHT, pygame.K_d]:
            self.move_right = False

    def move(self):
        if self.move_left:
            self.rect.x -= self.speed
        if self.move_right:
            self.rect.x += self.speed
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# ----- Game Variables -----

player = Player(WIDTH // 2, HEIGHT - 100)

running = True

# ----- Main Game Loop -----

while running:
    clock.tick(FPS)

    # ----- Handle Events -----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            player.handle_keydown(event.key)

        if event.type == pygame.KEYUP:
            player.handle_keyup(event.key)

    # ----- Game Updates -----
    player.move()

    # ----- Drawing -----
    screen.fill(BLACK)
    player.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
