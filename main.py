import pygame
import random
import math

# initialize pygame
pygame.init()

# create a display
screen = pygame.display.set_mode((800, 600))
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# change title and display
pygame.display.set_caption('First Game')

# player
playerAlive = True
playerIMG = pygame.image.load('spaceship1.png')
playerX = 370
playerY = 520
playerX_change = 0
playerX_change_rate = .6

# enemy
enemyAlive = True
enemyIMG = pygame.image.load('enemy-1.png')
enemyX = random.randint(0, 736)
enemyY = random.randint(65, 100)
enemyX_change_rate = .5
enemyY_change_rate = 50
enemyX_change = enemyX_change_rate
enemyY_change = 0

# bullet
bulletState = False
bulletIMG = pygame.image.load('bullet.png')
bulletX = playerX+25
bulletY = playerY
bulletX_change_rate = 0
bulletY_change_rate = -3

# general var
score = 0
running = True
bulletLimit = 12
bulletCount = 0
scoreToWin = 10

# functions


def player(x, y):
    screen.blit(playerIMG, (x, y))


def enemy(x, y):
    screen.blit(enemyIMG, (x, y))


def bullet(x, y):
    screen.blit(bulletIMG, (x, y))


def fire_bullet():
    global bulletState
    global bulletCount
    bulletState = True
    bulletCount += 1


def destroy_enemy():
    global enemyAlive
    enemyAlive = False


def player_die():
    global playerAlive
    playerAlive = False


def is_collision(b_x, b_y, e_x, e_y):
    distance = math.sqrt((b_x-e_x)*(b_x-e_x) + (b_y-e_y)*(b_y-e_y))
    if distance < 25:
        return True
    else:
        return False

# font

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
# myfont = pygame.freetype.Font("your_font.ttf", 24)

# game loop

while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                print('left pressed')
                playerX_change = - playerX_change_rate
            if event.key == pygame.K_RIGHT:
                print('right pressed')
                playerX_change = playerX_change_rate
            if event.key == pygame.K_UP and bulletCount < bulletLimit:
                fire_bullet()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                print('left released')
                playerX_change = 0
            if event.key == pygame.K_RIGHT:
                print('right released')
                playerX_change = 0

    # player co-ordinate change
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy co-ordinate change
    enemyX += enemyX_change

    if enemyX <= 0:
        enemyX = 0
        enemyX_change = enemyX_change_rate
        enemyY += enemyY_change_rate
    elif enemyX >= 736:
        enemyX = 736
        enemyX_change = -enemyX_change_rate
        enemyY += enemyY_change_rate

    # bullet co-ordinate change
    if bulletState:
        bulletY += bulletY_change_rate
    else:
        bulletX = playerX
        bulletY = playerY

    if bulletY < 0:
        bulletState = False

    # game logic
    # collision = is_collision(bulletX, bulletY, enemyX, enemyY)
    collision = bulletX >= enemyX and bulletX <= enemyX+64 and bulletY <= enemyY+64 and bulletY >= enemyY

    if collision and enemyY < 400:
        score += 1
        bulletState = False
        print(score)

    player(playerX, playerY)
    enemy(enemyX, enemyY)
    if bulletState:
        bullet(bulletX, bulletY)

    scoreText = myfont.render('Score: '+str(score), False, (0, 0, 255))
    screen.blit(scoreText, (0, 0))

    if score >= scoreToWin:
        winText = myfont.render('Winner', False, (0, 255, 0))
        screen.blit(winText, (300, 300))

    """
    if playerX >= enemyX and playerX <= enemyX+64 and playerY <= enemyY+64 and playerY >= enemyY and score < scoreToWin:
        player_die()
    """

    if enemyY > 400 and score < scoreToWin:
        loseText = myfont.render('Loser', False, (255, 0, 0))
        screen.blit(loseText, (300, 300))

    pygame.display.update()


