# -*- coding: utf-8 -*-
# Podosfairaki

import pygame
from random import randint
from pygame.locals import *
from math import sin, cos, pi
from sys import exit

def PrepareSound(filename):
    sound = pygame.mixer.Sound(filename)
    return sound

class ScoreBoard:
  def __init__(self,sw,y, onleft):
    self.y = y
    self.font = pygame.font.SysFont("Impact",48)
    self.score = 0
    self.onLeft = onleft
    self.sw = sw

  def Goal(self):
    self.score += 1

  def Show(self,surface):
    scoretext = self.font.render(str(self.score), True, (255,255,0))
    
    if self.onLeft:
        self.x = 100
    else:
        self.x = self.sw - scoretext.get_width()-100
        
    surface.blit(scoretext,(self.x, self.y))

  def GetScore(self):
    return self.score

  def SetScore(self, score):
    self.score = score

  def ResetScore(self):
    self.score = 0

class Timer:
    def __init__ (self, minutes, seconds, x, y):
        self.minutes = minutes
        self.seconds = seconds
        self.initminutes = minutes
        self.initseconds = seconds
        self.timerevent = 6
        self.font = pygame.font.SysFont("impact",48)
        self.x = x
        self.y = y

    def Show(self, screen):
        if self.minutes < 10:
            strminutes = '0'+str(self.minutes)
        else:
            strminutes = str(self.minutes)

        if self.seconds < 10:
            strseconds = '0'+str(self.seconds)
        else:
            strseconds = str(self.seconds)

        thetext = self.font.render(strminutes+":"+strseconds, True,(255,255,255))
        screen.blit(thetext, (self.x,self.y))
        
    def start(self):
        pygame.time.set_timer(USEREVENT+self.timerevent, 1000)

    def stop(self):
        pygame.time.set_timer(USEREVENT+self.timerevent, 0)

    def reset(self):
        self.minutes = self.initminutes
        self.seconds = self.initseconds

    def tick(self):
        self.seconds -= 1
        if self.seconds == -1:
            self.minutes -=1
            if self.minutes == -1:
                self.minutes = 0
                self.seconds = 0
                self.stop()
                return True
            else:
                self.seconds = 59
                return False
        return False
    

class GoalPost:
    def __init__(self, filenames,sw,sh, gipedo):
        self.filenames = filenames
        self.images = []
        for filename in self.filenames:
            self.images.append(pygame.image.load(filename))
        self.h1 = self.images[0].get_height()
        self.w1 = self.images[0].get_width()
        g1 = gipedo.getHeight()
        self.leftx = 0
        self.rightx = sw - self.w1
        self.y = sh - g1 - self.h1+1
        self.collision_rect_left = pygame.Rect((self.leftx+self.w1-15, self.y+32),
                                               (15, self.h1-32))
        self.collision_rect_right = pygame.Rect((self.rightx, self.y+32),
                                                (15, self.h1-32))
        self.dokari_rect_left = pygame.Rect((self.leftx+self.w1-15,self.y),
                                            (15, 32))
        self.dokari_rect_right = pygame.Rect((self.rightx, self.y),
                                             (15,32))
        
    def Show(self, screen):
        screen.blit(self.images[0], (self.leftx, self.y))
        screen.blit(self.images[1], (self.rightx, self.y))

    def getGoal(self, ball):
        if ball.rect.colliderect(self.collision_rect_left) and ball.xspeed<0:
            return "Left"
        elif ball.rect.colliderect(self.collision_rect_right) and ball.xspeed>0:
            return "Right"
        else:
            return "None"

    def getDokari(self,ball):
        if ball.rect.colliderect(self.dokari_rect_left) and ball.xspeed<0:
            ball.xspeed = -0.80 * ball.xspeed
        if ball.rect.colliderect(self.dokari_rect_right) and ball.xspeed>0:
            ball.xspeed = -0.80 * ball.xspeed
    

class Planet:
    def __init__(self, filename, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load(filename)
    
    def Show(self, screen):
        screen.blit(self.image, (self.x, self.y))
        
class Background:
    def __init__(self, filename, s_height):
        self.filename = filename
        self.image = pygame.image.load(filename)
        self.x = 0
        self.y = s_height - self.image.get_height()
        
    def Show(self, screen):
        screen.blit(self.image,(self.x, self.y))

    def getHeight(self):
        return self.image.get_height()

    def getWidth(self):
        return self.image.get_width()
    
class Ball:
    def __init__ (self, filenames, players, gipedo,x, sw=1000,
                  sh=400):
        self.angle = pi/4
        
        # Screen width and height
        self.bouncewave = PrepareSound("bounce.wav")
        self.sw = sw
        self.sh = sh
        self.filenames = filenames
        self.imageindex = 0
        self.xspeed = 0
        self.yspeed = 0
        self.bounce = False
        self.kickedby = None
        self.kicktime = 0
        self.images =[]
        for filename in self.filenames:
            self.images.append(pygame.image.load(filename))
        self.countimages = len(self.images)
        
        # Initial x position
        
        self.x = x

        # Initial y position calculated on the ground

        self.y = self.sh - gipedo.getHeight() - self.images[0].get_height()

        # Remember initial positions

        self.init_x = self.x
        self.init_y = self.y
        self.width = self.images[0].get_width()
        self.height = self.images[0].get_height()
        self.rect = pygame.Rect((self.x, self.y),
                         (self.width, self.height))

    def ResetPosition(self):
        self.x = self.init_x
        self.y = self.init_y
        self.rect = pygame.Rect((self.x, self.y),
                                (self.width, self.height))

    def Drop(self):
        self.y = 100
        self.xspeed = 0
        self.yspeed = 200

    def Show(self, screen):
        screen.blit(self.images[self.imageindex],
                    (self.x, self.y))    

    def Move(self, time):       
        if self.kickedby:
            if self.kickedby == players[0]:
                otherplayer = players[1]
            else:
                otherplayer = players[0]
            if self.rect.colliderect(otherplayer.rect) and not otherplayer.avoidcollision:
                self.xspeed = -self.xspeed * 0.25
                otherplayer.avoidcollision = True
                pygame.time.set_timer(USEREVENT + otherplayer.kickeventno, 150)
            if self.rect.colliderect(self.kickedby.rect) and not self.kickedby.avoidcollision:
                self.xspeed = -self.xspeed * 0.25
                self.kickedby.avoidcollision = True
                pygame.time.set_timer(USEREVENT + self.kickedby.kickeventno, 150)
            self.yspeed = self.yspeed * sin(self.angle) + 0.1 * self.kicktime
            if self.xspeed > 0:
                self.xspeed -= self.xspeed * 0.1 * time
            else:
                self.xspeed += self.xspeed * 0.1 * time
            if abs(self.xspeed) <=1:
                self.xspeed = 0
       
        if self.y > self.init_y and self.bounce==False:
           self.y = self.init_y
           self.kickedby = None
           self.bouncetime = 1
           self.yspeed = -0.45 * self.yspeed
           self.bounce = True
           pygame.time.set_timer(USEREVENT+2,10)
           
        self.x = self.x + self.xspeed* time        
        self.y = self.y + self.yspeed* time
        if self.x < 0:
            self.x = 0
            self.xspeed = -0.25*self.xspeed
        if self.x + self.width > self.sw:
            self.x = self.sw - self.width
            self.xspeed = -0.25*self.xspeed
        self.rect = pygame.Rect((self.x, self.y),
                         (self.width, self.height))

    def Bounce(self):
        if self.bounce:
            self.yspeed = self.yspeed + 0.1 * self.bouncetime
            self.bouncetime += 1
            if self.y > self.init_y:
                self.y = self.init_y
                self.yspeed = -self.yspeed * 0.35
                pygame.time.set_timer(USEREVENT+2, 10)
                self.bouncetime = 1
                if abs(self.yspeed)<=50:
                    self.bouncetime = 1
                    self.y = self.init_y
                    self.bounce = False
                    self.yspeed = 0
                    self.kickedby = None
                    pygame.time.set_timer(USEREVENT+2, 0)
            
    def kick(self,player):
        if self.kickedby == None:
            self.xspeed = 4*player.xspeed
            if abs(player.xspeed)>=200:
                self.angle=pi/2.8
            else:
                self.angle=pi/3.5
            self.yspeed = -700-abs(player.xspeed)
            self.kickedby = player
            self.kicktime = 0        
            pygame.time.set_timer(USEREVENT+3,10)
            pygame.time.set_timer(USEREVENT+player.kickeventno, 150)
            player.avoidcollision = True

    def roll(self,xspeed):
        self.xspeed = xspeed        

    def IsMoving(self):
        if self.xspeed!=0 or self.yspeed!=0:
            return True
        else:
            return False
        
    def Rotate(self):
        if self.IsMoving():
            self.imageindex += 1
            if self.imageindex == 3:
                self.imageindex = 0

    def isKickable(self, player):
        if player.faceright==True:
            bx1=player.rect.bottomright[0]
            bx2=self.rect.bottomleft[0]
        else:
            bx1=player.rect.bottomleft[0]
            bx2=self.rect.bottomright[0]
              
        if abs( bx1 - bx2) <=5 or player.hasball:
            
            return True        
        else:
            return False
         
class Player:
    def __init__(self, filenames, gipedo, eventno, kickeventno, x=100,imageindex=0, 
                 sw=1000, sh=400):
        self.xspeed = 0
        self.yspeed = 0
        self.dirchange = False
        self.x = x
        self.sw = sw
        self.sh = sh
        self.hasball = False
        self.imageindex = imageindex
        self.bouncetime = 1
        if self.imageindex == 0 or self.imageindex==2:
            self.faceright=True
            self.faceleft = False
        else:
            self.faceright= False
            self.faceleft = True
        self.eventno = eventno
        self.kickeventno = kickeventno
        self.avoidcollision = False
        self.jumping = False
        self.filenames = filenames

        self.images =[]

        for filename in self.filenames:
            self.images.append(pygame.image.load(filename))

        self.h1 = self.images[0].get_height()
        self.w1 = self.images[0].get_width()
        g1 = gipedo.getHeight()
        self.y = self.sh - g1 - self.h1
        self.init_y = self.y
        self.init_x = self.x
        self.rect = pygame.Rect((self.x, self.y),
                                (self.w1, self.h1))
    
    def ResetPosition(self):
        self.x = self.init_x
        self.y = self.init_y
        self.rect = pygame.Rect((self.x, self.y),
                                (self.w1, self.h1))
        
    def Show(self, screen):
        screen.blit(self.images[self.imageindex],
                    (self.x, self.y))

    def toggleFace(self):
        if self.faceright:
            self.faceright=False
        else:
            self.faceright = True
        
    def Move(self, xspeed, yspeed, time, anim):
        self.x = self.x + xspeed* time
        self.y = self.y + self.yspeed* time
        self.rect = pygame.Rect((self.x, self.y),
                                (self.w1, self.h1))
        if self.xspeed==0 and self.imageindex== 2 and xspeed<0 :
            self.dirchange = True
            
        if  self.xspeed==0 and self.imageindex==3 and xspeed>0:
            self.dirchange = True
            
        if xspeed > 0 and not self.faceright:
            self.dirchange = True
            self.toggleFace()
            
        elif xspeed<0 and self.faceright:
            self.dirchange= True
            self.toggleFace()
            
        elif self.xspeed != 0:
            self.dirchange = False

        self.xspeed = xspeed
        
        if anim == True:
            if xspeed > 0:
                if self.imageindex == 0:
                    self.imageindex = 2
                else:
                    self.imageindex = 0
            elif xspeed < 0:
                if self.imageindex == 1:
                    self.imageindex = 3
                else:
                    self.imageindex = 1
            else:
                if self.imageindex == 0:
                    self.imageindex = 2
                if self.imageindex == 1:
                    self.imageindex = 3
        if self.x < 0:
            self.x = 0
        if self.x + self.w1 > self.sw:
            self.x = self.sw - self.w1

    def jump(self, yspeed):
        if self.faceright:
            self.imageindex = 4
        else:
            self.imageindex = 5
        self.yspeed = yspeed
        self.jumping = True
        pygame.time.set_timer(USEREVENT+self.eventno,10)

    def inJump(self):
        self.yspeed = self.yspeed + 0.1 * self.bouncetime
        self.bouncetime += 1
        if self.y > self.init_y:
            self.y = self.init_y
            pygame.time.set_timer(USEREVENT+self.eventno, 0)
            self.bouncetime = 1
            self.imageindex = 0
            self.yspeed = 0
            self.jumping = False
            if self.faceright:
                self.imageindex = 2
            else:
                self.imageindex = 3
            
        
    def getPosition(self):
        return (self.x, self.y)

def CenterMessage(screen, surface):
  return (screen.get_width() - surface.get_width())/2

def GameOverShow(screen):
  font = pygame.font.SysFont("impact", 32)
  gameovertext = font.render("Game Over!",True,(255,255,255))
  text_x = CenterMessage(screen, gameovertext)
  screen.blit (gameovertext,(text_x,200))
  gameovertext = font.render("Press R to Restart", True, (255,255,255))
  text_x = CenterMessage(screen, gameovertext)
  screen.blit(gameovertext,(text_x,240))

def GoalShow(screen):
  font = pygame.font.SysFont("impact", 64)
  goaltext = font.render("GOAL!",True,(255,255,255))
  text_x = CenterMessage(screen, goaltext)
  screen.blit (goaltext,(text_x,140))

def ResetGame():
    endgame = False
    theplayer.ResetPosition()
    theplayer2.ResetPosition()
    thetimer.reset()
    thetimer.start()
    theball.ResetPosition()
    leftScore.ResetScore()
    rightScore.ResetScore()
    theball.Drop()
    anim = False

def ResetAfterGoal():
    theplayer.ResetPosition()
    theplayer2.ResetPosition()
    theball.ResetPosition()
    theball.Drop()
    anim = False

pygame.init()

# Screen Width and Height

w=1000
h=400

# Initial Ball position

ball_x = 500

# Background color

scolor = (50,150,255)
screen = pygame.display.set_mode((w,h),DOUBLEBUF)

#pygame.key.set_repeat(1, 1)

pygame.display.set_caption("Space Football!!")

endprogram = False

# Create and automatically position background image

gipedo = Background('gipedo2d.png',h)

# Create and automatically position goalposts

goalposts = GoalPost(['terma-left.png', 'terma-right.png'],w,h, gipedo)

# Create and automatically position players

theplayer = Player(['newplayer1.png','newplayer1r.png',
                    'newplayer11.png','newplayer11r.png',
                    'playerjump1r.png','playerjump1l.png'],
                    gipedo,4,7, 200,2)
theplayer2 = Player(['newplayer2.png','newplayer2r.png',
                     'newplayer21.png','newplayer21r.png',
                     'playerjump2r.png','playerjump2l.png'],
                    gipedo,5,0, 745,3)
theplanet = Planet("planet.png",  500,0)
# Create a players list to repeatedly execute player commands
# in main loop

players = [theplayer, theplayer2]

# Create the ball object

theball = Ball(['ball3.png', 'ball1.png', 'ball2.png'],players, gipedo, ball_x)

framerate = 50
xspeed=0
yspeed=0
xspeed2=0
yspeed2=0
gameminutes = 3
gameseconds = 0
accfact = 3
clock = pygame.time.Clock()
kickwave = PrepareSound("kick.wav")
goalwave = PrepareSound("goal.wav")
leftScore = ScoreBoard(w,10, True)
rightScore = ScoreBoard(w,10, False)
pygame.time.set_timer(USEREVENT+1, 100)
pygame.time.set_timer(USEREVENT+3, 10)
thetimer = Timer(gameminutes,gameseconds,450,10)
thetimer.start()
theball.Drop()
goalframecounter = 0
inGoal = False
anim = False
endgame = False
while not endprogram:    
    screen.fill(scolor)
    gipedo.Show(screen)
    theplanet.Show(screen)
    theplayer.Show(screen)
    theplayer2.Show(screen)
    theball.Show(screen)
    goalposts.Show(screen)
    thetimer.Show(screen)
    leftScore.Show(screen)
    rightScore.Show(screen)
    goal = goalposts.getGoal(theball)
    if goal == "Left" and not inGoal:
        goalwave.play()
        rightScore.Goal()
        inGoal = True
    if goal == "Right" and not inGoal:
        goalwave.play()
        leftScore.Goal()
        inGoal = True
    if inGoal:
        GoalShow(screen)
        goalframecounter +=1
        if goalframecounter == 100:
            goalframecounter = 0
            inGoal = False
            ResetAfterGoal()
        
    goalposts.getDokari(theball)
    time = clock.tick(framerate)/1000.0
    theball.Move(time)
    for player in players:
        if player.hasball and player.dirchange :
            if player.faceright:
                theball.x = player.rect.bottomright[0] -10
            else:
                theball.x = player.rect.bottomleft[0] +10 - theball.width
        if theball.rect.colliderect(player.rect) and not theball.kickedby:
            player.hasball = True
            theball.roll(player.xspeed)
        else:
            player.hasball=False
        
    #if theplayer.hasball == False and theplayer2.hasball==False and theball.kickedby== None and theball.bounce==False:
    #    theball.xspeed = 0
        
    for event in pygame.event.get():
        if event.type == QUIT:
            endprogram = True
        if event.type == USEREVENT+1:
            anim = True
            theball.Rotate()
        if event.type == USEREVENT+2:
            theball.Bounce()
        if event.type == USEREVENT+3:
            theball.kicktime += 1
        if event.type == USEREVENT+4:
            if theplayer.jumping:
                theplayer.inJump()
        if event.type == USEREVENT+5:
            if theplayer2.jumping:
                theplayer2.inJump()
        if event.type == USEREVENT+6:
            endgame = thetimer.tick()
        if event.type == USEREVENT+7:
            theplayer.avoidcollision = False
            pygame.time.set_timer(USEREVENT+7, 0)
        if event.type == USEREVENT+0:
            theplayer2.avoidcollision = False
            pygame.time.set_timer(USEREVENT+0,0)
        if not endgame:
            if event.type==KEYDOWN:
                if event.key==K_RIGHT and not inGoal:
                    xspeed = 70
                if event.key==K_LEFT:
                    xspeed = -70
                if event.key==K_UP:
                    if not theplayer2.jumping:
                        yspeed = -300
                        theplayer2.jump(yspeed)
                if event.key==K_a:
                    xspeed2 = -70
                if event.key==K_d:
                    xspeed2 = 70
                if event.key==K_w:
                    if not theplayer.jumping:
                        yspeed2 = -300
                        theplayer.jump(yspeed2)
                
            key = pygame.key.get_pressed()
            if key[K_LCTRL]:
                endprogram = True
            if key[K_SPACE]:
                if theball.isKickable(theplayer):
                    kickwave.play()
                    theball.kick(theplayer)
                    theplayer.hasball = False 
            if key[K_RCTRL]:
                if theball.isKickable(theplayer2):
                    kickwave.play()
                    theball.kick(theplayer2)
                    theplayer2.hasball = False        
            if key[K_RIGHT]:
                xspeed = xspeed + accfact
            elif key[K_LEFT]:
                xspeed = xspeed - accfact
            else:
                xspeed = 0
            if key[K_a]:
                xspeed2 = xspeed2 - accfact
            elif key[K_d]:
                xspeed2 = xspeed2 + accfact
            else:
                xspeed2 = 0
        else:
            xspeed = 0
            xspeed2 = 0
            GameOverShow(screen)
            key = pygame.key.get_pressed()
            if key[K_r]:
                inGoal = False
                ResetGame()
                
                
                        
            
    theplayer2.Move(xspeed, yspeed, time,anim)
    theplayer.Move(xspeed2, yspeed2, time,anim)
    if xspeed2 == 0 and theplayer.hasball == True:
        theball.xspeed = 0
    if xspeed == 0 and theplayer2.hasball == True:
        theball.xspeed = 0
    if anim == True:
        anim = False
    pygame.display.update()

pygame.quit()
exit()
