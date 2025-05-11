import pygame
import sys
import random
import time

pygame.init()

# Screen settings
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Simple Shooter Game")
font = pygame.font.SysFont('Arial', 12)

# Player settings
player_width = 50
player_height = 50
player_x = screen_width // 2 - player_width // 2
player_y = screen_height - player_height - 10
player_speed = 5

# Bullets settings
bullet_width = 5
bullet_height = 10
bullet_speed = 7
bullets = []

# Enemy settings
enemy_width = 50
enemy_height = 60
enemy_speed = 2
enemies = []

enemy_timer = 0
enemy_spawn_time = 2000
score = 0
health = 3
pygame.mixer.music.load('sound/laser.mp3')

clock = pygame.time.Clock()

def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)

# Game over
def show_game_over(screen):
    gameOver = pygame.mixer.Sound('sound/game_over.mp3')
    gameOver.play()
    font = pygame.font.Font(None, 50)
    text = font.render("Game Over", True, (255, 0, 0))
    screen.fill((0, 0, 0))
    screen.blit(text, (150, 150))
    pygame.display.flip()
    time.sleep(60)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_x = player_x + player_width // 2 - bullet_width // 2
                bullet_y = player_y
                pygame.mixer.music.play(0)
                bullets.append(pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
        player_x += player_speed
    for bullet in bullets:
        bullet.y -= bullet_speed
    bullets = [bullet for bullet in bullets if bullet.y > 0]

    # Update enemy positions and spawn new ones
    current_time = pygame.time.get_ticks()
    if current_time - enemy_timer > enemy_spawn_time:
        enemy_x = random.randint(0, screen_width - enemy_width)
        enemy_y = -enemy_height
        enemies.append(pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height))
        enemy_timer = current_time

    for enemy in enemies:
        if score > 10:
            enemy_speed = 3
        enemy.y += enemy_speed
        if enemy.y >= screen_height - enemy_height:
            health-=1
            enemies.remove(enemy)


    # Check collisions
    for bullet in bullets[:]:
        for enemy in enemies:
            if check_collision(bullet, enemy):
                score += 1
                bullets.remove(bullet)
                enemies.remove(enemy)

    enemies = [enemy for enemy in enemies if enemy.y < screen_height]

    # now print the text
    text_surface = font.render(
        f"Score: {score} Health: {health}",
        True,
        (255, 255, 255)
    )

    if health == 0:
        break

    # Fill screen with a color
    screen.fill((0,0,0))
    screen.blit(text_surface, dest=(20, 20))

    pygame.draw.rect(screen, (0, 128, 255), (player_x, player_y, player_width, player_height))

    # Draw the bullets
    for bullet in bullets:
        pygame.draw.rect(screen, (255, 255, 255), bullet)

    # Draw the enemies
    for enemy in enemies:
        pygame.draw.rect(screen, (255, 0, 0), enemy)

    # Update the display
    pygame.display.flip()

    clock.tick(60)
show_game_over(screen)