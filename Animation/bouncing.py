#
# Bouncing balls
#

import pygame
from pygame.locals import *
from sys import exit

pygame.init()
sprite_image = 'soccer-ball.png'

#
# Initial coordinates/speeds for ball1 and ball2
#

x = 100.0
y = 100.0
x2 = 300.0
y2 = 300.0
xspeed = 50
yspeed = 50
xspeed2 = 100
yspeed2 = -100

#
# Screen resolution / initialization
#

xwidth = 640
ywidth = 480
screen = pygame.display.set_mode((xwidth, ywidth), 0, 32)
surfacecolor= (50,80,250)

#
# Initialize sprites, Clock object and set framerate
#

sprite = pygame.image.load(sprite_image)
spritewidth = sprite.get_width()
spriteheight = sprite.get_height()
clock = pygame.time.Clock()
framerate = 60

#
# Main loop
#

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    screen.fill(surfacecolor)
    screen.blit(sprite, (x, y))
    screen.blit(sprite, (x2,y2))
    time = clock.tick(framerate)/1000.0
    distance_x = time * xspeed
    distance_y = time * yspeed
    distance_x2 = time * xspeed2
    distance_y2 = time * yspeed2
    x += distance_x
    y += distance_y
    x2 += distance_x2
    y2 += distance_y2

    if (x > (640.0-spritewidth) or x<=0.0):
        xspeed = -xspeed
    if (y > (480.0-spriteheight) or y<=0.0):
        yspeed = -yspeed
    if (x2 > (640.0-spritewidth) or x2<=0.0):
        xspeed2 = -xspeed2
    if (y2 > (480.0-spriteheight) or y2<=0.0):
        yspeed2 = -yspeed2

    pygame.display.update()
