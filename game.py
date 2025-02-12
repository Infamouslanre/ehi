import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 600  # Narrower screen
HEIGHT = 800  # Taller screen

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BRICK_COLOR = (139, 69, 19)  # Brown color for bricks

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Save the World: Recycle Game")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Load images (you can replace these with your own images)
hero_img = pygame.Surface((50, 50))
hero_img.fill(GREEN)

recyclable_img = pygame.Surface((30, 30))
recyclable_img.fill(BLUE)  # Blue for recyclable items

non_recyclable_img = pygame.Surface((30, 30))
non_recyclable_img.fill(RED)  # Red for non-recyclable items

# Font for displaying score, timer, and game over message
font = pygame.font.Font(None, 36)

# Game variables
hero_x = WIDTH // 2 - 25
hero_y = HEIGHT - 100
hero_speed = 5

initial_item_speed = 2  # Starting speed of items
item_speed = initial_item_speed
items = []
score = 0
countdown_time = 60  # 60-second countdown
start_time = pygame.time.get_ticks()  # Start time in milliseconds

# Health system
max_health = 3
health = max_health

# Brick walls
wall_width = 50  # Width of each brick wall
spawn_area_left = wall_width  # Left boundary for item spawning
spawn_area_right = WIDTH - wall_width - 30  # Right boundary for item spawning

# Maximum number of items allowed on screen
max_items_on_screen = 5

# Function to check if two items overlap
def items_overlap(new_item, existing_items):
    for item in existing_items:
        if (
            new_item["x"] < item["x"] + 30
            and new_item["x"] + 30 > item["x"]
            and new_item["y"] < item["y"] + 30
            and new_item["y"] + 30 > item["y"]
        ):
            return True
    return False

# Function to spawn items without overlapping
def spawn_item():
    if len(items) >= max_items_on_screen:  # Don't spawn if too many items are on screen
        return

    attempts = 0
    while attempts < 100:  # Try up to 100 times to find a non-overlapping position
        item_type = random.choice(["recyclable", "non_recyclable"])
        item_x = random.randint(spawn_area_left, spawn_area_right)  # Spawn within the narrowed area
        item_y = -30
        new_item = {"type": item_type, "x": item_x, "y": item_y}

        if not items_overlap(new_item, items):
            items.append(new_item)
            break
        attempts += 1

# Function to reset the game
def reset_game():
    global hero_x, hero_y, items, score, countdown_time, item_speed, start_time, health
    hero_x = WIDTH // 2 - 25
    hero_y = HEIGHT - 100
    items = []
    score = 0
    countdown_time = 60
    item_speed = initial_item_speed
    start_time = pygame.time.get_ticks()
    health = max_health

# Function to format the countdown timer
def format_time(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02}:{seconds:02}"

# Function to draw brick walls
def draw_walls():
    pygame.draw.rect(screen, BRICK_COLOR, (0, 0, wall_width, HEIGHT))  # Left wall
    pygame.draw.rect(screen, BRICK_COLOR, (WIDTH - wall_width, 0, wall_width, HEIGHT))  # Right wall

# Main game loop
def game_loop():
    global hero_x, hero_y, score, countdown_time, item_speed, health

    running = True
    game_over = False

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_r:  # Press 'R' to restart
                    reset_game()
                    game_over = False

        if not game_over:
            # Move the hero
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and hero_x > wall_width:  # Stop at the left wall
                hero_x -= hero_speed
            if keys[pygame.K_RIGHT] and hero_x < WIDTH - wall_width - 50:  # Stop at the right wall
                hero_x += hero_speed

            # Spawn items
            if random.randint(1, 30) == 1:
                spawn_item()

            # Move items and check for collisions
            for item in items[:]:
                item["y"] += item_speed

                # Check for collision with hero
                if (
                    hero_x < item["x"] + 30
                    and hero_x + 50 > item["x"]
                    and hero_y < item["y"] + 30
                    and hero_y + 50 > item["y"]
                ):
                    if item["type"] == "recyclable":
                        score += 1
                        countdown_time += 2  # Increase time by 2 seconds
                    else:
                        health -= 0.5  # Lose half a heart
                        if health <= 0:
                            game_over = True
                    items.remove(item)

                # Remove items that go off-screen
                if item["y"] > HEIGHT:
                    if item["type"] == "recyclable":
                        countdown_time -= 2  # Decrease time by 2 seconds for missing recyclable items
                    items.remove(item)

            # Update item speed based on elapsed time
            elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # Convert to seconds
            item_speed = initial_item_speed + elapsed_time // 10  # Increase speed over time

            # Update countdown timer
            remaining_time = countdown_time - elapsed_time  # Calculate remaining time
            if remaining_time <= 0:
                game_over = True

        # Draw the brick walls
        draw_walls()

        # Draw the hero
        screen.blit(hero_img, (hero_x, hero_y))

        # Draw the items
        for item in items:
            if item["type"] == "recyclable":
                screen.blit(recyclable_img, (item["x"], item["y"]))
            else:
                screen.blit(non_recyclable_img, (item["x"], item["y"]))

        # Draw the score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (wall_width + 10, 10))

        # Draw the countdown timer
        timer_text = font.render(f"Time: {format_time(remaining_time)}", True, WHITE)
        screen.blit(timer_text, (WIDTH - wall_width - 150, 10))

        # Draw the health system
        heart_text = font.render(f"Hearts: {health}", True, WHITE)
        screen.blit(heart_text, (WIDTH // 2 - 50, 10))

        # Game over message
        if game_over:
            game_over_text = font.render("Game Over! Press R to Restart", True, WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2))

        # Update the display
        pygame.display.flip()
        clock.tick(60)

# Start the game
game_loop()