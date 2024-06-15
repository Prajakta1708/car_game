import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants for the screen size and colors
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Car Game")

# Load images
car_image = pygame.image.load('car.png')  # Replace 'car.png' with your car image path
car_image = pygame.transform.scale(car_image, (50, 100))  # Resize the car image if needed

# Variables for the car
car_rect = car_image.get_rect()
car_rect.centerx = SCREEN_WIDTH // 2
car_rect.bottom = SCREEN_HEIGHT - 20
car_speed = 5

# Variables for car movement
car_vel_x = 0
car_vel_y = 0
acceleration = 0.2  # Acceleration factor
friction = 0.1  # Friction factor

# Variables for obstacles
initial_obstacle_speed = 5
obstacle_width = 100
obstacle_height = 20
obstacles = []
max_obstacles = 10
obstacle_spawn_counter = 0
obstacle_spawn_rate = 60  

crash_sound = pygame.mixer.Sound('crash-77686.mp3')  # Replace with your crash sound file
crash_sound.set_volume(0.5)  


font = pygame.font.Font(None, 48)

# Game state
game_over = False

# Function to create a new obstacle
def create_obstacle():
    obstacle_x = random.randint(0, SCREEN_WIDTH - obstacle_width)
    obstacle_y = -obstacle_height
    obstacle_speed = random.randint(initial_obstacle_speed - 2, initial_obstacle_speed + 2)  # Random speed variation
    obstacle = pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)
    return obstacle, obstacle_speed

# Add initial obstacles
for _ in range(5):
    obstacle, speed = create_obstacle()
    obstacles.append((obstacle, speed))

# Game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Check if game over
    if not game_over:
        # Control the car's movement
        keys = pygame.key.get_pressed()

        # Horizontal movement
        if keys[pygame.K_LEFT]:
            car_vel_x -= acceleration
        elif keys[pygame.K_RIGHT]:
            car_vel_x += acceleration
        else:
            car_vel_x *= (1 - friction)  # Apply friction

        # Vertical movement (forward and backward)
        if keys[pygame.K_UP]:
            car_vel_y -= acceleration
        elif keys[pygame.K_DOWN]:
            car_vel_y += acceleration
        else:
            car_vel_y *= (1 - friction)  # Apply friction

        # Update car position based on velocity
        car_rect.x += car_vel_x
        car_rect.y += car_vel_y

        # Ensure the car stays within the screen bounds
        if car_rect.left < 0:
            car_rect.left = 0
        if car_rect.right > SCREEN_WIDTH:
            car_rect.right = SCREEN_WIDTH
        if car_rect.top < 0:
            car_rect.top = 0
        if car_rect.bottom > SCREEN_HEIGHT:
            car_rect.bottom = SCREEN_HEIGHT

        # Spawn new obstacles periodically
        obstacle_spawn_counter += 1
        if obstacle_spawn_counter >= obstacle_spawn_rate and len(obstacles) < max_obstacles:
            obstacle, speed = create_obstacle()
            obstacles.append((obstacle, speed))
            obstacle_spawn_counter = 0

        # Move obstacles and check collisions
        for obstacle, speed in obstacles[:]:
            obstacle.y += speed

            # Check collision with the car
            if obstacle.colliderect(car_rect):
                game_over = True
                crash_sound.play()

            # Remove obstacles that are off-screen
            if obstacle.y > SCREEN_HEIGHT:
                obstacles.remove((obstacle, speed))

        # Clear the screen
        screen.fill(WHITE)

        # Draw the car on the screen
        screen.blit(car_image, car_rect)

        # Draw obstacles
        for obstacle, _ in obstacles:
            pygame.draw.rect(screen, BLACK, obstacle)

    else:  # Game over state
        # Display game over text overlay
        game_over_text = font.render("Crashed! Game Over", True, BLACK)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(game_over_text, text_rect)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    pygame.time.Clock().tick(60)