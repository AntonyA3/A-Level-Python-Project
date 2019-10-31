import pygame
import  math
import random
from pygame.locals import *
def inverse_position(fixed_pos,invert_pos):
    inversed_position=[invert_pos[0]-fixed_pos[0],invert_pos[1]-fixed_pos[1]]
    return inversed_position


pygame.init()
class Sprite:
    def __init__(self,name,health,viewport_position,global_position,image):
        self.type=name

    def lose_health(self,health):
        self.health=max(self.health-health,0)
    def draw(self,surface):

        surface.blit(pygame.image.load(self.image),(self.viewport_position),None)

    def get_name(self):
        return self.name

class Enemies(Sprite):
    def __init__(self,name,health,viewport_position,global_position,image):
        Sprite.__init__(self,name,health,viewport_position,global_position,image)
        self.type=name
        self.global_position=[0,0]
    def offset_from_player(self,player):
        diffrence=inverse_position(player.global_position,self.global_position)
        self.viewport_position=[int(diffrence[0]+player.viewport_position[0]),int(diffrence[1]+player.viewport_position[1])]
    def ai(self,player,weapons,delta,difficulty):
        pass
    def give_score(self,player,information):
        pass


    def enemy_update(self,player,weapons,delta,information,difficulty):
        self.offset_from_player(player)
        self.ai(player,weapons,delta,difficulty,information)
        self.give_score(player,information)
    def render_enemy(self,surface):
        self.draw(surface)

class Destroyer(Enemies):
    def __init__(self,name,health,viewport_position,global_position,radius,image):
        Sprite.__init__(self,name,health,viewport_position,global_position,image)
        self.name=name
        self.type = "Destroyer"
        self.health=health
        self.viewport_position=viewport_position
        self.global_position=global_position
        self.radius=0
        self.growth_size=0.00001
        self.dead=False
    def ai(self,player,weapons,delta,difficulty,information):
        self.growth_size+=((0.001/60)*delta)
        self.radius+=math.ceil(math.exp(self.growth_size))*math.ceil(difficulty["number"])

        if math.hypot(self.global_position[0]-player.global_position[0],self.global_position[1]-player.global_position[1])<self.radius-64:
            player.health=0





    def draw(self,surface):
        pygame.draw.circle(surface,(255,255,255),self.viewport_position,self.radius)




class Basic(Enemies):
    def __init__(self,velocity, name, health, viewport_position, global_position, image,speed):
        Enemies.__init__(self,velocity, name, health, viewport_position, global_position)
        self.name = name
        self.type="Basic"
        self.health = health
        self.image=image
        self.viewport_position = viewport_position
        self.global_position = global_position
        self.speed=speed
        self.direction=[0,0]
        self.dead=False
        self.rect=pygame.image.load(image).get_rect()
    def give_score(self,player,information):
         if self.dead==True:
            if player.health>0:
                information.score+=2
            if int(information.highscore) <= int(information.score):
                information.highscore = information.score
            return True
    def draw(self,surface):
        surface.blit(pygame.image.load(self.image),(self.viewport_position),None)

    def ai(self,player,weapons,delta,difficulty,information):

        x = player.global_position[0]+player.velocity[0]*3 - self.global_position[0]
        y = player.global_position[1]+player.velocity[1]*3 - self.global_position[1]
        distance = math.hypot(x, y)
        if distance!=0:
            speed=((self.speed/60)*delta)*(difficulty["number"]/2)
            self.direction=[ x / distance,y / distance]

            self.velocity=[self.direction[0]*speed,self.direction[1]*speed]
            if player.health <= 0:
                self.velocity = [self.velocity[0] * -0.1, self.velocity[1] * -0.1]
            self.global_position=[self.global_position[0]+self.velocity[0],self.global_position[1]+self.velocity[1]]
            self.rect[0], self.rect[1] = self.viewport_position[0], self.viewport_position[1]

        for weapon in player.bullets:
            if weapon.rect.colliderect(self.rect):
                self.health-=(5/difficulty["number"]*0.5)
                information.hit_bullets+=1
                weapon.dead=True


        if player.rect.colliderect(self.rect):
            player.health-=int(5*difficulty["number"])
            self.dead=True
        if self.health <= 0:

            self.dead = True
        if math.hypot(player.global_position[0]-self.global_position[0],player.global_position[1]-self.global_position[1])>2000:
            self.dead=True





class Enemyloader:
    def __init__(self,loader):
        self.loaderarray=loader
    def die(self):
        for enemy in self.loaderarray:
            if enemy.dead==True:
                self.loaderarray.remove(enemy)
    def load(self,player):

        if len(self.loaderarray)<50:
            self.loaderarray.append(Basic([19, 10], "enemy_no_" + str(3423534), 1, [0, 0],[player.global_position[0]+random.randrange(-1000,1000,1999),player.global_position[1]+random.randrange(-1000,1000,1999)],
                                         "images/basic enemy.png",random.randint(player.max_speed-2,player.max_speed)))


