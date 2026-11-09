import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My little baby TG 3")
clock = pygame.time.Clock()

try:
    font = pygame.font.SysFont("comicsansms", 30, bold=True)
    big_font = pygame.font.SysFont("comicsansms", 70, bold=True)
except Exception:
    font = pygame.font.Font(None, 36)
    big_font = pygame.font.Font(None, 72)

DARK_PURPLE = (25, 15, 40)
MID_PURPLE = (55, 30, 80)
WHITE = (255, 255, 255)
YELLOW = (255, 220, 50)
RED = (255, 60, 60)

ICE_CREAM_TUB = (100, 200, 255)
ICE_CREAM_PINK = (255, 140, 180)
ICE_CREAM_CREAM = (255, 245, 220)

JUICE_ORANGE = (255, 140, 0)
JUICE_DARK_ORANGE = (210, 100, 0)
STRAW_COLOR = (255, 230, 100)

try:
    player_image = pygame.image.load("player3.jpg").convert_alpha()
    player_image = pygame.transform.scale(player_image, (70, 70))
except pygame.error:
    print("Ошибка: Не удалось загрузить 'player3.jpg'. Убедитесь, что файл в папке с кодом.")
    pygame.quit()
    sys.exit()

stars = []
for _ in range(60):
    stars.append({
        'x': random.randint(0, SCREEN_WIDTH),
        'y': random.randint(0, SCREEN_HEIGHT),
        'size': random.randint(1, 3),
        'speed': random.uniform(0.2, 0.8)
    })

def draw_background(surf):
    for y in range(SCREEN_HEIGHT):
        r = DARK_PURPLE[0] + (MID_PURPLE[0] - DARK_PURPLE[0]) * y // SCREEN_HEIGHT
        g = DARK_PURPLE[1] + (MID_PURPLE[1] - DARK_PURPLE[1]) * y // SCREEN_HEIGHT
        b = DARK_PURPLE[2] + (MID_PURPLE[2] - DARK_PURPLE[2]) * y // SCREEN_HEIGHT
        pygame.draw.line(surf, (r, g, b), (0, y), (SCREEN_WIDTH, y))
    
    for star in stars:
        star['y'] += star['speed']
        if star['y'] > SCREEN_HEIGHT:
            star['y'] = 0
            star['x'] = random.randint(0, SCREEN_WIDTH)
        pygame.draw.circle(surf, (220, 220, 255), (int(star['x']), int(star['y'])), star['size'])

def draw_ice_cream(surf, x, y):
    pygame.draw.circle(surf, ICE_CREAM_PINK, (x - 7, y - 8), 11)
    pygame.draw.circle(surf, ICE_CREAM_CREAM, (x + 7, y - 8), 11)
    pygame.draw.circle(surf, WHITE, (x, y - 14), 10)
    pygame.draw.polygon(surf, ICE_CREAM_TUB, [(x - 14, y - 2), (x + 14, y - 2), (x + 10, y + 16), (x - 10, y + 16)])
    pygame.draw.line(surf, WHITE, (x - 14, y - 2), (x + 14, y - 2), 2)

def draw_orange_juice(surf, x, y):
    pygame.draw.line(surf, STRAW_COLOR, (x + 4, y - 16), (x + 10, y - 24), 3)
    pygame.draw.rect(surf, JUICE_ORANGE, (x - 16, y - 16, 32, 32), border_radius=4)
    pygame.draw.rect(surf, JUICE_DARK_ORANGE, (x - 16, y - 16, 32, 32), 2, border_radius=4)
    pygame.draw.circle(surf, YELLOW, (x, y), 6)
    pygame.draw.circle(surf, JUICE_DARK_ORANGE, (x, y), 6, 1)

def game():
    player_rect = player_image.get_rect()
    player_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)
    player_speed = 6

    bullets = []
    enemies = []
    ice_creams = []
    
    random_objects = []
    for _ in range(3):
        random_objects.append({
            'x': random.randint(20, SCREEN_WIDTH - 20),
            'y': random.randint(20, SCREEN_HEIGHT // 2),
            'dx': random.choice([-3, -2, 2, 3]),
            'dy': random.choice([-3, -2, 2, 3]),
            'radius': 12
        })

    score = 0
    lives = 3
    spawn_timer = 0
    ice_cream_timer = 0
    level = 1
    game_over = False

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_SPACE:
                    bullets.append(pygame.Rect(player_rect.centerx - 3, player_rect.top, 6, 12))

        keys = pygame.key.get_pressed()

        if not game_over:
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_rect.left > 0:
                player_rect.x -= player_speed
            if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_rect.right < SCREEN_WIDTH:
                player_rect.x += player_speed
            if (keys[pygame.K_UP] or keys[pygame.K_w]) and player_rect.top > 0:
                player_rect.y -= player_speed
            if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player_rect.bottom < SCREEN_HEIGHT:
                player_rect.y += player_speed

            for bullet in bullets[:]:
                bullet.y -= 10
                if bullet.bottom < 0:
                    bullets.remove(bullet)

            spawn_timer += 1
            if spawn_timer > max(15, 45 - level * 3):
                spawn_timer = 0
                enemies.append([random.randint(30, SCREEN_WIDTH - 30), -30, random.uniform(3, 5 + level)])

            ice_cream_timer += 1
            if ice_cream_timer > 90:
                ice_cream_timer = 0
                ice_creams.append([random.randint(30, SCREEN_WIDTH - 30), -30])

            for e in enemies[:]:
                e[1] += e[2]
                enemy_rect = pygame.Rect(e[0] - 16, e[1] - 16, 32, 32)

                for bullet in bullets[:]:
                    if enemy_rect.colliderect(bullet):
                        if bullet in bullets:
                            bullets.remove(bullet)
                        if e in enemies:
                            enemies.remove(e)
                        score += 10
                        break

                if enemy_rect.colliderect(player_rect):
                    if e in enemies:
                        enemies.remove(e)
                    lives -= 1
                    if lives <= 0:
                        game_over = True

                elif e[1] > SCREEN_HEIGHT + 30:
                    if e in enemies:
                        enemies.remove(e)

            for ic in ice_creams[:]:
                ic[1] += 3
                ic_rect = pygame.Rect(ic[0] - 14, ic[1] - 14, 28, 28)
                if ic_rect.colliderect(player_rect):
                    score += 15
                    ice_creams.remove(ic)
                elif ic[1] > SCREEN_HEIGHT + 30:
                    ice_creams.remove(ic)

            for obj in random_objects:
                obj['x'] += obj['dx']
                obj['y'] += obj['dy']

                if obj['x'] - obj['radius'] <= 0 or obj['x'] + obj['radius'] >= SCREEN_WIDTH:
                    obj['dx'] *= -1
                if obj['y'] - obj['radius'] <= 0 or obj['y'] + obj['radius'] >= SCREEN_HEIGHT:
                    obj['dy'] *= -1

        draw_background(screen)

        for bullet in bullets:
            pygame.draw.rect(screen, YELLOW, bullet)

        for e in enemies:
            draw_orange_juice(screen, int(e[0]), int(e[1]))

        for ic in ice_creams:
            draw_ice_cream(screen, int(ic[0]), int(ic[1]))

        for obj in random_objects:
            pygame.draw.circle(screen, RED, (int(obj['x']), int(obj['y'])), obj['radius'])

        screen.blit(player_image, player_rect)

        score_text = font.render(f"Очки: {score}", True, WHITE)
        lives_text = font.render(f"Жизни: {lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (SCREEN_WIDTH - 150, 10))

        if game_over:
            over_text = big_font.render("GAME OVER", True, RED)
            screen.blit(over_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 40))

        pygame.display.flip()

game()