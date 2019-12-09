import pgzrun

def draw():
    screen.fill((50,80,250))
    theball.draw()
    theball2.draw()


def update(dt):
    global x, y, xspeed, yspeed
    global x2, y2, xspeed2, yspeed2
    x = x + xspeed * dt
    y = y + yspeed * dt
    x2 = x2 + xspeed2 * dt
    y2 = y2 + yspeed2 * dt
    if x < 0:
        x = 0
        xspeed = -xspeed
    if x > WIDTH - theball.width:
        x = WIDTH - theball.width
        xspeed = -xspeed
    if y < 0:
        y = 0
        yspeed = -yspeed
    if y > HEIGHT - theball.height:
        y = HEIGHT - theball.height
        yspeed = -yspeed
    if x2 < 0:
        x2 = 0
        xspeed2 = -xspeed2
    if x2 > WIDTH - theball2.width:
        x2 = WIDTH - theball2.width
        xspeed2 = -xspeed2
    if y2 < 0:
        y2 = 0
        yspeed2 = -yspeed2
    if y2 > HEIGHT - theball2.height:
        y2 = HEIGHT - theball2.height
        yspeed2 = -yspeed2
    theball.pos = x, y
    theball2.pos = x2, y2

WIDTH = 640
HEIGHT = 480
TITLE = "Bouncing Ball"
x, y = 100.0, 100.0
x2, y2 = 50.0, 50.0
xspeed, yspeed = 150.0, 120.0
xspeed2, yspeed2 = -120.0, 150.0
theball = Actor("soccer-ball", anchor=('left', 'top'))
theball2 = Actor("soccer-ball", anchor=('left', 'top'))
theball.pos = x, y
theball2.pos = x2, y2
pgzrun.go()
