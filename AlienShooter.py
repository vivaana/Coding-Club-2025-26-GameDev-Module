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

class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.randint(1, 3)
        self.speed = random.uniform(0.5, 1.5)

    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = 0
            self.x = random.randint(0, WIDTH)

    def draw(self, surface):
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.size)

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
stars = [Star() for _ in range(100)]

score = 0
can_shoot = True
shoot_cooldown = 300  # milliseconds
last_shot_time = 0

pygame.time.set_timer(pygame.USEREVENT, 1000)

game_over = False
running = True

# ----- Main Game Loop -----

while running:
    clock.tick(FPS)
    current_time = pygame.time.get_ticks()

    # ----- Handle Events -----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over:
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

        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Reset everything
                    player = Player(WIDTH // 2, HEIGHT - 100)
                    bullets = []
                    aliens = []
                    stars = [Star() for _ in range(100)]
                    score = 0
                    can_shoot = True
                    last_shot_time = 0
                    game_over = False
                elif event.key in [pygame.K_q, pygame.K_ESCAPE]:
                    running = False

    # ----- Game Updates -----
    if not game_over:
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

        # Bullet hits alien
        for bullet in bullets[:]:
            for alien in aliens[:]:
                if bullet.rect.colliderect(alien.rect):
                    bullets.remove(bullet)
                    aliens.remove(alien)
                    score += 1
                    break

        # Alien hits player
        for alien in aliens[:]:
            if alien.rect.colliderect(player.rect):
                aliens.remove(alien)
                player.lives -= 1
                if player.lives <= 0:
                    game_over = True

        for star in stars:
            star.update()

    # ----- Drawing -----
    screen.fill(BLACK)

    for star in stars:
        star.draw(screen)

    player.draw(screen)

    for bullet in bullets:
        bullet.draw(screen)

    for alien in aliens:
        alien.draw(screen)

    # HUD
    lives_text = font.render(f"Lives: {player.lives}", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(lives_text, (10, 10))
    screen.blit(score_text, (WIDTH - 150, 10))

    # Game over screen
    if game_over:
        game_over_text = large_font.render("GAME OVER", True, WHITE)
        restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
