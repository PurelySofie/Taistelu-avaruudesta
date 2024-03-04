import time
import sys
from constants import *
from playership import PlayerShip
from player import Player
from laser import Laser
from enemies import Enemies
import pgzrun

WIDTH=800
HEIGHT=600
TITLE="Avaruus taistelu"
ICON="rock_big_icon.png"

scroll_speed = 2

player = Player()

spacecraft = PlayerShip("goodship", (400,480))

# Pelaajan aluksen nopeus
spacecraft.set_speed(4)

# Vihollisten luonti eri tasoille
enemies1 = Enemies((WIDTH,HEIGHT), "level1.dat")
enemies2 = Enemies((WIDTH,HEIGHT), "level2.dat")


# Pelaajan laserin ampumiseen liittyvät asiat
lasers = []
laser_last_fired = 0
time_between_lasers = 0.3

scroll_position = 0

# Paikat missä pelaajan avaruusalukseen voi osua
spacecraft_hit_pos = [
    (0,-40), (10,-30), (-10,-30), (13,-15), (-13,-15), (25,-3), (-25,-3),
    (46,12), (-46,12), (25,24), (-25,24), (10,27), (-10,27), (0,27) ]

# Pelin tila (start, game tai gameover)
status = "start"

# Odotusaika pelin aloitukselle
wait_timer = 0

def draw ():
    # Taustan liikkuminen
    screen.blit("background", (0,scroll_position-600))
    screen.blit("background", (0,scroll_position))

    if status == "game1":
        enemies1.draw(screen)
    if status == "game2":
        enemies2.draw(screen)


    spacecraft.draw()


    for this_laser in lasers:
        this_laser.draw()

    screen.draw.text("Score: {}".format(player.score), fontname="supersedan", fontsize=40, topleft=(30,30), color=(255,255,255))
    screen.draw.text("Lives: {}".format(player.lives), fontname="supersedan", fontsize=40, topright=(770,30), color=(255,255,255))

    if status == "start" or status == "start-wait":
        screen.draw.text("Press a number key to select a level", fontname="vtks escape", fontsize=30, center=(400,300), color=(255,255,255))
    elif status == "gameover" or status == "gameover-wait":
        screen.draw.text("Game Over", fontname="vtks escape", fontsize=40, center=(400,200), color=(255,255,255))


def update(time_interval):

    global status, scroll_position, laser_last_fired, wait_timer

    # Painamalla ESC peli sulkeutuu
    if keyboard.escape:
        sys.exit()
    
    if status == "start":
        wait_timer = time.time() + DELAY_TIME
        status = "start-wait"
    if status == "start-wait":
        if (time.time() < wait_timer):
            return
        if keyboard.k_1:
            player.reset()
            enemies1.reset()
            status = "game1"
        elif keyboard.k_2:
            player.reset()
            enemies2.reset()
            status = "game2"
        
    elif status == "gameover":
        wait_timer = time.time() + DELAY_TIME
        status = "gameover-wait"
    
    elif status == "gameover-wait":
        if (time.time() < wait_timer):
            return
        if keyboard.space or keyboard.lshift:
            status = "start"
    
    elif status == "game1" or status == "game2":
        scroll_position += scroll_speed
        if (scroll_position >= 600):
            scroll_position = 0

        # Laserien päivitys
        for this_laser in lasers:
            this_laser.update(time_interval)

            if this_laser.y <= 0:
                lasers.remove(this_laser)

            elif enemies1.check_laser(this_laser):
                player.score += 10
                lasers.remove(this_laser)
                sounds.asteroid_explode.play()

            elif enemies2.check_laser(this_laser):
                player.score += 10
                lasers.remove(this_laser)
                sounds.asteroid_explode.play()

        if status == "game1":
            if enemies1.check_crash(spacecraft, spacecraft_hit_pos):
                player.lives -= 1

                if player.lives < 1:
                    status = "gameover"
                    return
                
                else:
                    sounds.ship_explode.play()


        elif status == "game2":
            if enemies2.check_crash(spacecraft, spacecraft_hit_pos):
                player.lives -= 1
                if player.lives < 1:
                    status = "gameover"
                    return
                
                else:
                    sounds.ship_explode.play()

        # Päivitetään viholliset
        enemies1.update(time_interval)
        enemies2.update(time_interval)

        # Pelajaan liikkuminen
        if keyboard.up:
            spacecraft.move("up")
        if keyboard.down:
            spacecraft.move("down")
        if keyboard.left:
            spacecraft.move("left")
        if keyboard.right:
            spacecraft.move("right")
        if keyboard.space or keyboard.lshift:

            if (time.time() > laser_last_fired + time_between_lasers):
                laser_last_fired = time.time()
                lasers.append(Laser("laser_green",(spacecraft.x,spacecraft.y-25)))
                sounds.laser_shoot.play()

pgzrun.go()