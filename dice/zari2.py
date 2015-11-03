# -*- coding: utf-8 -*-
#
# Zari
#

import pygame
from random import randint
from pygame.locals import *
from sys import exit

pygame.init()
sprite_image = ['face1.png','face2.png','face3.png','face4.png',
                'face5.png','face6.png']

class Zari:
    def __init__(self):
        self.faces =[]
        for face in sprite_image:
            self.faces.append(pygame.image.load(face))
        self.width = self.faces[0].get_width()
        self.height = self.faces[0].get_height()
        self.value = 0
        self.face = self.faces[0]
    def roll(self):
        self.value = randint(0,5)
        self.face = self.faces[self.value]
    def show(self , screen, x, y):
        screen.blit(self.face, (x, y))

class ScoreBoard:
    def __init__(self):
        self.textfont = pygame.font.SysFont("Arial",48)
        self.message=u"Κάτι Άλλο!"
    def GetScore(self, value1, value2):
        self.message=u"Κάτι άλλο!"
        if (value1==0 and value2==1) or (value1==1 and value2==0):
            self.message=u"ΑσόΔυο"
        if value1==5 and value2==5:
            self.message=u"Εξάρες"
        if value1==2 and value2==2:
            self.message=u"Τρίτσες"
        if value1==3 and value2==3:
            self.message=u"Ντόρτια"
        if value1==1 and value2==1:
            self.message=u"Δίπλες"
        if value1==4 and value2==4:
            self.message=u"Πεντάρες"
        if value1==0 and value2==0:
            self.message=u"Άσοι"       
        self.thetext = self.textfont.render(self.message, True,
                             (255,0,0),(255,255,0))
        return self.thetext

def centerSurface(w):
    return ( xwidth - w ) / 2.0

def spin():
     screen.fill(surfacecolor)
     x=centerSurface(2*dice.width+offset)
     dice.show(screen, x,20)
     x1=x+dice.width+offset
     dice2.show(screen, x1,20)
    
#
# Screen resolution / initialization
#

xwidth = 440
ywidth = 340
screen = pygame.display.set_mode((xwidth, ywidth), 0, 32)
surfacecolor= (50,80,250)

#
# Initialize sprites, Clock object and set framerate
#
dice = Zari()
dice2 = Zari()
offset = 10
myscore = ScoreBoard()
clock = pygame.time.Clock()
framerate = 5
   
#
# Main loop
#

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            keyboardinput = event.key
            if keyboardinput == K_SPACE:
                for i in range(0,5):
                    dice.roll()
                    dice2.roll()
                    spin()
                    pygame.display.update()
            if keyboardinput == K_q:
                pygame.quit()
                exit()

    spin()
    thetext=myscore.GetScore(dice.value, dice2.value)
    y = centerSurface(thetext.get_width())
    screen.blit(thetext, (y,250))
    time = clock.tick(framerate)/1000.0
    pygame.display.update()
