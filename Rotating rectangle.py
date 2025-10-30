import pygame
import math

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rotating Rectangle")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Rectangle properties
rect_width, rect_height = 100, 50
rect_center = (WIDTH // 2, HEIGHT // 2)
angle = 0
rotation_speed = 10  # Degrees per frame

# Main loop
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(WHITE)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Rotate rectangle
    rotated_rect = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
    rotated_rect.fill(RED)
    rotated_rect = pygame.transform.rotate(rotated_rect, angle)
    rect_pos = rotated_rect.get_rect(center=rect_center)
    
    screen.blit(rotated_rect, rect_pos)
    
    pygame.display.flip()
    
    # Update angle
    angle += rotation_speed
    angle %= 360
    
    clock.tick(30)  # Limit FPS to 30

pygame.quit()