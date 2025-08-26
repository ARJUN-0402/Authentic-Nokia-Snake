import pygame
import random
import sys
import time

# =========================
# Setup
# =========================
pygame.init()

# Screen & grid
WIDTH, HEIGHT = 480, 320
CELL = 16
COLS, ROWS = WIDTH // CELL, HEIGHT // CELL

# Colors (Nokia LCD-ish)
LCD = (170, 215, 81)
LCD_DARK = (162, 209, 73)
INK = (25, 25, 25)
FOOD = (40, 40, 40)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("📟 Nokia Snake (Retro Pixel)")

clock = pygame.time.Clock()
SCORE_FONT = pygame.font.SysFont("Arial", 24)
GAME_OVER_FONT = pygame.font.SysFont("Arial", 36)

# =========================
# Helpers
# =========================
def spawn_food(snake):
    while True:
        x = random.randrange(0, COLS) * CELL
        y = random.randrange(0, ROWS) * CELL
        if [x, y] not in snake:
            return [x, y]

def draw_grid_bg():
    screen.fill(LCD)
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, LCD_DARK, (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(screen, LCD_DARK, (0, y), (WIDTH, y), 1)

def draw_snake(snake):
    for x, y in snake:
        pygame.draw.rect(screen, INK, (x+1, y+1, CELL-2, CELL-2))

def draw_food(pos):
    x, y = pos
    pygame.draw.rect(screen, FOOD, (x+2, y+2, CELL-4, CELL-4))

# =========================
# Game Loop
# =========================
def game_loop():
    sx = (COLS // 2) * CELL
    sy = (ROWS // 2) * CELL
    snake = [[sx, sy], [sx - CELL, sy], [sx - 2*CELL, sy]]
    direction = "RIGHT"

    food = spawn_food(snake)
    score = 0
    fps = 10

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                elif e.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                elif e.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                elif e.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"

        # Move
        head = snake[0][:]
        if direction == "UP":
            head[1] -= CELL
        elif direction == "DOWN":
            head[1] += CELL
        elif direction == "LEFT":
            head[0] -= CELL
        elif direction == "RIGHT":
            head[0] += CELL
        snake.insert(0, head)

        # Eat
        if head == food:
            score += 1
            food = spawn_food(snake)
        else:
            snake.pop()

        # Game Over
        if (head[0] < 0 or head[0] >= WIDTH or
            head[1] < 0 or head[1] >= HEIGHT or
            head in snake[1:]):
            running = False

        # Draw
        draw_grid_bg()
        draw_snake(snake)
        draw_food(food)

        score_text = SCORE_FONT.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(fps)

    return score

def show_game_over(score):
    screen.fill(BLACK)
    msg = GAME_OVER_FONT.render("Game Over!", True, WHITE)
    scr = SCORE_FONT.render(f"Score: {score}", True, WHITE)
    screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//3))
    screen.blit(scr, (WIDTH//2 - scr.get_width()//2, HEIGHT//2))
    pygame.display.flip()
    time.sleep(2)

# =========================
# Main
# =========================
if __name__ == "__main__":
    while True:
        score = game_loop()
        show_game_over(score)
