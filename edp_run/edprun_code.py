import pygame
import time
import threading
import random
import math

# pygame setup
pygame.init()
pygame.font.init()
font = pygame.font.Font(pygame.font.get_default_font(), 36)
screen = pygame.display.set_mode((700, 700))
clock = pygame.time.Clock()
running = True
player_pos = pygame.Vector2(screen.get_width() / 2 - 50, 500)
background_pos = pygame.Vector2(0,0)
car_pos = pygame.Vector2(0,0)
dt = 0
background = pygame.image.load('road.png')
title_surface = pygame.image.load('title.png')
car = pygame.image.load('cupcake.png')
player = pygame.image.load('edp.png')
background_rect = background.get_rect()
speed = 800
score = 0
text_surface = font.render('Score: ' + str(score), False, (255, 255, 255))
alive = True
player_rect = player.get_rect()
car_rect = car.get_rect()
objects = []
gamestarted = True

def my_function():
    global score
    global background_pos
    while True and alive == True:
        score += 1
        time.sleep(1)

# Create a thread that runs the function
my_thread = threading.Thread(target=my_function)
my_thread.start()

class GameObject:

    def __init__(self, image, height, speed):
        global nocars
        global score

        nocars += 1

        self.speed = speed

        self.image = image

        self.pos = image.get_rect().move(0, height)

        self.pos.y = 0 - random.randrange(10, 200)

        self.pos.x = random.randrange(50,600)

        self.move()

    def move(self):

        self.pos = self.pos.move(self.speed, 0)

        while any(self.pos.colliderect(o.pos) for o in objects if self != o):
            self.pos.x = random.randrange(50, 600)

        if self.pos.y > 750:
            if self.pos.y >= 750:
                self.pos.y = 0 - random.randrange(10, 200)
                #while any(self.pos.colliderect(o.pos) for o in objects if self != o):
                self.pos.x = random.randrange(50, 600)
                time.sleep(0.01)
        elif alive == True:
            self.pos.y += score * 20 * dt
            #time.sleep(0.01)

def roadmove():
    global background_pos
    while True and alive == True:
        if background_pos.y >= 0:
            background_pos.y = -700
            time.sleep(0.01)
        elif score < 10:
            background_pos.y += score * 15 * dt
            time.sleep(0.01)
        else:
            background_pos.y += score * 10 * dt
            time.sleep(0.01)


# Create a thread that runs the function
my_thread2 = threading.Thread(target=roadmove)
my_thread2.start()

nocars = 0

while running:
    if gamestarted == True:

        if nocars < 4:
            o = GameObject(car, 0, 0)
            objects.append(o)

        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("purple")

        screen_center = (
        ( 0),
        ( 0)
        )

        background = pygame.transform.scale(background, (700, 1400))
        screen.blit(background, (background_pos))
        #screen.blit(car, (car_pos))
        screen.blit(text_surface, (screen_center))

        player_rect = player.get_rect(topleft=(player_pos.x, player_pos.y))



        for o in objects:
            o.move()
            object_rect = o.image.get_rect(topleft=(o.pos.x, o.pos.y))

            screen.blit(o.image, o.pos)
            screen.blit(text_surface, (screen_center))

            if player_rect.colliderect(object_rect) and pygame.time.get_ticks() > 1000:
                alive = False
                screen.fill("black")
                x_position = (screen.get_width() - title_surface.get_width()) / 2
                y_position = (screen.get_height() - title_surface.get_height()) / 2 - 10

                # Draw the surface in the middle of the screen
                screen.blit(title_surface, (x_position, y_position))
                screen.blit(text_surface, (screen.get_width() / 2 - text_surface.get_width() / 2, screen.get_height() / 2))


        # drawing background and graphoics thing here

        #pygame.draw.circle(screen, "red", player_pos, 40)

        screen.blit(player, (player_pos.x, player_pos.y))

        text_surface = font.render('Score: ' + str(score), False, (255, 255, 255))

        keys = pygame.key.get_pressed()
        if alive == True:
            # W key
            #if keys[pygame.K_w]:
                #if player_pos.y < 0:
                #    player_pos.y += speed * dt
                #else:
                #    player_pos.y -= speed * dt
            # S key
            if keys[pygame.K_SPACE]:
                gamestarted = True
            # A key
            if keys[pygame.K_a]:
                if player_pos.x < -50:
                    player_pos.x = 700
                else:
                    player_pos.x -= speed * dt
            # D key
            if keys[pygame.K_d]:
                if player_pos.x > 700:
                    player_pos.x = -50
                else:
                    player_pos.x += speed * dt
        


    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60
    dt = clock.tick(60) / 1000


pygame.quit()