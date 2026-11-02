import pygame
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My little baby TG")

WHITE = (255, 255, 255)

try:
    player_image = pygame.image.load("player.png").convert_alpha()
    player_image = pygame.transform.scale(player_image, (80, 80))
except pygame.error as e:
    print("Не удалось загрузить картинку 'player.png'. Убедитесь, что она лежит в папке с проектом.")
    pygame.quit()
    sys.exit()

player_rect = player_image.get_rect()
player_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

player_speed = 5

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player_rect.y -= player_speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player_rect.y += player_speed

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_rect.x += player_speed

    if player_rect.left < 0:
        player_rect.left = 0
    if player_rect.right > SCREEN_WIDTH:
        player_rect.right = SCREEN_WIDTH
    if player_rect.top < 0:
        player_rect.top = 0
    if player_rect.bottom > SCREEN_HEIGHT:
        player_rect.bottom = SCREEN_HEIGHT

    screen.fill(WHITE)
    screen.blit(player_image, player_rect)
    pygame.display.flip()

    clock.tick(60)