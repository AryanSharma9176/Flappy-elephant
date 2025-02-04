import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 600
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_WIDTH = 60
PIPE_GAP = 150
PIPE_SPEED = 3
GROUND_HEIGHT = 50

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (135, 206, 235)
BROWN = (139, 69, 19)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Load assets
bird_img = pygame.image.load("bird.png")
bird_img = pygame.transform.scale(bird_img, (40, 30))

# Font
font = pygame.font.Font(None, 36)

# Load high score
high_score_file = "highscore.txt"
if os.path.exists(high_score_file):
    with open(high_score_file, "r") as f:
        high_score = int(f.read().strip())
else:
    high_score = 0

# Bird class
class Bird:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT // 2
        self.velocity = 0

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        if self.y > HEIGHT - GROUND_HEIGHT:
            self.y = HEIGHT - GROUND_HEIGHT
            self.velocity = 0

    def draw(self):
        screen.blit(bird_img, (self.x, self.y))

# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, 400)
        self.passed = False

    def update(self):
        self.x -= PIPE_SPEED
        if self.x + PIPE_WIDTH < 0:
            self.x = WIDTH
            self.height = random.randint(100, 400)
            self.passed = False

    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, 0, PIPE_WIDTH, self.height))
        pygame.draw.rect(screen, GREEN, (self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT - self.height - PIPE_GAP - GROUND_HEIGHT))

    def check_collision(self, bird):
        if bird.x + 40 > self.x and bird.x < self.x + PIPE_WIDTH:
            if bird.y < self.height or bird.y + 30 > self.height + PIPE_GAP:
                return True
        return False

# Game loop
def main():
    global high_score

    bird = Bird()
    pipes = [Pipe(WIDTH + i * 200) for i in range(3)]
    running = True
    score = 0

    while running:
        screen.fill(BLUE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.flap()

        bird.update()
        for pipe in pipes:
            pipe.update()
            if pipe.check_collision(bird):
                game_over(score)
                return
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                score += 1
            pipe.draw()

        # Draw ground
        pygame.draw.rect(screen, BROWN, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))

        bird.draw()

        # Display scores
        score_text = font.render(f"Score: {score}", True, WHITE)
        high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (10, 40))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

# Game over function
def game_over(score):
    global high_score

    if score > high_score:
        high_score = score
        with open(high_score_file, "w") as f:
            f.write(str(high_score))

    screen.fill((0, 0, 0))
    game_over_text = font.render("GAME OVER!", True, WHITE)
    score_text = font.render(f"Your Score: {score}", True, WHITE)
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    restart_text = font.render("Press SPACE to Restart", True, WHITE)

    screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 60))
    screen.blit(score_text, (WIDTH // 2 - 80, HEIGHT // 2 - 30))
    screen.blit(high_score_text, (WIDTH // 2 - 80, HEIGHT // 2))
    screen.blit(restart_text, (WIDTH // 2 - 120, HEIGHT // 2 + 40))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False
                main()

# Run game
if __name__ == "__main__":
    main()
