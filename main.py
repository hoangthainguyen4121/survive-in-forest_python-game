import pygame
import os
import random

# Initialize Pygame
pygame.init()

# Set up the screen dimensions
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# Load background image
platform_image = pygame.image.load("platform.png").convert()
platform_image = pygame.transform.scale(platform_image, (screen_width, screen_height))

# Load player image
player_image_left = pygame.image.load("player.png").convert_alpha()
player_aspect_ratio = player_image_left.get_width() / player_image_left.get_height()
player_new_height = int(screen_height / 6)
player_new_width = int(player_new_height * player_aspect_ratio)
player_image_left = pygame.transform.scale(player_image_left, (player_new_width, player_new_height))
player_image_left.set_colorkey((0, 0, 0))
player_image_right = pygame.transform.flip(player_image_left, True, False)
player_image = player_image_left
player_x = (screen_width - player_image.get_width()) // 2
player_y = screen_height - player_image.get_height()

# Load ghost image
ghost_image = pygame.image.load("ghost.png").convert_alpha()
ghost_aspect_ratio = ghost_image.get_width() / ghost_image.get_height()
ghost_new_height = int(screen_height / 6)
ghost_new_width = int(ghost_new_height * ghost_aspect_ratio)
ghost_image = pygame.transform.scale(ghost_image, (ghost_new_width, ghost_new_height))
ghost_x = random.randint(0, screen_width - ghost_image.get_width())
ghost_y = 0 - ghost_image.get_height()
ghost_speed = 5

# Load background music
pygame.mixer.music.load("song.mp3")
pygame.mixer.music.play(-1)

# Initialize player's health
player_health = 100

# Initialize jumping variables
is_jumping = False
jump_count = 10
jump_height = 200

def draw_health_bar(screen, x, y, health):
    bar_width = 100
    bar_height = 10
    fill_percentage = health / 100
    fill_width = int(bar_width * fill_percentage)
    outline_rect = pygame.Rect(x, y, bar_width, bar_height)
    fill_rect = pygame.Rect(x, y, fill_width, bar_height)
    pygame.draw.rect(screen, (255, 0, 0), fill_rect)
    pygame.draw.rect(screen, (255, 255, 255), outline_rect, 2)

# Main game loop
clock = pygame.time.Clock()
running = True
while running and player_health > 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= 5
        player_image = player_image_left
    if keys[pygame.K_RIGHT]:
        player_x += 5
        player_image = player_image_right

    if not is_jumping:
        if keys[pygame.K_UP]:
            is_jumping = True
    else:
        if jump_count >= -10:
            direction = 1 if jump_count >= 0 else -1
            player_y -= (jump_count ** 2) * 0.2 * direction
            jump_count -= 1
        else:
            is_jumping = False
            jump_count = 10

    # Move the ghost
    ghost_y += ghost_speed
    if ghost_y > screen_height:
        ghost_y = 0 - ghost_image.get_height()
        ghost_x = random.randint(0, screen_width - ghost_image.get_width())

    # Check for collisions between the player and the ghost
    player_rect = pygame.Rect(player_x, player_y, player_image.get_width(), player_image.get_height())
    ghost_rect = pygame.Rect(ghost_x, ghost_y, ghost_image.get_width(), ghost_image.get_height())
    if player_rect.colliderect(ghost_rect):
        player_health -= 20  # Decrease the player's health by 5 instead of 1
        ghost_y = 0 - ghost_image.get_height()
        ghost_x = random.randint(0, screen_width - ghost_image.get_width())

    # Draw the background, characters, and health bar
    screen.blit(platform_image, (0, 0))
    screen.blit(player_image, (player_x, player_y))
    screen.blit(ghost_image, (ghost_x, ghost_y))
    draw_health_bar(screen, 10, 10, player_health)

    # Update the screen
    pygame.display.update()

    # Limit the frame rate
    clock.tick(30)

# Quit Pygame
pygame.quit()
