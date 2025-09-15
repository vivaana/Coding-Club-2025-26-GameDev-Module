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

alien_img = pygame.image.load("assets/alien.png")
alien_img = pygame.transform.scale(alien_img, (50, 50))

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

class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, 20)

    def update(self):
        self.rect.y -= 8

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 0), self.rect)

    def is_off_screen(self):
        return self.rect.y < 0

class Alien:
    def __init__(self):
        self.image = alien_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = -self.rect.height

    def update(self):
        self.rect.y += 4

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def is_off_screen(self):
        return self.rect.y > HEIGHT

# ----- Game Variables -----

player = Player(WIDTH // 2, HEIGHT - 100)
bullets = []
aliens = []

can_shoot = True
shoot_cooldown = 300  # milliseconds
last_shot_time = 0

# Set a timer to spawn aliens every 1000 ms
pygame.time.set_timer(pygame.USEREVENT, 1000)

running = True

# ----- Main Game Loop -----

while running:
    clock.tick(FPS)
    current_time = pygame.time.get_ticks()

    # ----- Handle Events -----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            player.handle_keydown(event.key)

            if event.key == pygame.K_SPACE and can_shoot:
                bullets.append(Bullet(player.rect.centerx - 5, player.rect.top))
                can_shoot = False
                last_shot_time = current_time

        if event.type == pygame.KEYUP:
            player.handle_keyup(event.key)

        if event.type == pygame.USEREVENT:
            aliens.append(Alien())

    # ----- Game Updates -----
    player.move()

    if not can_shoot and current_time - last_shot_time > shoot_cooldown:
        can_shoot = True

    for bullet in bullets[:]:
        bullet.update()
        if bullet.is_off_screen():
            bullets.remove(bullet)

    for alien in aliens[:]:
        alien.update()
        if alien.is_off_screen():
            aliens.remove(alien)

    # ----- Drawing -----
    screen.fill(BLACK)

    player.draw(screen)

    for bullet in bullets:
        bullet.draw(screen)

    for alien in aliens:
        alien.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
