#! /usr/bin/env python
# coding=utf-8
#
# The Python Adventure
# Based on an idea published in Pixel Magazine
# issue 18, January 1986
#

import pygame
from pygame.locals import *
from random import randint
from sys import exit

# Define app window width and height

screenwidth = 680
screenheight = 240

# The keys used in the game: b,n,a,d
# The dictionary provides a mapping between keys and directions

thekeys = [ K_b, K_n, K_a, K_d ]
key_dir_map = { K_b : 0, K_n : 1, K_a : 2, K_d : 3 }

# return the column position for centering a message
# by determining the messages width and averaging the
# distance using screenwidth

def centerMessage(surface):
    return (screenwidth - surface.get_width())/2

#
# Process the event queue and quit if the user
# closes windows
# returns true if user clicks close
#

def getQuit():
    for event in pygame.event.get():
      if event.type == QUIT:
        return True

#
# Populate a list with the acceptable key input
# for a specific room
#

def getPossibleKeys(moves,room):
    destinations = moves[room]
    possiblekeys = []
    index = 0
    for i in destinations:
        if i!=-1:
            possiblekeys.append(thekeys[index])
        index +=1
    return possiblekeys

#
# Populate a list with possible direction keywords
# for a specific room
#

def getExitNames(moves,room):
    directions = [ "(Β)όρεια ", "(Ν)ότια ", "(Α)νατολικά ", "(Δ)υτικά " ]
    destinations = moves[room]
    index = 0
    exitnames = []
    for i in destinations:
        if i != -1:
            exitnames.append(directions[index])
        index += 1
    return exitnames

# Main program

def main():
    # Initialize the pygame library

    pygame.init()
    pygame.key.set_repeat()

    # Initialize screen and colorlist for the bars

    surfacecolor = (50,80,250)
    screen = pygame.display.set_mode((screenwidth, screenheight), 0, 32)
    pygame.display.set_caption("The Adventure")
    colorlist = [ (253,53,8), (23,233,9), (0,0,0), (202,228,7), (1,191,0),
                  (204,34,254), (255,255,255), (75,0,244), (0,239,0),
                  (242,17,251), (249,50,0), (188,185,192), (108,40,251),
                  (253,80,0), (185,215,0), (253,47,3) ]

    # Setup some fonts and text messages

    headerfont = pygame.font.SysFont("Tahoma",48)
    textfont = pygame.font.SysFont("Tahoma",22)
    header_text = headerfont.render("The Adventure!", True, (255,0,0),(255,255,0))
    win_text = textfont.render(u"Κέρδισες! Η περιπέτεια τελείωσε.", False, (255,255,0))
    lose_text = textfont.render(u"Έχασες! Η περιπέτεια τελείωσε.", False, (255,255,0))

    # Initialize the room descriptions list

    rooms = [ "Βρίσκεσαι στον κήπο. Παντού σκοτάδι.",
              "Βρίσκεσαι στο μπάνιο. Ακούς θόρυβο.",
              "Βρίσκεσαι στο χωλ. Παραλίγο να σκοντάψεις.",
              "Βρισκεσαι στην αποθήκη. Η ατμόσφαιρα είναι αποπνικτική.",
              "Έφτασες στο καθιστικό. Βρήκες τον πατέρα σου.",
              "Βρίσκεσαι στο σαλόνι. Ακούγεται μουσική.",
              "Βρίσκεσαι στην τραπεζαρία. Τα πάντα είναι ανάστατα.",
              "Βρίσκεσαι στο διάδρομο. Είναι σκοτεινά. Σκάλα Νότια",
              "Είσαι στη κουζίνα. Ακούς φωνές.",
              "Είσαι στον πάνω διάδρομο. Παντού ησυχία. Σκάλα Βόρεια.",
              "Είσαι στο δωμάτιο του αδερφού σου. Ο αδερφός σου σε μαρτυρά!",
              "Είσαι στο δωμάτιο των γονέων σου. Η μητέρα σου σε έπιασε.",
              "Είσαι στο δωμάτιο σου. Είσαι ασφαλής." ]

    #
    # The following list contains lists :)
    # The list's index denotes the current room.
    # Each single-list contains four numbers:
    # First number -> Destination room if North
    # Second number -> Destination room if South
    # Third number -> Destination room if East
    # Fourth number -> Destination room if West
    #
    # Destination is set to -1 if it does not exist
    #

    moves = [   [-1,2,-1,-1],
                [-1,-1,2,-1],
                [0,5,3,1],
                [-1,8,-1,2],
                [-1,6,5,-1],
                [2,8,-1,4],
                [4,7,-1,-1],
                [6,9,8,-1],
                [5,-1,-1,7],
                [7,11,12,10],
                [-1,-1,9,-1],
                [9,-1,-1,-1],
                [-1,-1,-1,9] ]

    # When player reaches any of the following room(s),
    # he wins the game

    winrooms = [ 12 ]

    # When player reaches any of the following rooms,
    # he loses

    lossrooms = [ 4, 10, 11 ]

    # Startup room
    # Doesn't have to be 0, but must not be a winning
    # or losing room

    room = 0

    # Initialize text/header positions

    headerx = centerMessage(header_text)
    headery = 20
    texty = 160
    message_y = 185
    box_x = 0
    box_y = 90
    box_width = screenwidth / 16.0
    box_height = box_width * 1.33

    # Initialize clock object and set framerate

    clock = pygame.time.Clock()
    framerate = 25

    # Begin main loop

    endgame = False

    while not endgame:

        # fill screen with bluish tin

        screen.fill(surfacecolor)

        # Show header message

        screen.blit(header_text,(headerx,headery))

        # Show room descritpion text

        description = textfont.render(rooms[room].decode('utf-8'), False, (255,255,255))
        textx = centerMessage(description)
        screen.blit(description,(textx, texty))

        # Draw TI-99 like color bars

        box_x = 0
        for color in colorlist:
            box_pos = (box_x, box_y, box_width, box_height)
            pygame.draw.rect(screen, color, box_pos)
            box_x += box_width

        # Check if user won or lost or play in progress

        if room in lossrooms:
            message_x = centerMessage(lose_text)
            screen.blit(lose_text,(message_x, message_y))

            # Process quit message here

            endgame = getQuit()

        elif room in winrooms:
            message_x = centerMessage(win_text)
            screen.blit(win_text,(message_x, message_y))

            # Process quit message here too

            endgame = getQuit()
        else:

            # print possible exits

            exits_text = ("".join(getExitNames(moves,room))).decode('utf-8')
            question = textfont.render(u"Έξοδοι: "+exits_text, False, (255,255,255))
            message_x = centerMessage(question)
            screen.blit(question,(message_x,message_y))

            # get a list of acceptable keys, depending on room

            allowed_keys = getPossibleKeys(moves,room)
            direction = -1

            # Process keyboard events (QUIT too)

            for event in pygame.event.get():
              if event.type == KEYDOWN:
                  keyboardinput = event.key
                  if keyboardinput in allowed_keys:
                    direction = key_dir_map[keyboardinput]
              if event.type == QUIT:
                  endgame = True

            # Get the move done

            if direction != -1:
                move = moves[room]
                room = move[direction]

        # Obey framerate and update display

        time = clock.tick(framerate)
        pygame.display.update()

    # endgame

    pygame.quit()
    exit()

# Start program
if __name__ == "__main__":
    main()
