import pygame
from pygame import mixer
import sys
from random import randint
import math


# Initialize the pygame module
pygame.init()

# creating the screen
size = width, height = 800, 600  # size of the screen

screen = pygame.display.set_mode(size)

# Background image
bg = pygame.image.load("./media/bg.jpg")

# Background sound
mixer.music.load('./media/background.wav')
mixer.music.play(-1)
mixer.music.set_volume(0.2)

# Title and Icon
pygame.display.set_caption("Space Invaders")  # Title of the application
icon = pygame.image.load('./media/ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("./media/player.png")
playerX = 370
playerY = 480
moveX = moveY = 0

# Bullet
bulletImg = pygame.image.load("./media/bullet.png")
bulletX = 386
bulletY = 445
isFired = False
move_bulletX = move_bulletY = 0

# Enemies
enemyImg = []
enemyX = []
enemyY = []
move_enemy_x = []
num_of_enemies = 6

for c in range(num_of_enemies):
    enemyImg.append(pygame.image.load("./media/enemy-1.png"))
    enemyX.append(randint(1, 736))
    enemyY.append(randint(50, 150))
    move_enemy_x.append(0.8)

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game over text
gOver_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render(f"Score: {score_value}", True, (128, 0, 128))
    screen.blit(score, (x, y))


def game_over_text():
    game_over = font.render(f"GAME OVER", True, (128, 0, 128))
    screen.blit(game_over, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def shoot_bullet(x, y):
    global isFired
    isFired = True
    screen.blit(bulletImg, (x, y))


def enemy(x, y, c):
    screen.blit(enemyImg[c], (x, y))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow((enemyX - bulletX), 2) +
                         math.pow((enemyY - bulletY), 2))
    if distance < 27:
        return True
    else:
        return False


while True:
    screen.fill((0, 0, 0))
    # Background image
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moveX -= 0.5
                move_bulletX -= 0.5
            elif event.key == pygame.K_RIGHT:
                moveX += 0.5
                move_bulletX += 0.5
            elif event.key == pygame.K_SPACE:
                shoot_bullet(playerX, bulletY)
                bullet_sound = mixer.Sound('./media/laser.wav')
                bullet_sound.set_volume(0.3)
                bullet_sound.play()

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                moveX = 0
                move_bulletX = 0

            # elif event.key == pygame.K_DOWN or event.key == pygame.K_UP:
            #     moveY = 0

    # playerY += moveY
    if playerX <= 0 and moveX < 0:
        playerX = 0
    elif playerX >= screen.get_width() - 64 and moveX > 0:
        playerX = 736
    if bulletY <= 0:
        bulletY = 480
        bulletX = playerX + 16
        isFired = False

    # if playerY <= 0 and moveY:
    #     playerY = 0
    # elif playerY >= screen.get_height() - 64 and moveY > 0:
    #     playerY = screen.get_height() - 64

    for c in range(num_of_enemies):
        game_over = isCollision(playerX, playerY, enemyX[c], enemyY[c])
        if game_over:
            for d in range(num_of_enemies):
                enemyY[d] = 2000
            game_over_text()
            break

        if enemyX[c] <= 0 or enemyX[c] >= screen.get_width() - 64:
            move_enemy_x[c] *= -1
            enemyY[c] += 20
        enemyX[c] += move_enemy_x[c]

        # Collision
        collision = isCollision(enemyX[c], enemyY[c], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound('./media/explosion.wav')
            collision_sound.set_volume(0.3)
            collision_sound.play()
            bulletY = 480
            isFired = False
            score_value += 1
            enemyX[c] = randint(1, 736)
            enemyY[c] = randint(50, 150)

        enemy(enemyX[c], enemyY[c], c)

    if isFired:
        bulletY -= move_bulletY
        move_bulletX = 0
        shoot_bullet(bulletX, bulletY)

    move_bulletY = 1
    playerX += moveX

    bulletX += move_bulletX

    player(playerX, playerY)
    show_score(textX, textY)

    pygame.display.update()
