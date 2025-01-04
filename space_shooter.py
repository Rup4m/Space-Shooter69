import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Clock for controlling FPS
clock = pygame.time.Clock()

# Load images
bg_image = pygame.image.load("background2.png")  # Replace with your image path
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))  # Scale to fit the screen

player_img = pygame.image.load("player.png")  # Replace with your image path
player_img = pygame.transform.scale(player_img, (50, 50))

bullet_img = pygame.image.load("bullet1.png")  # Replace with your image path
bullet_img = pygame.transform.scale(bullet_img, (50, 50))

enemy_img = pygame.image.load("enemy.png")  # Replace with your image path
enemy_img = pygame.transform.scale(enemy_img, (50, 50))

shield_img = pygame.image.load("shield.png")  # Replace with your image path
shield_img = pygame.transform.scale(shield_img, (50, 50))  # Resize shield image to fit the player

# Font for displaying text
font = pygame.font.Font(None, 36)

# Function to reset game variables
def reset_game():
    global player_x, player_y, score, lives, bullets, enemies, enemy_spawn_timer, level, enemy_speed, enemy_spawn_rate, shield_active, shield_timer
    player_x = WIDTH // 2
    player_y = HEIGHT - 100
    score = 0
    lives = 3
    bullets = []
    enemies = []
    enemy_spawn_timer = 0
    level = 1
    enemy_speed = 3  # Starting enemy speed
    enemy_spawn_rate = 50  # Starting spawn rate
    shield_active = False
    shield_timer = 0

# Game variables
player_x = WIDTH // 2
player_y = HEIGHT - 100
player_speed = 5
bullet_speed = -7
enemy_speed = 3
enemy_spawn_rate = 50  # Frames between spawns
level = 1
shield_active = False
shield_timer = 0

# Power-up class
class PowerUp:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        if self.type == "shield":
            self.image = shield_img

    def move(self):
        self.y += 3  # Power-up moves down the screen

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

# Spawn power-ups randomly
def spawn_power_up():
    if random.random() < 0.01:  # 1% chance to spawn a power-up
        type = random.choice(["shield"])  # Only spawn shield power-ups
        x = random.randint(0, WIDTH - 50)
        y = -30
        return PowerUp(x, y, type)
    return None

# Game loop flag
running = True

# Main game loop
while running:
    reset_game()

    while lives > 0:  # Game is running
        screen.fill(BLACK)  # Fill with black first to ensure no leftover screen artifacts

        # Draw the background
        screen.blit(bg_image, (0, 0))  # Draw the background image at the top-left corner

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - 50:
            player_x += player_speed
        if keys[pygame.K_SPACE]:
            # Add bullet if it's not already spamming
            if len(bullets) == 0 or bullets[-1][1] < player_y - 50:
                bullets.append([player_x + 22, player_y])

        # Update bullets
        for bullet in bullets[:]:
            bullet[1] += bullet_speed
            if bullet[1] < 0:
                bullets.remove(bullet)

        # Spawn enemies
        enemy_spawn_timer += 1
        if enemy_spawn_timer >= enemy_spawn_rate:
            enemy_x = random.randint(0, WIDTH - 50)
            enemies.append([enemy_x, -50])
            enemy_spawn_timer = 0

        # Update enemies
        for enemy in enemies[:]:
            enemy[1] += enemy_speed
            if enemy[1] > HEIGHT:  # Enemy leaves the screen
                enemies.remove(enemy)
            elif player_x < enemy[0] < player_x + 50 and player_y < enemy[1] < player_y + 50:
                # Collision with player
                if not shield_active:  # If no shield, player loses life
                    enemies.remove(enemy)
                    lives -= 1
                    if lives <= 0:
                        # Game Over, show the Game Over screen
                        print("Game Over!")
                        break
                else:
                    # If shield is active, ignore damage
                    enemies.remove(enemy)

        # Collision detection (bullets and enemies)
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if (
                    bullet[0] > enemy[0] and bullet[0] < enemy[0] + 50
                    and bullet[1] > enemy[1] and bullet[1] < enemy[1] + 50
                ):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 1
                    break

        # Level up when score reaches threshold
        if score >= level * 10:  # Increase level every 10 points
            level += 1
            enemy_speed += 1  # Increase enemy speed with each level
            enemy_spawn_rate -= 5  # Increase spawn rate (decrease time between enemy spawns)
            print(f"Level Up! Now at level {level}")

        # Draw player
        screen.blit(player_img, (player_x, player_y))

        # Draw bullets
        for bullet in bullets:
            screen.blit(bullet_img, (bullet[0], bullet[1]))

        # Draw enemies
        for enemy in enemies:
            screen.blit(enemy_img, (enemy[0], enemy[1]))

        # Draw shield if active
        if shield_active:
            screen.blit(shield_img, (player_x, player_y))  # Draw shield over player

        # Display score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Display lives
        lives_text = font.render(f"Lives: {lives}", True, RED)
        screen.blit(lives_text, (WIDTH - 120, 10))

        # Display level
        level_text = font.render(f"Level: {level}", True, BLUE)
        screen.blit(level_text, (WIDTH - 120, 40))

        # Update screen
        pygame.display.flip()
        clock.tick(60)

        # Handle shield timer
        if shield_active and pygame.time.get_ticks() - shield_timer > 5000:  # Shield lasts for 5 seconds
            shield_active = False

        # Spawn power-ups
        power_up = spawn_power_up()
        if power_up:
            power_up.move()
            power_up.draw()

            # Power-up collision detection
            if player_x < power_up.x < player_x + 50 and player_y < power_up.y < player_y + 50:
                if power_up.type == "shield":
                    shield_active = True
                    shield_timer = pygame.time.get_ticks()  # Start shield timer
                power_up = None  # Remove power-up after collection

    # Game Over Screen
    game_over_text = font.render("Game Over! Press R to Restart or Q to Quit", True, RED)
    screen.fill(BLACK)
    screen.blit(game_over_text, (WIDTH // 4, HEIGHT // 2))
    pygame.display.flip()

    # Wait for player input to either restart or quit
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                waiting_for_input = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Reset the game and restart
                    reset_game()
                    waiting_for_input = False
                elif event.key == pygame.K_q:
                    # Quit the game
                    running = False
                    waiting_for_input = False

pygame.quit()
