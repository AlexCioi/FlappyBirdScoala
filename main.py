import pygame
import math
import random

# pygame setup
pygame.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
player_rect = pygame.Rect(player_pos.x, player_pos.y, 150, 150)  # Create a Rect for the player

keys = pygame.key.get_pressed()
oldPressed = keys

bg = pygame.image.load("img/flappy_bg.png").convert()
player_img = pygame.image.load("img/bird.png").convert_alpha()  # incarca imaginea player-ului
player_img = pygame.transform.scale(player_img, (150, 150))

# background logic
scroll = 0
tiles = math.ceil(screen.get_width() / bg.get_width()) + 1

pipes = []
pipe_timer = 0

class Pipe:
    def __init__(self, x):
        self.x = x
        self.top_height = random.randint(50, 400)
        self.bottom_height = 720 - self.top_height - 200
        self.width = 80
        self.speed = 300

    def move(self, dt):
        self.x -= self.speed * dt

    def draw(self):
        pygame.draw.rect(screen, (0, 255, 0), (self.x, 0, self.width, self.top_height))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, 720 - self.bottom_height, self.width, self.bottom_height))

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

    screen.blit(player_img, player_pos)  # afisarea playerului dupa imagine

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

    # se genereaza pipe uri dupa timer
    pipe_timer += dt
    if pipe_timer >= 2:  # Adjust this value to change the frequency of pipes
        pipes.append(Pipe(1280))
        pipe_timer = 0

    # aici se face update la pipe uri
    for pipe in pipes:
        pipe.move(dt)
        pipe.draw()

    # aici se verifica coliziunea

    for pipe in pipes:
        if player_rect.colliderect(pygame.Rect(pipe.x, 0, pipe.width, pipe.top_height)) or \
                player_rect.colliderect(pygame.Rect(pipe.x, 720 - pipe.bottom_height, pipe.width, pipe.bottom_height)):
            print("Collision!")
            player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
            player_rect = pygame.Rect(player_pos.x, player_pos.y, 150, 150)
            pipes.clear()  # aici o iau pipe urile de la capat

    # flip() the display to put your work on screen
    pygame.display.update()
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
