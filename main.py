# Example file showing a circle moving on screen
import pygame
import math

# pygame setup
pygame.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

keys = pygame.key.get_pressed()
oldPressed = keys

bg = pygame.image.load("img/flappy_bg.png").convert()

# background logic
scroll = 0
tiles = math.ceil(screen.get_width() / bg.get_width()) + 1

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # draw scrolling background
    for i in range(0, tiles):
        screen.blit(bg, (i * bg.get_width() + scroll, 0))

    # scroll background
    scroll -= 300 * dt  # scroll speed
    if abs(scroll) > bg.get_width():
        scroll = 0

    pygame.draw.circle(screen, "black", player_pos, 40)

    # Jucatorul cade continuu ca la flappy
    player_pos.y += 350 * dt

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and not oldPressed[pygame.K_SPACE]:
        player_pos.y -= 10000 * dt  # viteza cu care cade jucatorul

    # protectie sa nu iasa din ecran
    if player_pos.y > screen.get_height():
        player_pos.y = screen.get_height() / 2
    if player_pos.y < 0:
        player_pos.y = 35

    oldPressed = keys

    # flip() the display to put your work on screen
    pygame.display.update()
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
