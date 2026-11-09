import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My little baby TG 2")
clock = pygame.time.Clock()


try:
    font = pygame.font.SysFont("comicsansms", 30, bold=True)
    big_font = pygame.font.SysFont("comicsansms", 70, bold=True)
except Exception:
    font = pygame.font.Font(None, 36)
    big_font = pygame.font.Font(None, 72)


BG = (40, 25, 45)
WHITE = (255, 255, 255)
DARK_BROWN = (60, 30, 15)
CHOCO_LINE = (90, 45, 20)
CREAM_WHITE = (245, 240, 220)
CREAM_SHADOW = (210, 205, 180)
YELLOW = (255, 220, 50)
RED = (255, 60, 60)


try:
    player_image = pygame.image.load("player2.jpg").convert_alpha()
    player_image = pygame.transform.scale(player_image, (60, 60))
except pygame.error:
    print("Ошибка: картинка 'player.png' не найдена в папке с проектом.")
    pygame.quit()
    sys.exit()


def draw_dark_chocolate(surf, x, y):
    # Плитка
    pygame.draw.rect(surf, DARK_BROWN, (x - 15, y - 15, 30, 30), border_radius=4)
    # Дольки шоколада
    pygame.draw.rect(surf, CHOCO_LINE, (x - 12, y - 12, 10, 10), 1)
    pygame.draw.rect(surf, CHOCO_LINE, (x + 2, y - 12, 10, 10), 1)
    pygame.draw.rect(surf, CHOCO_LINE, (x - 12, y + 2, 10, 10), 1)
    pygame.draw.rect(surf, CHOCO_LINE, (x + 2, y + 2, 10, 10), 1)


def draw_white_chocolate(surf, x, y):
    pygame.draw.circle(surf, CREAM_SHADOW, (x, y), 18)
    pygame.draw.circle(surf, CREAM_WHITE, (x, y), 16)
    pygame.draw.circle(surf, WHITE, (x - 4, y - 4), 5)
    pygame.draw.circle(surf, CREAM_SHADOW, (x, y), 8, 1)


def game():
    player_rect = player_image.get_rect()
    player_rect.center = (WIDTH // 2, HEIGHT - 80)
    player_speed = 6

    enemies = []
    chocolates = []
    score = 0
    lives = 3
    spawn_timer = 0
    choco_timer = 0
    level = 1
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if not game_over:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player_rect.x -= player_speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player_rect.x += player_speed
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                player_rect.y -= player_speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                player_rect.y += player_speed

            player_rect.left = max(0, player_rect.left)
            player_rect.right = min(WIDTH, player_rect.right)
            player_rect.top = max(0, player_rect.top)
            player_rect.bottom = min(HEIGHT, player_rect.bottom)

            spawn_timer += 1
            if spawn_timer > max(15, 45 - level * 3):
                spawn_timer = 0
                enemies.append([random.randint(30, WIDTH - 30), -30, random.uniform(3, 5 + level)])

            choco_timer += 1
            if choco_timer > 90:
                choco_timer = 0
                chocolates.append([random.randint(30, WIDTH - 30), -30])

            for e in enemies[:]:
                e[1] += e[2]
                enemy_rect = pygame.Rect(e[0] - 18, e[1] - 18, 36, 36)

                if e[1] > HEIGHT + 30:
                    enemies.remove(e)
                    score += 1
                    if score % 10 == 0:
                        level += 1
                elif player_rect.colliderect(enemy_rect):
                    enemies.remove(e)
                    lives -= 1
                    if lives <= 0:
                        game_over = True

            for c in chocolates[:]:
                c[1] += 3
                choco_rect = pygame.Rect(c[0] - 15, c[1] - 15, 30, 30)

                if c[1] > HEIGHT + 30:
                    chocolates.remove(c)
                elif player_rect.colliderect(choco_rect):
                    chocolates.remove(c)
                    lives += 1
                    score += 5

        screen.fill(BG)

        for c in chocolates:
            draw_dark_chocolate(screen, int(c[0]), int(c[1]))
        for e in enemies:
            draw_white_chocolate(screen, int(e[0]), int(e[1]))

        screen.blit(player_image, player_rect)

        score_text = font.render(f"Счёт: {score}  Уровень: {level}", True, YELLOW)
        screen.blit(score_text, (10, 10))
        lives_text = font.render(f"Жизни: {'❤' * max(0, lives)}", True, RED)
        screen.blit(lives_text, (WIDTH - 250, 10))

        if game_over:
            over = big_font.render("GAME OVER!", True, RED)
            screen.blit(over, (WIDTH // 2 - over.get_width() // 2, HEIGHT // 2 - 80))
            restart = font.render("Нажми R для рестарта", True, WHITE)
            screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, HEIGHT // 2 + 20))
            if keys[pygame.K_r]:
                game()
                return

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    game()