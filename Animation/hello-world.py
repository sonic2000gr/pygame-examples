#
# pygame hello world
#
# ���, ��� ����� ���� ��������� ��� ��������.
# ��� ������ ��� �� ��������!
#
import pygame
from pygame.locals import *
from sys import exit

# Define app window width and height

swidth,sheight = 320,140

def centerMessage(surface):
    return (swidth - surface.get_width())/2

#
# Process the event queue 
# returns true if user clicks close
#

def getQuit():
    for event in pygame.event.get():
      if event.type == QUIT:
        return True


def main():
    # Initialize the pygame library

    pygame.init()
    surfacecolor = (50,80,250)
    screen = pygame.display.set_mode((swidth, sheight), DOUBLEBUF, 32)
    pygame.display.set_caption("Hello Pygame!")
    textfont = pygame.font.SysFont("Arial",48)
    thetext = textfont.render("Hello World!", True, (255,0,0),(255,255,0))
    
    # Initialize text position

    textx = centerMessage(thetext)
    texty = 40

   # Begin main loop

    endprogram = False

    while not endprogram:

        # fill screen with bluish tint

        screen.fill(surfacecolor)

        # Show text message

        screen.blit(thetext,(textx,texty))     
        endprogram = getQuit()
        pygame.display.update()

    # shutdown pygame and exit program
    
    pygame.quit()
    exit()

# Start program
if __name__ == "__main__":
    main()
