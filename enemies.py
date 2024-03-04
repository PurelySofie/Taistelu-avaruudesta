import sys
import time
import csv
from constants import *
from pgzero.actor import Actor
from asteroid import Asteroid

class Enemies:

    def __init__(self, screen_size, configfile):
        self.screen_size = screen_size
        self.asteroids = []
        self.level_time = time.time()
        self.level_end = None
        # Tasojen tiedostojen lataus
        try:
            with open(configfile, 'r') as file:
                csv_reader = csv.reader(file)
                for enemy_details in csv_reader:
                    if enemy_details[1] == "end":
                        self.level_end = float(enemy_details[0])

                    elif enemy_details[1] == "asteroid":
                        start_time = float(enemy_details[0])
                        image = enemy_details[2]
                        start_pos = (int(enemy_details[3]),
                            int(enemy_details[4]))
                        velocity = float(enemy_details[5])
                        self.asteroids.append(Asteroid(start_time, image, start_pos, velocity))
        
        except IOError:
            print ("Config Error "+configfile)
            sys.exit()
        
        except:
            print ("Config Corrupt "+configfile)
            sys.exit()


    def next_level (self):
        self.level_time = time.time()
        for this_asteroid in self.asteroids:
            this_asteroid.reset()


    def reset (self):
        self.level_time = time.time()
        for this_asteroid in self.asteroids:
            this_asteroid.reset()


    # Päivittää kaikkien vihollisten paikat
    def update(self, time_interval):
        if (self.level_end != None and
            time.time() > self.level_time + self.level_end):
                self.next_level()

        for this_asteroid in self.asteroids:
            this_asteroid.update(self.level_time, time_interval)



    # Piirtää kaikki aktiiviset viholliset ruudulle
    def draw(self, screen):
        for this_asteroid in self.asteroids:
            this_asteroid.draw()



    # Katsoo osuuko pelaajan ampuna laseri viholliseen
    def check_laser(self, laser):
        for this_asteroid in self.asteroids:

            # Jos vihollinen ei ole näkyvissä laseri ei osu
            if this_asteroid.status != STATUS_VISIBLE:
                continue

            if (this_asteroid.colliderect(laser)):
                this_asteroid.hit()
                return True

        return False

    # Katsoo osuuko pelaajan avaruusalus viholliseen
    def check_crash(self, spacecraft, collide_points=None):
        for this_asteroid in self.asteroids:


            # Jos vihollinen ei ole näkyvissä pelaaja ei osu
            if this_asteroid.status != STATUS_VISIBLE:
                continue


            if (this_asteroid.colliderect(spacecraft)):
                if (collide_points == None):
                    this_asteroid.status = STATUS_DESTROYED
                    return True
                
                for this_point in collide_points:
                    if this_asteroid.collidepoint(
                        spacecraft.x+this_point[0],
                        spacecraft.y+this_point[1] ):
                            this_asteroid.status = STATUS_DESTROYED
                            return True
        return False