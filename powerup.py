import pygame
import  math
import random
from pygame.locals import *
from enemies import Sprite

class Health_powerup(Sprite):
    def __init__(self,name,health,viewport_position,global_position,image):
        Sprite.__init__(self,name,health,viewport_position,global_position,image)
        self.global_position=global_position
        self.viewport_position=viewport_position
        self.image=image


class Upgrade_booth(Sprite):
    def __init__(self,name,health,viewport_position,global_position,image):
        Sprite.__init__(self, name, health, viewport_position, global_position, image)
        self.global_position=global_position
        self.dead=False

        self.upgrades=["health_up","max_speed_up","reduce_delay","max_speed_up"]

        self.powerup="lol"
        self.image=image
        self.rect = pygame.image.load(self.image).get_rect()

    def activated(self,player):
        random.seed()
        self.powerup=self.upgrades[random.randrange(len(self.upgrades))]
        if self.powerup=="health_up":
            player.max_health=int(player.max_health*1.2)
            player.health=player.max_health
        if self.powerup=="max_speed_up":
            player.max_speed=int(player.max_speed*1.2)
        if self.powerup=="reduce_delay":
            player.weapon_delay=int(player.weapon_delay/1.2)




