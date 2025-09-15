import pygame
import sys

# Initialize Pygame
pygame.init()

# ----- Screen Settings -----
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Alien Shooter")

# ----- Clock & FPS -----
clock = pygame.time.Clock()
FPS = 60

# ----- Colors -----
BLACK = (0, 0, 0)

# ----- Main Game Loop -----
running = True
while running:
    clock.tick(FPS)  # Limit the game to 60 FPS

    # ----- Event Handling -----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ----- Drawing -----
    screen.fill(BLACK)

    # Update the display
    pygame.display.flip()

# Clean up and exit
pygame.quit()
sys.exit()
