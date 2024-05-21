import pygame
import math
import random

class Pipe:
    def __init__(self, x, speed):
        self.x = x
        self.top_height = random.randint(50, 400)
        self.bottom_height = 720 - self.top_height - 200
        self.width = 80
        self.speed = speed
        self.passed = False

    def move(self, dt):
        self.x -= self.speed * dt

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.x, 0, self.width, self.top_height))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, 720 - self.bottom_height, self.width, self.bottom_height))


class powerup:
    def __init__(self, x, speed):
        self.x = x - random.randint(0 ,200)
        self.speed = speed
        self.y = screen.get_height()/2 - 20 - random.randint(-200,200)
        self.rect = pygame.Rect(x-20,  self.y - 20,40,40)

    def move(self, dt):
        self.x -= self.speed * dt
        self.rect = pygame.Rect(self.x-20,  self.y - 20,40,40)
    def draw(self,screen):
        screen.blit(catavape, pygame.math.Vector2(self.rect.x, self.rect.y))  # afisarea playerului dupa imagine


# pygame setup
pygame.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
player_bbox = pygame.Rect(player_pos.x-20,player_pos.y-20,40,40)
vertical_vel = 0

keys = pygame.key.get_pressed()
oldPressed = keys

bg = pygame.image.load("img/flappy_bg.png").convert()

flappyimg = pygame.image.load("img/flapy.png").convert()
if random.randint(0 ,100) > 75: #randomursu
    flappyimg = pygame.image.load("img/ursu.jpg").convert()

catavape = pygame.image.load("img/catavape.png").convert()

# background logic
scroll = 0
tiles = math.ceil(screen.get_width() / bg.get_width()) + 1

pipes = []
powerups = []
pipe_timer = 0

reset = False

score = 0

scroll_speed = 400
gravity = 450
jumping = 1200

pygame.font.init() # you have to call this at the start,
                   # if you want to use this module.
my_font = pygame.font.SysFont('Comic Sans MS', 30)

while running:
    if reset:
        vertical_vel = 0
        scroll = 0
        player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        keys = pygame.key.get_pressed()
        oldPressed = keys
        reset = False
        pipes.clear()
        powerups.clear()
        player_bbox = pygame.Rect(player_pos.x - 20, player_pos.y - 20, 40, 40)
        score = 0

    # poll for events / nu e problema noastra credits pygame
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # draw scrolling background
    for i in range(0, tiles):
        screen.blit(bg, (i * bg.get_width() + scroll, 0))

    keys = pygame.key.get_pressed()

    # scroll background
    scroll -= scroll_speed * dt  # scroll speed
    if abs(scroll) > bg.get_width():
        scroll = 0

    text_surface = my_font.render(str(score), False, (0, 0, 0))
    screen.blit(text_surface, (0, 0))

    # Jucatorul cade continuu ca la flappy
    player_pos.y += gravity * dt

    # bum
    if keys[pygame.K_SPACE] and not oldPressed[pygame.K_SPACE] and player_pos.y > 75:
        vertical_vel = -jumping  # sare vere

    # bumti bumti
    if vertical_vel != 0:
        player_pos.y += vertical_vel*dt
        vertical_vel += 50

    player_bbox = pygame.Rect(player_pos.x - 20, player_pos.y - 20 , 30, 30)

    #moarte cerebrala
    if player_pos.y - 35 > screen.get_height():
        reset = True

        # se genereaza pipe uri dupa timer
    pipe_timer += dt
    if pipe_timer >= 2:  # Adjust this value to change the frequency of pipes
        pipes.append(Pipe(1280,scroll_speed))
        pipe_timer = 0
        if random.randint(0, 100) > 75:
            powerups.append((powerup(1100,scroll_speed)))



    # aici se face update la pipe uri
    for pipe in pipes:
        pipe.move(dt)
        pipe.draw(screen)

    for power in powerups:
        power.move(dt)
        power.draw(screen)

    for pipe in pipes:
        if player_bbox.colliderect(pygame.Rect(pipe.x, 0, pipe.width, pipe.top_height)) or \
                player_bbox.colliderect(pygame.Rect(pipe.x, 720 - pipe.bottom_height, pipe.width, pipe.bottom_height)):
            reset = True
        if player_pos.x > pipe.x + pipe.width and not pipe.passed:
            pipe.passed = True
            score += 1


    for power in powerups:
        if player_bbox.colliderect((power.rect)):
            trecemprin = True


    #varu la sfarsit sa nu avem lag
    #pygame.draw.rect(screen, "white", player_bbox)
    screen.blit(flappyimg, pygame.math.Vector2(player_pos.x - 20, player_pos.y - 20))  # afisarea playerului dupa imagine




    oldPressed = keys

    # flip() the display to put your work on screen / nu e problema noastra credits pygame
    pygame.display.update()
    pygame.display.flip()


    # limits FPS to 60 / nu e problema noastra credits pygame
    # dt is delta time in seconds since last frame, used for framerate-independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
