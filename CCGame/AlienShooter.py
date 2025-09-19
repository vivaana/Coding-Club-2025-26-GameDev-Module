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
uncollectibleBullet = pygame.image.load("assets/uncollectibleBullet.png")
uncollectibleBullet = pygame.transform.scale(uncollectibleBullet, (60,60))

uncollectibleHeart = pygame.image.load("assets/uncollectibleHeart.png")
uncollectibleHeart = pygame.transform.scale(uncollectibleHeart, (60,60))

uncShield = pygame.image.load("assets/uncShield.png")
uncShield = pygame.transform.scale(uncShield, (60,60))

uncollectibleUpGplayer = pygame.image.load("assets/UncollectibleUpgrade.png")
uncollectibleUpGplayer = pygame.transform.scale(uncollectibleUpGplayer, (90, 90))

UpGplayer_img = pygame.image.load("assets/PlayerUpgrade.png")
UpGplayer_img = pygame.transform.scale(UpGplayer_img, (120, 120))

shield = pygame.image.load("assets/shield.png")
shield = pygame.transform.scale(shield, (90, 90))

player_img = pygame.image.load("assets/player.png")
player_img = pygame.transform.scale(player_img, (70, 70))

heart_img = pygame.image.load("assets/heart.png")
heart_img = pygame.transform.scale(heart_img, (60, 60))

bullet_img = pygame.image.load("assets/bullet.png")
bullet_img = pygame.transform.scale(bullet_img, (60, 60))

alien_img = pygame.image.load("assets/alien.png")
alien_img = pygame.transform.scale(alien_img, (50, 50))

font = pygame.font.SysFont(None, 36)
large_font = pygame.font.SysFont(None, 64)

game_font = pygame.font.Font('assets/SpaceQuest-Xj4o.ttf', 25)
game_font2 = pygame.font.Font('assets/SpaceQuest-Xj4o.ttf', 70)

upG = False

extraLives = 0
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
        if upG == False:
            self.image = player_img
            self.rect = self.image.get_rect(topleft=(x, y))
            self.speed = 7
            self.lives = 3 + extraLives
            self.move_left = False
            self.move_right = False
        elif upG == True:
            self.image = UpGplayer_img
            self.rect = self.image.get_rect(topleft=(x, y))
            self.speed = 12
            self.lives = 5 + extraLives
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

class Button:
    def __init__(self, x, y, width, height, price, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False
        self.price = price

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = game_font.render(buttonText, True, (20, 20, 20))

        objects.append(self)
        #credits to https://thepythoncode.com/article/make-a-button-using-pygame-in-python

    def processImg(self, color, hoverColor, pressColor, image, dimx, dimy):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(color)
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(hoverColor)
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(pressColor)
                if self.onePress:
                    self.onclickFunction()
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False


        self.buttonSurface.blit(image, [
            self.buttonRect.width/2 - dimx/2,# - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - dimy/2# - self.buttonSurf.get_rect().height/2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)
    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if self.onePress:
                    self.onclickFunction()
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False


        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)
# ----- Game Variables -----

player = Player(WIDTH // 2, HEIGHT - 100)
bullets = []
aliens = []
stars = [Star() for _ in range(100)]
enemiesEscaped = 0

score = 0
can_shoot = True

shoot_cooldown = 300  # milliseconds

sendThem = False

last_shot_time = 0

if upG == False:
    pygame.time.set_timer(pygame.USEREVENT, 1000)
elif upG == True:
    pygame.time.set_timer(pygame.USEREVENT, 500)

money = 0
objects = []


game_over = False
game_paused = False
startScreen = True
running = False
shop = False
shieldOn = False

def buttonStartsGame():
    global startScreen,running,shop,extraLives
    if upG == False:
        player.lives = 3 + extraLives
    elif upG == True:
        player.lives = 5 + extraLives
    startScreen = False
    running = True
    shop = False

def buttonShop():
    global startScreen,running,shop
    startScreen = False
    running = False
    shop = True

def buttonStartScreen():
    global startScreen,running,shop
    startScreen = True
    running = False
    shop = False

def buttonheart():
    global extraLives, money
    extraLives += 1
    money -= lifePrice
    if money < 0:
        money = 0

def buttonbullet():
    global shoot_cooldown, money
    shoot_cooldown *= 0.6

    money -= bulletsPrice
    if money < 0:
        money = 0

def buttonUpGrade():
    global upG, money
    upG = True
    money -= upGPrice
    if money < 0:
        money = 0

def buttonShield():
    global shieldOn, money, sendThem
    shieldOn = True
    sendThem = True
    pygame.time.set_timer(pygame.USEREVENT+1, 30000)
    pygame.time.set_timer(pygame.USEREVENT + 3, 24000)
    pygame.time.set_timer(pygame.USEREVENT + 2, 50)
    money -= shieldsPrice
    if money < 0:
        money = 0




Button(300, 200, 400, 100, 0,'Start Game (or spacebar)', buttonStartsGame)
Button(300, 310, 400, 100, 0,'Shop', buttonShop)
Button(590, 10, 200, 75, 0,'Start Screen', buttonStartScreen)
Button(300, 200, 96, 80, 50,'PickUp1', buttonheart)
Button(450, 200, 96, 80, 50,'PickUp1', buttonbullet)
Button(580, 200, 96, 80, 50,'PickUp1', buttonUpGrade)
Button(170, 200, 96, 80, 50,'PickUp1', buttonShield)

scores = []
monies = []

gainMoney = 0

while running == True or startScreen == True or shop == True:
    while startScreen:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                startScreen = False
                shop = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if upG == False:
                        player.lives = 3 + extraLives
                    elif upG == True:
                        player.lives = 5 + extraLives
                    startScreen = False
                    running = True
                    shop = False

        for star in stars:
            star.update()

        screen.fill(BLACK)

        for star in stars:
            star.draw(screen)

        heading_text = "ALIEN SHOOTERS"
        score_surface = game_font2.render(heading_text, True, (36, 124, 201))
        screen.blit(score_surface,(115,90))

        moneyYouHave = game_font.render(f"Total Money: {money}", True, WHITE)
        screen.blit(moneyYouHave, (WIDTH - 260, HEIGHT - 50))

        listButtonsStartScreen = objects[:2]
        for i in listButtonsStartScreen:
            i.process()

        pygame.display.flip()

    while shop:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                startScreen = False
                shop = False

            if event.type == pygame.KEYDOWN:
                '''if event.key == pygame.K_SPACE:
                    startScreen = False
                    running = False
                    shop = False'''

        for star in stars:
            star.update()

        screen.fill(BLACK)

        for star in stars:
            star.draw(screen)

        heading_text = "Shop"
        score_surface = game_font2.render(heading_text, True, (36, 124, 201))
        screen.blit(score_surface,(320,50))

        shieldsPrice = 0
        lifePrice = 50
        bulletsPrice = 75
        upGPrice = 500

        moneyYouHave = game_font.render(f"Total Money: {money}", True, WHITE)
        screen.blit(moneyYouHave, (WIDTH - 260, HEIGHT - 50))
        shieldPrice = game_font.render(f"|  £30 |", True, WHITE, (43, 102, 166))
        heartPrice = game_font.render(f"|  £50 |", True, WHITE, (43, 102, 166))
        bulletPrice = game_font.render(f"|  £75 |", True, WHITE, (43, 102, 166))
        upgradePrice = game_font.render(f"| £500 |", True, WHITE, (43, 102, 166))

        objects[2].process()

        screen.blit(uncollectibleHeart, (320, 200))
        screen.blit(heartPrice, (300, 280))
        if money >= lifePrice:
            objects[3].processImg((227, 175, 79),(168, 123, 42),(153, 102, 9),heart_img, 60,60)

        screen.blit(uncollectibleBullet, (450, 200))
        screen.blit(bulletPrice, (450, 280))
        if money >= bulletsPrice:
            objects[4].processImg((227, 175, 79),(168, 123, 42),(153, 102, 9),bullet_img, 60,60)

        screen.blit(uncollectibleUpGplayer, (580, 200))
        screen.blit(upgradePrice, (580, 280))
        if money >= upGPrice:
            objects[5].processImg((227, 175, 79),(168, 123, 42),(153, 102, 9),UpGplayer_img, 60,60)

        screen.blit(uncShield, (190, 200))
        screen.blit(shieldPrice, (170, 280))
        if money >= shieldsPrice:
            objects[6].processImg((227, 175, 79),(168, 123, 42),(153, 102, 9), shield, 60,60)

        #objects[4].processImg((227, 175, 79),(168, 123, 42),(153, 102, 9),alien_img,50,50)
        #objects[4].processImg((227, 175, 79),(168, 123, 42),(153, 102, 9),alien_img,50,50)

        pygame.display.flip()
    # ----- Main Game Loop -----

    while running:
        clock.tick(FPS)
        current_time = pygame.time.get_ticks()

        # ----- Handle Events -----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                shop = False
                startScreen = False

            if not game_over and not game_paused:
                if event.type == pygame.KEYDOWN:
                    player.handle_keydown(event.key)

                    if event.key == pygame.K_SPACE and can_shoot:
                        if upG == False:
                            bullets.append(Bullet(player.rect.centerx - 5, player.rect.top))
                        elif upG == True:
                            bullets.append(Bullet(player.rect.centerx - 30, player.rect.top+15))
                            bullets.append(Bullet(player.rect.centerx - 15, player.rect.top+5))
                            bullets.append(Bullet(player.rect.centerx - 0, player.rect.top))
                            bullets.append(Bullet(player.rect.centerx + 15, player.rect.top+5))
                            bullets.append(Bullet(player.rect.centerx + 30, player.rect.top+15))
                        can_shoot = False
                        last_shot_time = current_time

                    if event.key == pygame.K_ESCAPE:
                        game_paused = True

                if event.type == pygame.KEYUP:
                    player.handle_keyup(event.key)

                if event.type == pygame.USEREVENT or event.type == pygame.USEREVENT+2 and shieldOn == True and sendThem == True:
                    aliens.append(Alien())

                if event.type == pygame.USEREVENT+3:
                    sendThem = False

                if event.type == pygame.USEREVENT+1:
                    shieldOn = False


            elif game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # Reset everything
                        scores.append(gainMoney)
                        if upG == True:
                            monies.append(int(score*0.15)+money)
                        elif upG == False:
                            monies.append(int(score * 0.35) + money)
                        money = monies[-1]
                        money = money + (1+ int(score/25))
                        score = 0
                        player = Player(WIDTH // 2, HEIGHT - 100)
                        bullets = []
                        aliens = []
                        stars = [Star() for _ in range(100)]
                        enemiesEscaped = 0
                        can_shoot = True
                        last_shot_time = 0
                        game_over = False
                        running = False
                        startScreen = True

                    elif event.key in [pygame.K_q, pygame.K_ESCAPE]:
                        running = False
                        startScreen = False
                        shop = False

            elif game_paused:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_paused = False



        # ----- Game Updates -----
        if not game_over and not game_paused:
            player.move()

            if not can_shoot and current_time - last_shot_time > shoot_cooldown:
                can_shoot = True

            for bullet in bullets[:]:
                bullet.update()
                if bullet.is_off_screen():
                    bullets.remove(bullet)

            for alien in aliens[:]:
                alien.update()
                if alien.is_off_screen() and shieldOn == False:
                    aliens.remove(alien)
                    enemiesEscaped += 1

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
                    if shieldOn == False:
                        player.lives -= 1
                        if player.lives <= 0:
                            game_over = True
                    elif shieldOn == True:
                        score += 1


            for star in stars:
                star.update()

        # ----- Drawing -----
        screen.fill(BLACK)

        for star in stars:
            star.draw(screen)

        if shieldOn == True:
            screen.blit(shield, (player.rect.x, player.rect.y))
        elif shieldOn == False:
            if upG == False:
                player.draw(screen)
            else:
                screen.blit(UpGplayer_img,(player.rect.x, player.rect.y))


        for bullet in bullets:
            bullet.draw(screen)

        for alien in aliens:
            alien.draw(screen)

        # HUD
        if upG == True:
            gainMoney = int(score*0.15)
        if upG == False:
            gainMoney = int(score*0.35)
        combinedMoney = money+gainMoney
        lives_text = game_font.render(f"Lives: {player.lives}", True, WHITE)
        score_text = game_font.render(f"Score: {score}", True, WHITE)
        aliens_escaped = game_font.render(f"Escaped: {enemiesEscaped}", True, WHITE)
        moneyEarned = game_font.render(f"Money Earned: {gainMoney}", True, WHITE)
        totalMoney = game_font.render(f"Total Money: {combinedMoney}", True, WHITE)
        screen.blit(lives_text, (10, 10))
        screen.blit(score_text, (WIDTH - 150, 10))
        screen.blit(aliens_escaped, (WIDTH/2-60, 10))
        screen.blit(moneyEarned, (WIDTH - 260, HEIGHT-80))
        screen.blit(totalMoney, (WIDTH- 260, HEIGHT-50))

        # Game pause screen
        if game_paused:
            game_paused_text = large_font.render("PAUSED", True, WHITE)
            restart_text = game_font.render("Press SPACE to resume.", True, WHITE)
            screen.blit(game_paused_text, (WIDTH // 2 - game_paused_text.get_width() // 2, HEIGHT // 2 - 50))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10))
            screen.blit(totalMoney, (WIDTH - 260, HEIGHT - 50))

        # Game over screen
        if game_over:
            game_over_text = large_font.render("GAME OVER", True, WHITE)
            restart_text = game_font.render("Press R to Restart or Q to Quit", True, WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10))
            screen.blit(totalMoney, (WIDTH- 260, HEIGHT-50))

        pygame.display.flip()

pygame.quit()
sys.exit()
