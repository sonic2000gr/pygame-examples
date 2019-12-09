import pgzrun

def draw():
    screen.fill((50,80,250))
    screen.draw.text("Hello World!", (30,50),
                     fontname = "liberation-sans-regular",
                     fontsize = 48,
                     color="red",
                     background="yellow")

WIDTH = 320
HEIGHT = 140
TITLE = "Hello Pygame"
pgzrun.go()
