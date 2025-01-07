import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Paddle settings
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
PADDLE_SPEED = 10

# Ball settings
BALL_RADIUS = 8
BALL_SPEED = 5

# Brick settings
BRICK_ROWS = 5
BRICK_COLUMNS = 8
BRICK_WIDTH = WIDTH // BRICK_COLUMNS
BRICK_HEIGHT = 20

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Paddle
paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 50, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_dx = random.choice([-BALL_SPEED, BALL_SPEED])
ball_dy = -BALL_SPEED

# Bricks
bricks = [
    pygame.Rect(col * BRICK_WIDTH, row * BRICK_HEIGHT, BRICK_WIDTH, BRICK_HEIGHT)
    for row in range(BRICK_ROWS)
    for col in range(BRICK_COLUMNS)
]

def draw():
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLUE, paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    for brick in bricks:
        pygame.draw.rect(screen, RED, brick)
    pygame.display.flip()

def move_paddle():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= PADDLE_SPEED
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.x += PADDLE_SPEED

def move_ball():
    global ball_dx, ball_dy
    ball.x += ball_dx
    ball.y += ball_dy

    # Wall collision
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_dx = -ball_dx
    if ball.top <= 0:
        ball_dy = -ball_dy

    # Paddle collision
    if ball.colliderect(paddle):
        ball_dy = -BALL_SPEED

    # Brick collision
    for brick in bricks[:]:
        if ball.colliderect(brick):
            bricks.remove(brick)
            ball_dy = -ball_dy
            break

    # Bottom collision
    if ball.bottom >= HEIGHT:
        return False

    return True

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    move_paddle()
    if not move_ball():
        print("Game Over!")
        running = False

    draw()
    clock.tick(60)

pygame.quit()
