import sys

import pygame

pygame.init()

# Constants
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
LIGHT_RADIUS = 100

# Set a title for the window
pygame.display.set_caption('Haunted Mansion')
background_image = pygame.image.load('assets/images/6270a1b48d6ba9126de0dea232a0f545853fc013.jpeg')
screen.blit(background_image, (0, 0))
scaled_background = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Set up font and color
font = pygame.font.Font(None, 74)
menu_font = pygame.font.Font("PublicPixel-rv0pA.ttf", 60)
white = (255, 255, 255)

# Define menu items
menu_items = ["Start Game", "Quit"]


# def create_light_surface():
#     light_surface = pygame.Surface((WIDTH, HEIGHT))
#     light_surface.fill((0, 0, 0))  # Fill with black
#     light_surface.set_colorkey((0, 0, 0))  # Make black transparent
#     return light_surface
#
# def draw_player_light(light_surface, player_position):
#     # Get the player's position
#     player_x, player_y = player_position
#
#     # Draw a circle that represents the light area
#     pygame.draw.circle(light_surface, (255, 255, 255), (player_x, player_y), LIGHT_RADIUS)


# Function to render the main menu
def render_menu(selected_index):
    screen.blit(scaled_background, (0, 0))
    for idx, item in enumerate(menu_items):
        if idx == selected_index:
            color = (0, 255, 0)  # Highlight selected item in green
        else:
            color = white
        text_surface = menu_font.render(item, True, color)
        screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, 200 + idx * 80))
    pygame.display.flip()


pause_menu_items = ["Resume", "Quit"]

# Game state variable
paused = False


class Camera:
    def __init__(self, world_width, world_height):
        self.camera = pygame.Rect(0, 0, WIDTH, HEIGHT)
        self.world_width = world_width
        self.world_height = world_height

    def apply(self, entity):
        return entity[0] - self.camera.x, entity[1] - self.camera.y

    def update(self, target):
        # Center the camera on the player
        x = -target[0] + WIDTH // 2
        y = -target[1] + HEIGHT // 2

        # Clamp the camera's position so it stays within the world boundaries
        x = min(0, max(x, -(self.world_width - WIDTH)))  # Keep the camera in bounds horizontally
        y = min(0, max(y, -(self.world_height - HEIGHT)))  # Keep the camera in bounds vertically

        self.camera = pygame.Rect(x, y, WIDTH, HEIGHT)


# Function to render pause menu
def render_pause_menu(selected_index):
    screen.fill((0, 0, 0))  # Fill screen with black for the pause menu
    for idx, item in enumerate(pause_menu_items):
        color = (0, 255, 0) if idx == selected_index else white
        text_surface = font.render(item, True, color)
        screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 + idx * 80))
    pygame.display.flip()


# Pause menu loop
def pause_menu():
    selected_index = 0
    global paused
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(pause_menu_items)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(pause_menu_items)
                elif event.key == pygame.K_RETURN:
                    if selected_index == 0:  # Resume the game
                        paused = False
                        return
                    elif selected_index == 1:  # Quit the game
                        pygame.quit()
                        sys.exit()

        # Render the pause menu
        render_pause_menu(selected_index)


def draw_dialogue_box(screen, dialogue_text, choices, selected_choice):
    # Set the dimensions and position of the dialogue box
    box_width = 600
    box_height = 150
    box_x = (screen.get_width() - box_width) // 2
    box_y = screen.get_height() - box_height - 50  # Positioned near the bottom of the screen

    # Create a rectangle for the dialogue box
    pygame.draw.rect(screen, (50, 50, 50), (box_x, box_y, box_width, box_height))
    pygame.draw.rect(screen, (255, 255, 255), (box_x, box_y, box_width, box_height), 3)  # Border

    # Set up font
    font = pygame.font.Font(None, 28)  # You can specify a different font file if you have one

    # Render the dialogue text
    text_surface = font.render(dialogue_text, True, (255, 255, 255))
    screen.blit(text_surface, (box_x + 20, box_y + 20))

    # Render the choices
    choice_y_offset = box_y + 60
    for i, choice in enumerate(choices):
        color = (255, 255, 0) if i == selected_choice else (255, 255, 255)  # Highlight selected choice
        choice_surface = font.render(choice, True, color)
        screen.blit(choice_surface, (box_x + 40, choice_y_offset + i * 30))


def handle_dialogue_input(selected_choice, choices):
    keys = pygame.key.get_pressed()

    # Navigate up
    if keys[pygame.K_w]:
        selected_choice -= 1
        if selected_choice < 0:
            selected_choice = len(choices) - 1  # Loop back to the last option

    # Navigate down
    elif keys[pygame.K_s]:
        selected_choice += 1
        if selected_choice >= len(choices):
            selected_choice = 0  # Loop back to the first option

    # If the player presses Enter, return the selected choice
    if keys[pygame.K_RETURN]:
        return selected_choice  # Return the index of the selected choice

    return None  # No selection made yet


# Main menu loop
def main_menu():
    selected_index = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for idx, item in enumerate(menu_items):
                    text_surface = menu_font.render(item, True, white)
                    item_rect = text_surface.get_rect(center=(WIDTH // 2, 200 + idx * 80))
                    if item_rect.collidepoint(mouse_pos):
                        selected_index = idx
                        if selected_index == 0:  # "Start Game"
                            start_game()
                        elif selected_index == 2:  # "Quit"
                            pygame.quit()
                            sys.exit()

            # Handle keypress for navigating the menu (same as before)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(menu_items)
                elif event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(menu_items)
                elif event.key == pygame.K_RETURN:
                    if selected_index == 0:  # "Start Game"
                        start_game()
                    elif selected_index == 2:  # "Quit"
                        pygame.quit()
                        sys.exit()

        # Render menu
        render_menu(selected_index)


def start_game():
    # Load the frames for each direction
    forward_frames = [pygame.image.load(f'assets/images/sprites/W/W-{i}.png') for i in range(0, 4)]
    down_frames = [pygame.image.load(f'assets/images/sprites/S/S-{i}.png') for i in range(0, 4)]
    left_frames = [pygame.image.load(f'assets/images/sprites/A/A-{i}.png') for i in range(0, 4)]
    right_frames = [pygame.image.load(f'assets/images/sprites/D/D-{i}.png') for i in range(0, 4)]

    # Player movement variables
    player_x, player_y = 400, 300
    player_speed = 5
    player_direction = 'down'

    # Animation variables
    current_frame = 0
    animation_speed = 8  # 8 FPS for animation
    frame_delay = 60 // animation_speed  # Delay in game frames between animation frames
    frame_timer = 0  # To control the timing of animation frames

    global paused
    paused = False

    # Button properties for the pause menu
    button_width, button_height = 200, 50
    resume_button_rect = pygame.Rect((WIDTH // 2 - button_width // 2, HEIGHT // 2 - 60), (button_width, button_height))
    quit_button_rect = pygame.Rect((WIDTH // 2 - button_width // 2, HEIGHT // 2 + 20), (button_width, button_height))

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # Create a larger surface for rendering
    scale_factor = 2  # Scale factor (2x)
    large_width, large_height = WIDTH * scale_factor, HEIGHT * scale_factor
    large_surface = pygame.Surface((large_width, large_height))

    # # Create light surface
    # light_surface = create_light_surface()

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Pause the game when ESC is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused  # Toggle pause

            # Check for mouse clicks in pause menu
            if paused and event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button_rect.collidepoint(event.pos):
                    paused = False  # Resume game
                elif quit_button_rect.collidepoint(event.pos):
                    running = False  # Quit game

        if paused:
            # Render the pause menu with buttons
            large_surface.fill((50, 50, 50))

            # Render text for pause menu
            font = pygame.font.Font('PublicPixel-rv0pA.ttf', 74)
            text = font.render("Paused", True, (255, 255, 255))
            large_surface.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 150))

            # Render buttons
            pygame.draw.rect(large_surface, (100, 200, 100), resume_button_rect)  # Resume button (green)
            pygame.draw.rect(large_surface, (200, 100, 100), quit_button_rect)  # Quit button (red)

            # Add button text
            small_font = pygame.font.Font('PublicPixel-rv0pA.ttf', 50)
            resume_text = small_font.render("Resume", True, (255, 255, 255))
            quit_text = small_font.render("Quit", True, (255, 255, 255))
            large_surface.blit(resume_text, (resume_button_rect.x + (button_width // 2 - resume_text.get_width() // 2),
                                             resume_button_rect.y + (
                                                         button_height // 2 - resume_text.get_height() // 2)))
            large_surface.blit(quit_text, (quit_button_rect.x + (button_width // 2 - quit_text.get_width() // 2),
                                           quit_button_rect.y + (button_height // 2 - quit_text.get_height() // 2)))

            pygame.display.flip()
            continue  # Skip game logic while paused

        # Handle player movement
        keys = pygame.key.get_pressed()
        # Initialize the camera with the world size
        camera = Camera(2048, 1536)  # World size (example)

        screen.fill((0, 0, 0))

        # Handle player movement with boundary checks
        if keys[pygame.K_w]:
            player_y = max(0, player_y - player_speed)
            player_direction = 'up'
        elif keys[pygame.K_s]:
            player_y = min(camera.world_height - forward_frames[0].get_height(), player_y + player_speed)
            player_direction = 'down'
        elif keys[pygame.K_a]:
            player_x = max(0, player_x - player_speed)
            player_direction = 'left'
        elif keys[pygame.K_d]:
            player_x = min(camera.world_width - forward_frames[0].get_width(), player_x + player_speed)
            player_direction = 'right'

        # Update the camera position to follow the player
        camera.update((player_x, player_y))

        # Draw the player based on direction and current animation frame
        if player_direction == 'up':
            screen.blit(forward_frames[current_frame], camera.apply((player_x, player_y)))
        elif player_direction == 'down':
            screen.blit(down_frames[current_frame], camera.apply((player_x, player_y)))
        elif player_direction == 'left':
            screen.blit(left_frames[current_frame], camera.apply((player_x, player_y)))
        elif player_direction == 'right':
            screen.blit(right_frames[current_frame], camera.apply((player_x, player_y)))

        # # Draw the player's light on the light surface
        # light_surface.fill((0, 0, 0))  # Reset the light surface
        # draw_player_light(light_surface, (player_x, player_y))
        #
        # # Draw the light surface on the main screen
        # screen.blit(light_surface, (0, 0))

        # Update the display
        pygame.display.flip()

        # Cap the frame rate at 60 FPS
        clock.tick(60)


main_menu()
pygame.quit()
