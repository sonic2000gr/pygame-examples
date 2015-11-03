#
# Bouncing ball
#

import pygame
from pygame.locals import *
from sys import exit

pygame.init()
sprite_image = 'ball1.png'
x = 100.0
y = 100.0
xwidth=640
ywidth=480
ballwidth=50
ballheight=50
xspeed = 10
yspeed = 10

screen = pygame.display.set_mode((xwidth, ywidth), 0, 32)

sprite = pygame.image.load(sprite_image)

surfacecolor= (50,80,250)

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    screen.fill(surfacecolor)
    screen.blit(sprite, (x, y))
    x += xspeed
    y += yspeed
    if (x > (640.-ballwidth) or x<=0.):
        xspeed=-xspeed
    if (y > (480.-ballheight) or y<=0.):
        yspeed=-yspeed

    pygame.display.update()
