#
# Bouncing ball - OOP :)
#

import pgzrun
from random import randint

class Ball(Actor):
  def __init__(self, theImage, x, y, xspeed, yspeed):
    super().__init__(theImage, anchor=('left', 'top'))
    self.x = x
    self.y = y
    self.xspeed = xspeed
    self.yspeed = yspeed
    self.pos = self.x, self.y
    
  def Move(self, time):
    distance_x = time * self.xspeed
    distance_y = time * self.yspeed
    self.x = self.x + distance_x
    self.y = self.y + distance_y
    if self.x < 0:
        self.x = 0
        self.xspeed = -self.xspeed
    if self.x > WIDTH - self.width:
        self.x = WIDTH - self.width
        self.xspeed = -self.xspeed
    if self.y < 0:
        self.y = 0
        self.yspeed = -self.yspeed
    if self.y > HEIGHT - self.height:
        self.y = HEIGHT - self.height
        self.yspeed = -self.yspeed
    self.pos = self.x, self.y
    
balls=[]
for i in range(0,8):
  x = randint(80,500)
  y = randint(80,400)
  xspeed = 0
  while xspeed >= -5 and xspeed <= 5:
    xspeed = randint(-50,50)
  yspeed = 0
  while yspeed >= -5 and yspeed <=5:
    yspeed = randint(-50,50)
  balls.append(Ball('soccer-ball', x, y, xspeed, yspeed))

def draw():
    screen.fill((50,80,250))
    for theball in balls:
        theball.draw()

def update(dt):
    for theball in balls:
        theball.Move(dt)

WIDTH = 640
HEIGHT = 480
TITLE = "Bouncing Ball OOP"
pgzrun.go()
