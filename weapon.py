import math
import pygame
from pygame.locals import *
from enemies import Sprite

class Bullet(Sprite):
    def __init__(self,angle,speed,name,health,viewport_position,global_position,image):
        Sprite.__init__(self,name,health,viewport_position,global_position,image)
        self.angle=angle
        self.speed=speed
        self.image=image
        self.name=name
        self.viewport_position=viewport_position
        self.global_position=global_position
        self.activated=True
        self.origin = global_position
        self.dead=False
        self.rect=pygame.image.load(image).get_rect()



    def shoot(self):
        self.activated=True
    def shooting(self,player):
        if self.dead==False:
            bullet_sin=math.sin(self.angle+math.radians(180))
            player_sin=math.sin(player.get_angle())
            self.global_position=[self.global_position[0]+math.cos(self.angle)*self.speed,self.global_position[1]+math.sin(self.angle)*self.speed]
            self.rect[0],self.rect[1]=self.viewport_position[0],self.viewport_position[1]
        if abs(math.hypot(self.global_position[0]-self.origin[0],self.global_position[1]-self.origin[1]))>1000:
            self.dead=True
    def get_dead(self):
        return self.dead

