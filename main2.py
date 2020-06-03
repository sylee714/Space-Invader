import pygame
from player import Player
from enemy import Enemy
from bullet import Bullet
from pygame import mixer
import random
import math

# Initializes the pygame
pygame.init()
screen_width = 800
screen_height = 600
X_MIN = 0
X_MAX = 735

# Creates the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("alien.png")
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('background.png')

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Score
score_value = 0
score_font = pygame.font.Font('freesansbold.ttf', 32)
score_x = 10
score_y = 10


def display_score(x, y):
    score = score_font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# Game Over
game_over_font = pygame.font.Font('freesansbold.ttf', 32)


def display_game_over():
    text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(text, (300, 250))


# 3 levels of speed
speeds = [3, 5, 7]
level = 0
enemy_speed_level = 0
STOP = 0

# Player
player_x_change_value = 0
start_x = 370
start_y = 480
player_image = pygame.image.load("player.png")
player = Player(player_image, start_x, start_y)


def move_player(player_obj, x_change_value):
    player.set_x(player_obj.x + x_change_value)


# Bullet
fired_bullets = []
bullet_image = pygame.image.load("bullet.png")
bullet_speed = 5

# Load the initial bullet to player
player.load_bullet(Bullet(bullet_image, player.x, player.y))


# Generates random positions for enemies
def generate_rand_enemy_pos():
    return (random.randint(0, 735), random.randint(30, 150))


def generate_enemy(img, x_change_value, y_change_value):
    pos = generate_rand_enemy_pos()
    return Enemy(img, pos[0], pos[1], x_change_value, y_change_value)


# Enemy
enemies = []
enemy_x_change_value = speeds[enemy_speed_level]
enemy_y_change_value = 40
enemy_image = pygame.image.load("enemy.png")
# enemy = generate_enemy(enemy_image)
for i in range(6):
    enemies.append(generate_enemy(enemy_image, enemy_x_change_value, enemy_y_change_value))


def move_enemy_horizontal(enemy_obj, x_change_value):
    enemy_obj.set_x(enemy_obj.x + x_change_value)


def move_enemy_down(enemy_obj, y_change_value):
    enemy_obj.set_y(enemy_obj.y + y_change_value)


# Calculates the Euclidean distance between two objects. If it's less then 27 pixels then returns True;
# otherwise, returns False.
def is_collision(obj1, obj2):
    distance = math.sqrt((math.pow((obj2.x - obj1.x), 2)) + (math.pow((obj2.y - obj1.y), 2)))
    if distance < 27:
        return True
    return False


run = True
while run:

    # RGB - Red, Green, Blue
    screen.fill((0, 0, 0))

    # Background Image
    screen.blit(background, (0, 0))

    # Display Score
    display_score(score_x, score_y)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change_value = -speeds[level]
            if event.key == pygame.K_RIGHT:
                player_x_change_value = speeds[level]
            if event.key == pygame.K_SPACE:
                if len(player.bullet) > 0 and len(fired_bullets) < player.bullet_limit:
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    fired_bullet = player.fire_bullet()
                    fired_bullet.set_x(player.x)
                    fired_bullet.set_fired(True)
                    fired_bullets.append(fired_bullet)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change_value = STOP

    # If the player fired a bullet, move the bullet up and display it
    if len(fired_bullets) > 0:
        for bullet in fired_bullets:
            # Move bullet
            bullet.set_y(bullet.y - bullet_speed)
            # Place bullet; Add values are to center the bullet
            screen.blit(bullet.img, (bullet.x + 16, bullet.y + 10))

    # Check if the bullet reached the top
    for i in range(len(fired_bullets)):
        try:
            if fired_bullets[i].y <= 0:
                fired_bullets.pop(i)
        except IndexError:
            pass

    # Load bullets
    if len(player.bullet) < player.bullet_limit:
        player.load_bullet(Bullet(bullet_image, player.x, player.y))

    # Move player
    move_player(player, player_x_change_value)
    if player.x <= X_MIN:
        player.x = X_MIN
    elif player.x >= X_MAX:
        player.x = X_MAX

    for i in range(len(enemies)):
        # Check if an enemy hits the player. If it does, then end the game.
        if is_collision(player, enemies[i]) or enemies[i].y > screen_height:
            for k in range(len(enemies)):
                enemies[k].set_y(2000)
            player.bullet_limit = 0
            display_game_over()
            break

        # Move enemies.
        move_enemy_horizontal(enemies[i], enemies[i].x_change_value)
        # Move down enemies once they hit the end of the sides.
        if enemies[i].x <= X_MIN:
            enemies[i].x = X_MIN
            enemies[i].x_change_value = speeds[level]
            move_enemy_down(enemies[i], enemies[i].y_change_value)
        elif enemies[i].x >= X_MAX:
            enemies[i].x = X_MAX
            enemies[i].x_change_value = -speeds[level]
            move_enemy_down(enemies[i], enemies[i].y_change_value)

        # Check if a bullet hits the enemy. If it does, then remove
        # the bullet, reposition the enemy, and increase the score by
        # 1.
        for j in range(len(fired_bullets)):
            try:
                if is_collision(fired_bullets[j], enemies[i]):
                    collision_sound = mixer.Sound('explosion.wav')
                    collision_sound.play()
                    score_value += 1
                    new_x, new_y = generate_rand_enemy_pos()
                    enemies[i].set_x(new_x)
                    enemies[i].set_y(new_y)
                    fired_bullets.pop(j)
            except IndexError:
                pass

        # Place enemies
        screen.blit(enemies[i].img, (enemies[i].x, enemies[i].y))

    # Place player
    screen.blit(player.img, (player.x, player.y))

    pygame.display.update()
