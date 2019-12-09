import pgzrun

class Colorbars(object):
    def __init__(self):
        self.colorlist = [(253,53,8), (23,233,9), (0,0,0), (202,228,7), (1,191,0),
                          (204,34,254), (255,255,255), (75,0,244), (0,239,0),
                          (242,17,251), (249,50,0), (188,185,192), (108,40,251),
                          (253,80,0), (185,215,0), (253,47,3)]
        self.box_width = int(WIDTH/16.0)
        self.box_height = int(self.box_width * 1.33)
        self.box_x = 0
        self.box_y = 100

class Game(object):
    def __init__(self):
        self.rooms = [ "Βρίσκεσαι στον κήπο. Παντού σκοτάδι.",
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

        self.moves = [   [-1,2,-1,-1],
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

        self.winrooms = [ 12 ]

        # When player reaches any of the following rooms,
        # he loses

        self.lossrooms = [ 4, 10, 11 ]

        # Startup room
        # Doesn't have to be 0, but must not be a winning
        # or losing room

        self.room = 0
        self.thekeys = [ keys.B, keys.N, keys.A, keys.D ]
        self.key_dir_map = { keys.B : 0, keys.N : 1, keys.A : 2, keys.D : 3 }
        
    def hasWon(self):
        return (self.room in self.winrooms)
    
    def hasLost(self):
        return (self.room in self.lossrooms)
    
    def getDescription(self):
        return self.rooms[self.room]
    
    def getPossibleKeys(self):
        destinations = self.moves[self.room]
        possiblekeys = []
        index = 0
        for i in destinations:
            if i!=-1:
                possiblekeys.append(self.thekeys[index])
            index +=1
        return possiblekeys
    
    def move(self, thekey):
        index = self.key_dir_map[thekey]
        move = self.moves[self.room]
        self.room = move[index]
    
    def getExitNames(self):
        directions = [ "(Β)όρεια ", "(Ν)ότια ", "(Α)νατολικά ", "(Δ)υτικά " ]
        destinations = self.moves[self.room]
        index = 0
        s=''
        exitnames = []
        for i in destinations:
            if i != -1:
                exitnames.append(directions[index])
            index += 1
        return s.join(exitnames)


def draw():
    screen.fill((0x42, 0xeb, 0xf5))
    screen.draw.text("The Adventure!", (120,20),
                     color="red",
                     background="yellow",
                     fontname="liberation-sans-regular",
                     fontsize=64)
    bars.box_x = 0
    for color in bars.colorlist:
        box_pos = Rect((bars.box_x, bars.box_y), (bars.box_width, bars.box_height))
        screen.draw.filled_rect(box_pos, color)
        bars.box_x += bars.box_width
    if thegame.hasWon():
        screen.draw.text("Κέρδισες! Η περιπέτεια τελείωσε.", (30,170),
                         fontsize = 20,
                         color = "blue",
                         fontname = "liberation-sans-regular")
    elif thegame.hasLost():
        screen.draw.text("Έχασες! Η περιπέτεια τελείωσε.", (30,170),
                         fontsize = 20,
                         color = "blue",
                         fontname = "liberation-sans-regular")
    else:
        screen.draw.text("Έξοδοι: "+thegame.getExitNames(), (30, 170),
                                  fontsize = 20,
                                  color = "blue",
                                  fontname = "liberation-sans-regular")
        
    screen.draw.text(thegame.getDescription(), (30, 200), fontname = "liberation-sans-regular",
                                                          color = "blue",
                                                          fontsize = 20)
    

def update():
    global nodelay
    if not(thegame.hasLost() or thegame.hasWon()):
        possiblekeys = thegame.getPossibleKeys()
        if nodelay:
            for thekey in possiblekeys:
                if keyboard[thekey]:
                    thegame.move(thekey)
                    nodelay = False
                    clock.schedule_unique(updateDelay, 0.5)

def updateDelay():
    global nodelay
    nodelay = True

WIDTH = 680
HEIGHT = 240
nodelay = True
bars = Colorbars()
thegame = Game()
pgzrun.go()
