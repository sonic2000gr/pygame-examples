from random import randint
import pgzrun

def draw():
    pass

def update():
    ypos=0
    for ypos in range(0,479,30):
      for xpos in range(0,659,30):
        the_pos=Rect((xpos,ypos),(29,29))
        random_color = (randint(0,255), randint(0,255), randint(0,255))
        screen.draw.filled_rect(the_pos, random_color)

WIDTH = 660
HEIGHT = 480
pgzrun.go()
