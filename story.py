import pygame

pygame.init()

# Define window dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set a title for the window
pygame.display.set_caption('Haunted Mansion')
background_image = pygame.image.load('assets/images/1597767eb8c52fe21da17e881be43010-3137771454.jpg')
screen.blit(background_image, (0, 0))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color (e.g., black)
    screen.fill((0, 0, 0))

    player_x, player_y = 100, 100
    player_speed = 5

    # Load player sprite
    player_sprite = pygame.image.load('assets/images/Screenshot_2024-10-3_14714955.png')

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
        if keys[pygame.K_UP]:
            player_y -= player_speed
        if keys[pygame.K_DOWN]:
            player_y += player_speed

        # Clear the screen and redraw the background and player
        screen.fill((0, 0, 0))
        screen.blit(background_image, (0, 0))
        screen.blit(player_sprite, (player_x, player_y))

        pygame.display.flip()

pygame.quit()
