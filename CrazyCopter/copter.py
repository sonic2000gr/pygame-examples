# -*- coding: utf-8 -*-
#
# Crazy copter
#

import pygame
from random import randint
from pygame.locals import *
from sys import exit

def centertext(thetext):
    xsize = thetext.get_width()
    xpos = (xwidth - xsize)/2.0
    return xpos

class Explosion:
    def __init__(self):
        self.images = [ 'boom1.png', 'boom2.png']
        self.boom = []
        for image in self.images:
            self.boom.append(pygame.image.load(image))
    def Show(self, surface, x, y, index):
        surface.blit(self.boom[index], (x,y))

class ScoreBoard:
    def __init__ (self, x, y):
        self.score = 0
        self.x = x
        self.y = y
        self.textfont = pygame.font.SysFont("Arial",32)
        
    def ScoreUp(self):
        self.score = self.score + 10

    def YouWin(self, surface):
        self.message = "Game Over. You Win!"
        self.thetext = self.textfont.render(self.message, True,
                        (255,255,0),(50,80,250))
        x = centertext(self.thetext)
        surface.blit(self.thetext, (x,20))
        
    def YouLose(self, surface):
        self.message = "Game Over. You Lose!"
        self.thetext = self.textfont.render(self.message, True,
                        (255,255,0),(50,80,250))
        x = centertext(self.thetext)
        surface.blit(self.thetext, (x,20))

    def Show(self, surface):
        self.message = "Score: " + str(self.score)
        self.thetext = self.textfont.render(self.message, True,
                        (255,0,0),(0,255,0))
        surface.blit(self.thetext, (self.x,self.y))

class Building:
    def __init__ (self, x, size):
        self.x = x
        self.size = size
        self.image1 = pygame.image.load('build1.jpg')
        self.image2 = pygame.image.load('build2.jpg')
        self.width1 = self.image1.get_width()
        self.height1 = self.image1.get_height()
        self.width2 = self.image2.get_width()
        self.height2 = self.image2.get_height()
        self.height = (size-1) * self.height1 + self.height2
        self.y = ywidth - self.height - 40

    def getTop(self):
        if self.size > 1:
          self.rect = pygame.Rect(self.x, self.y,
                                self.width1, self.height1)
        else:
          self.rect = pygame.Rect(self.x, self.y,
                                self.width2, self.height2)
        return self.rect

    def Destroy(self):
        if self.size > 0:
          self.size = self.size -1
          self.height = (self.size-1) * self.height1 + self.height2
          self.y = ywidth - self.height - 40
        
    def Show(self, surface):
        if self.size > 0:
            for i in range(1 ,self.size):
                surface.blit(self.image1,
                  (self.x, self.y+ self.height1 * (i-1)))

            surface.blit(self.image2,                         
                (self.x,self.y + self.height1*(self.size-1)))

class Bomb:
    def __init__ (self, x, y, yspeed):
        self.x = x
        self.y = y
        self.yspeed = yspeed
        self.image = pygame.image.load('bomb.png')
        self.width = self.image.get_width()
        self.height = self.image.get_height()
    def Show(self, surface):
        if self.y + self.height <= ywidth - 50:
            surface.blit(self.image, (self.x, self.y))
        
    def Move(self, time):
        if self.y + self.height <= ywidth - 50:
            self.y = self.y + self.yspeed * time

    def BombDown(self):
        if self.y + self.height <= ywidth - 50:
            return False
        else:
            return True
        

                  
class Copter:
    def __init__ (self, x, y, xspeed, yspeed):
        self.x = x
        self.y = y
        self.xspeed = xspeed
        self.yspeed = yspeed
        self.withbomb = False
        self.image = pygame.image.load('copter.png')
        self.image2 = pygame.image.load('copter2.png')
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.touchgrass = False
        
    def Show(self, surface, index):
        if index == 0:
           surface.blit(self.image, (self.x, self.y))
        else:
           surface.blit(self.image2, (self.x, self.y))
           
        if self.withbomb == True:
            self.mybomb.Show(surface)

    def Goto(self, x, y):
        self.x = x
        self.y = y

    def Move(self, time):
        self.x = self.x + time * self.xspeed
        self.y = self.y + time * self.yspeed
        if self.x + self.width >= xwidth:
            self.x = 0
        if self.y + self.height >= ywidth-40:
            self.xspeed = 0
            self.yspeed = 0
            self.touchgrass = True
            
        if self.withbomb == True:
            self.mybomb.Move(time)
            if self.mybomb.BombDown() == True:
                self.withbomb = False
                
    def Fire(self):
        if self.withbomb == False:
            self.mybomb = Bomb(mycopter.x + mycopter.width/2,
                          mycopter.y+mycopter.height, 30)
            self.withbomb = True

    def getCopterRect(self):
        return pygame.Rect(self.x, self.y, self.width,
                           self.height)

    def getBombRect(self):
        return pygame.Rect(self.mybomb.x, self.mybomb.y,
                    self.mybomb.width, self.mybomb.height)
        
    def getBombX(self):
        if self.withbomb == True:
            return self.mybomb.x
        else:
            return -1

    def getBombY(self):
        if self.withbomb == True:
            return self.mybomb.y
        else:
            return -1

        
xwidth = 640
ywidth = 480
pygame.init()
screen = pygame.display.set_mode((xwidth, ywidth), 0, 32)
surfacecolor = (50,80,250)
backcolor = (0, 255, 0)


#
# Main loop
#
framerate=60
space = 0
mycopter = Copter(0,0,50,3)
myscore = ScoreBoard(0,ywidth-40)
myexplosion = Explosion()
offsetx = -30
offsety = -10
explosionindex = 0
explosioncount = 0
copterimage = 0
x = 60
mybuild = []
for i in range(0,7):
    mybuild.append(Building(x, randint(3,8)))
    x = x + 70

clock = pygame.time.Clock()
gameover = False
showexplosion = False
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == USEREVENT +1:
            if explosioncount < 8:
              if explosionindex == 0:
                  explosionindex = 1
              else:
                  explosionindex = 0
              explosioncount += 1
            else:
              showexplosion = False
              pygame.time.set_timer(USEREVENT+1,0)
              explosioncount = 0
              explosionindex =0
              
        if event.type == KEYDOWN:
            keyboardinput = event.key
            if keyboardinput == K_SPACE and gameover==False:
                mycopter.Fire()
            if keyboardinput == K_q:
                pygame.quit()
                exit()
            if keyboardinput == K_UP:
                mycopter.y = mycopter.y - 10
            if keyboardinput == K_r and gameover ==True:
                gameover = False
                copterimage = 0
                explosionindex = 0
                explosioncount = 0
                mycopter.xspeed = 50
                mycopter.yspeed = 3
                mycopter.x = 0
                mycopter.y = 0
                myscore.score = 0
                mycopter.touchgrass = False
                x = 60
                mybuild = []
                for i in range(0,7):
                    mybuild.append(Building(x, randint(3,8)))
                    x = x + 70
                
    screen.fill(surfacecolor)
    pygame.draw.rect(screen, backcolor, (0,ywidth-40, xwidth,40))    
    for build in mybuild:
      build.Show(screen)
    mycopter.Show(screen, copterimage)
    myscore.Show(screen)
    time = clock.tick(framerate)/1000.0
    mycopter.Move(time)
    if mycopter.withbomb == True:
        for build in mybuild:
            therect = build.getTop()
            c = therect.colliderect(mycopter.getBombRect())  
            if c == True:
                showexplosion = True
                bombx = mycopter.getBombX()
                bomby = mycopter.getBombY()
                pygame.time.set_timer(USEREVENT+1,125)
                mycopter.withbomb = False
                build.Destroy()
                myscore.ScoreUp()


    if showexplosion == True:
        myexplosion.Show(screen, bombx+offsetx,
                         bomby+offsety, explosionindex)
    for build in mybuild:
        therect = build.getTop()
        c = therect.colliderect(mycopter.getCopterRect())
        if c == True:
             mycopter.xspeed = 10
             mycopter.yspeed = 50
             gameover = True
             myscore.YouLose(screen)
             copterimage = 1

    if mycopter.touchgrass == True and copterimage==0:
        myscore.YouWin(screen)
        
    pygame.display.update()
