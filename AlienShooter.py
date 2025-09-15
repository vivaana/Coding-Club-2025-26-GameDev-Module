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

# Load player image and scale it
player_img = pygame.image.load("assets/player.png")
player_img = pygame.transform.scale(player_img, (70, 70))

class Player:
    def __init__(self, x, y):
        self.image = player_img
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 7

    def move(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        # Keep player inside screen bounds
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

# Initialize player and bullets list
player = Player(WIDTH // 2, HEIGHT - 100)
bullets = []

# Shooting cooldown variables
can_shoot = True
shoot_cooldown = 300  # milliseconds
last_shot_time = 0

running = True
while running:
    clock.tick(FPS)
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.move(keys)

    # Shoot bullets with cooldown
    if keys[pygame.K_SPACE] and can_shoot:
        bullet = Bullet(player.rect.centerx - 5, player.rect.top)
        bullets.append(bullet)
        can_shoot = False
        last_shot_time = current_time

    if not can_shoot and current_time - last_shot_time > shoot_cooldown:
        can_shoot = True

    # Update bullets and remove if off screen
    for bullet in bullets[:]:
        bullet.update()
        if bullet.is_off_screen():
            bullets.remove(bullet)

    # Draw everything
    screen.fill(BLACK)
    player.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
