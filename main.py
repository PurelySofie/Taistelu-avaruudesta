import time
import sys
import pgzrun
from pygame import K_SPACE, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_a, K_d, K_w, K_s, K_ESCAPE, K_RETURN
from pgzero.actor import Actor

from player import Player
from playership import PlayerShip
from laser import Laser
from enemies import Enemies

WIDTH = 1000
HEIGHT = 800
TITLE = "Taistelu Avaruudesta"
ICON = "asteroid_icon.png"

scroll_speed = 2
scroll_position = 0

player = Player()

playership = PlayerShip("goodship", (WIDTH*2, HEIGHT*2))
playership.set_speed(5)

enemies = Enemies((WIDTH, HEIGHT), "level1.dat")

lasers = []
laser_last_fired = 0
time_between_lasers = 0.5

playership_hit_pos = [
    (0,-40), (10,-30), (-10,-30), (13,-15), (-13,-15), (25,-3), (-25,-3),
    (46,12), (-46,12), (25,24), (-25,24), (10,27), (-10,27), (0,27) ]

status = "start"

wait_timer = 0


def draw():
    screen.blit("space", (0,scroll_position-800))
    screen.blit("space", (0,scroll_position))

    enemies.draw(screen)

    playership.draw()

    for this_laser in lasers:
        this_laser.draw()

    screen.draw.text("Score: {}".format(player.score), fontname="computerspeak", fontsize=40, topleft=(30,30), color=(255,255,255))
    screen.draw.text("Lives: {}".format(player.lives), fontname="computerspeak", fontsize=40, topright=(770,30), color=(255,255,255))

    if status == "start" or status == "start-wait":
        screen.draw.text("Press fire to start game", fontname="computerspeak", fontsize=40, center=(400,300), color=(255,255,255))
    elif status == "gameover" or status == "gameover-wait":
        screen.draw.text("Game Over", fontname="computerspeak", fontsize=40, center=(400,200), color=(255,255,255))

def update():
    global status, scroll_position, shot_last_fired, wait_timer
    # Allow Escape to quit straight out of the game regardless of state of the game
    if keyboard.escape:
        sys.exit()
    # Wait on fire key press to start game
    if status == "start":
        # start timer
        wait_timer = time.time() + DELAY_TIME
        status = "start-wait"
    if status == "start-wait":
        if (time.time() < wait_timer):
            return
        if keyboard.space or keyboard.lshift:
            player.reset()
            enemies.reset()
            status = "game"
    elif status == "gameover":
        # start timer
        wait_timer = time.time() + DELAY_TIME
        status = "gameover-wait"
    elif status == "gameover-wait":
        if (time.time() < wait_timer):
            return
        if keyboard.space or keyboard.lshift:
            status = "start"
    elif status == "game":
        # Scroll screen
        scroll_position += scroll_speed
        if (scroll_position >= 600):
            scroll_position = 0

        # Update existing shots
        for this_shot in shots:
            # Update position of shot
            this_shot.update(time_interval)
            if this_shot.y <= 0:
                shots.remove(this_shot)
            # Check if hit asteroid or enemy
            elif enemies.check_shot(this_shot):
                player.score += 10
                # remove shot (otherwise it continues to hit others)
                shots.remove(this_shot)
                sounds.asteroid_explode.play()

        if enemies.check_crash(playership, playership_hit_pos):
            player.lives -= 1
            if player.lives < 1:
                status = "gameover"
                return
            else:
                sounds.space_crash.play()

        # Update enemies after checking for a shot hit
        enemies.update(time_interval)

        # Handle keyboard
        if keyboard.up:
            playership.move("up")
        if keyboard.down:
            playership.move("down")
        if keyboard.left:
            playership.move("left")
        if keyboard.right:
            playership.move("right")
        if keyboard.space or keyboard.lshift:
            # check if time since last shot reached
            if (time.time() > laser_last_fired + time_between_lasers):
                # rest time last fired
                laser_last_fired = time.time()
                lasers.append(Laser("bullet_blue",(playership.x,playership.y-25)))
                # Play sound of gun firing
                #sounds.space_gun.play()

pgzrun.go()
