import pygame
import random
import time
import math

# Initialize pygame and set up display
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Aim Trainer")

# Colors
WHITE = (255, 255, 255)
BG_COLOR = (30, 30, 60)  # Dark background color
BLACK = (0, 0, 0)

# Circle Properties
TARGET_RADIUS_MIN = 8   # Smaller circle size
TARGET_RADIUS_MAX = 25
TARGET_GROWTH_SPEED = 0.3

# Game variables
score = 0
reaction_times = []
time_limit = 2  # Time in seconds to click on a target before game over
start_time = time.time()
circles = [{'pos': (random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50)),
            'radius': TARGET_RADIUS_MIN, 'growing': True}]

# Font for displaying text
font = pygame.font.SysFont("Arial", 24)

def draw_circles(circles):
    """Draw all circles with gradient effect."""
    for circle in circles:
        gradient_color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        pygame.draw.circle(screen, gradient_color, circle['pos'], int(circle['radius']))
        pygame.draw.circle(screen, WHITE, circle['pos'], int(circle['radius'] // 2))

def update_circles(circles):
    """Update the size of all circles (grow/shrink)."""
    for circle in circles:
        if circle['growing']:
            circle['radius'] += TARGET_GROWTH_SPEED
            if circle['radius'] >= TARGET_RADIUS_MAX:
                circle['growing'] = False
        else:
            circle['radius'] -= TARGET_GROWTH_SPEED
            if circle['radius'] <= TARGET_RADIUS_MIN:
                circle['growing'] = True

def check_click(circles, mouse_pos):
    """Check if any circle was clicked."""
    global score, TARGET_GROWTH_SPEED
    for circle in circles:
        distance = math.hypot(mouse_pos[0] - circle['pos'][0], mouse_pos[1] - circle['pos'][1])
        if distance <= circle['radius']:
            score += 1
            reaction_times.append(time.time() - start_time)

            TARGET_GROWTH_SPEED += 0.05

            if score % 3 == 0:
                circles.append({'pos': (random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50)),
                                'radius': TARGET_RADIUS_MIN, 'growing': True})

            circle['pos'] = (random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50))
            circle['radius'] = TARGET_RADIUS_MIN
            circle['growing'] = True
            return True
    return False

# Game loop
running = True
while running:
    screen.fill(BG_COLOR)
    draw_circles(circles)
    update_circles(circles)

    clicked = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            clicked = check_click(circles, pygame.mouse.get_pos())
            if clicked:
                start_time = time.time()

    if not clicked and time.time() - start_time > time_limit:
        running = False

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    pygame.time.delay(10)

# Game Over screen
screen.fill(BG_COLOR)
average_reaction = sum(reaction_times) / len(reaction_times) if reaction_times else 0
end_text = font.render(f"Game Over! Avg Reaction: {average_reaction:.2f}s, Score: {score}", True, WHITE)
screen.blit(end_text, (SCREEN_WIDTH // 2 - end_text.get_width() // 2, SCREEN_HEIGHT // 2))
pygame.display.flip()
time.sleep(3)
pygame.quit()