import pgzrun

def draw():
    screen.fill((50,80,250))
    theball.draw()


def update(dt):
    global x, y, xspeed, yspeed
    x = x + xspeed * dt
    y = y + yspeed * dt
    if x > WIDTH - theball.width:
        x = WIDTH - theball.width
        xspeed = -xspeed
    if x < 0:
        x = 0
        xspeed = -xspeed
    if y > HEIGHT - theball.height:
        y = HEIGHT - theball.height
        yspeed = -yspeed
    if y < 0:
        y = 0
        yspeed = -yspeed
    theball.pos = x, y

WIDTH = 640
HEIGHT = 480
TITLE = "Bouncing Ball"
x, y = 100.0, 100.0
xspeed, yspeed = 100.0, 100.0
theball = Actor("soccer-ball", anchor=('left', 'top'))
theball.pos = x, y
pgzrun.go()
