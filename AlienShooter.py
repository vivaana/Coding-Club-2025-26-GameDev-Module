import pygame
import sys
import random

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


class Player:
    def __init__(self, x, y):
        self.image = player_img
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 7
        self.lives = 3

    def move(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
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
        self.image = pygame.image.load("assets/alien.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = -self.rect.height

    def update(self):
        self.rect.y += 4

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def is_off_screen(self):
        return self.rect.y > HEIGHT


class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.randint(1, 3)

    def draw(self, surface):
        pygame.draw.circle(surface, WHITE, (self.x, self.y), self.size)


player = Player(WIDTH // 2, HEIGHT - 100)
bullets = []

can_shoot = True
shoot_cooldown = 300
last_shot_time = 0

aliens = []
pygame.time.set_timer(pygame.USEREVENT, 1000)

font = pygame.font.SysFont(None, 36)

score = 0

# Create stars
stars = [Star() for _ in range(100)]

running = True
while running:
    clock.tick(FPS)
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT:
            aliens.append(Alien())

    keys = pygame.key.get_pressed()
    player.move(keys)

    if keys[pygame.K_SPACE] and can_shoot:
        bullet = Bullet(player.rect.centerx - 5, player.rect.top)
        bullets.append(bullet)
        can_shoot = False
        last_shot_time = current_time

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

    for bullet in bullets[:]:
        for alien in aliens[:]:
            if bullet.rect.colliderect(alien.rect):
                bullets.remove(bullet)
                aliens.remove(alien)
                score += 1
                break

    for alien in aliens[:]:
        if alien.rect.colliderect(player.rect):
            aliens.remove(alien)
            player.lives -= 1
            if player.lives <= 0:
                print("Game Over!")
                running = False

    # Draw background and stars
    screen.fill(BLACK)
    for star in stars:
        star.draw(screen)

    player.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    for alien in aliens:
        alien.draw(screen)

    lives_text = font.render(f"Lives: {player.lives}", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(lives_text, (10, 10))
    screen.blit(score_text, (WIDTH - 150, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
