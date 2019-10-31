import math
import pygame

from pygame.locals import *

from enemies import Sprite
from weapon import Bullet
pygame.init()
def inverse_position(fixed_pos,invert_pos):
    inversed_position=[invert_pos[0]-fixed_pos[0],invert_pos[1]-fixed_pos[1]]
    return inversed_position

class Player(Sprite):
    def __init__(self,name,health,viewport_position,global_position,direction,angle,image,max_health):
        Sprite.__init__(self,name,health,viewport_position,global_position,image)
        self.name=name
        self.key_mapping={"forward":K_w,"backward":K_s,"left":K_a,"right":K_d}
        self.image=image
        self.health=health
        self.rect=pygame.image.load(self.image).get_rect()
        self.viewport_position=viewport_position
        self.global_position=global_position
        self.start_position=global_position
        self.speed=0
        self.angle=angle
        self.direction=direction
        self.velocity=[direction[0]*self.speed,direction[1]*self.speed]
        self.max_speed=10
        self.bullets=[]
        self.angle_offset=90
        self.time=pygame.time.get_ticks()
        self.distance_from_start=0
        self.max_health=max_health
        self.health_fraction=1
        self.weapon_delay=40

    def bullet_function(self):
        for bullet in self.bullets:
            bullet.shooting(self)
            diffrence = inverse_position(self.global_position, bullet.global_position)

            bullet.viewport_position = [int(diffrence[0] + self.viewport_position[0]),
                                        int(diffrence[1] + self.viewport_position[1])]

            if bullet.get_dead() == True:
                self.bullets.remove(bullet)


    def get_angle(self):
        return self.angle+self.angle_offset

    def mouse_to_output(self,delta,information):
        """

        :param delta: The time between processing the last frame and the current frame
        :return:
        """
        current_delay=(self.weapon_delay/60)*delta
        if pygame.mouse.get_pressed()[0] != 0:
            information.total_bullets+=1
            if abs(self.time - pygame.time.get_ticks()) > current_delay:
                self.time = pygame.time.get_ticks()
                x = pygame.mouse.get_pos()[0] - self.rect.center[0]
                y = pygame.mouse.get_pos()[1] - self.rect.center[1]
                distance = math.hypot(x, y)
                if distance!=0:
                    x_move = x / distance
                    y_move = y / distance
                    angle = math.atan2(y_move, x_move)

                    if self.speed<0:
                        bullet_speed=20
                    else:
                        bullet_speed=self.speed + 10

                    self.bullets.append(Bullet(angle, bullet_speed, "bullet_" + str(1), 10, self.viewport_position,
                                           [self.global_position[0] + 16, self.global_position[1] + 16],
                                           "images/bullet.png"))

    def keyboard_to_output(self,delta):
        """

        :param delta: The time between processing the last frame and the current frame
        :return:
        """
        max_speed=(self.max_speed/60)*delta
        speed_change=False
        #To detect if the key mapped to forward is pressed if it is it will accelerate the player.
        if pygame.key.get_pressed()[self.key_mapping["forward"]]!=0:
            self.speed=min(self.speed+(4/60)*delta,max_speed) #speed increases or becomes the maximum speer
            speed_change=True
        #To detect if the key mapped to backward is pressed if it is, it will decelerate the player.
        if pygame.key.get_pressed()[self.key_mapping["backward"]] != 0:
            self.speed =max(self.speed-(4/60)*delta,-1*max_speed) #speed decreases or becames the minimum speed
            speed_change=True
        #To detect if the key mapped to left is pressed if it is it will change the angle.
        if pygame.key.get_pressed()[self.key_mapping["left"]] != 0:
            self.angle+=(2/60)*delta
        #To detect if the key mapped to right is pressed It will change the player angle.

        if pygame.key.get_pressed()[self.key_mapping["right"]] != 0:
            self.angle-=(2/60)*delta
        #To detect if the key X is pressed it will slow down the player exponentially.
        if pygame.key.get_pressed()[K_x] != 0:
            self.speed=self.speed/(1+(delta*(0.05/60)))
            if self.speed<0.25:
                self.speed=0
        #This will automatically slow down the player if there is no change in speed.
        if speed_change!=True:
            self.speed/=(1+(delta*(0.01/60)))


    def update_physics(self):
        """

        :return:
        """

        self.direction=[math.cos(math.radians(-1*(self.angle+self.angle_offset))),math.sin(math.radians(-1*(self.angle+self.angle_offset)))]
        self.global_position=[self.global_position[0]+self.direction[0]*self.speed,self.global_position[1]+self.direction[1]*self.speed]
        self.distance_from_start=math.hypot(self.start_position[0]-self.global_position[0],self.start_position[1]-self.global_position[1])
        self.rect[0],self.rect[1]=self.viewport_position



    def draw(self, surface):
        """

        :param surface: This is the surface that the player image will be draw onto
        :return:
        """
        #This rotates the image by first rotating a Pygame.rect that is the same size as the image then
        # recenter the image to that position
        rect_center = self.rect.center
        image = pygame.transform.rotate(pygame.image.load("images\player spaceship.png"), self.angle)
        image_rect= image.get_rect()
        image_rect.center=rect_center

        self.health_fraction=self.health/self.max_health
        #a pygame .rec
        pygame.draw.rect(surface, (255,0 , 0), (10, 30, 200, 10))
        if self.health>0:
            pygame.draw.rect(surface,(0,255,0),(10,30,int(200*self.health_fraction),10))

        surface.blit(image, (image_rect))
        for bullet in self.bullets:
            bullet.draw(surface)

    def game_interfere(self):
        if self.health == 0:
            return "game_over"
    def update(self,delta,information):
        """
        :param delta: The time between processing the last frame and the current frame
        :return:
        """
        self.bullet_function()
        self.mouse_to_output(delta,information)
        self.keyboard_to_output(delta)
        self.update_physics()
        self.game_interfere()










