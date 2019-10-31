import pygame
import time

from pygame.locals import *
from player import Player
class Menus:
    def __init__(self,ui_parts):
        self.ui_parts=ui_parts

class Effector:
    def __init__(self,game):
        self.game=game
    def change_state(self,new_value):
        self.game.state=new_value
    def reset_game(self,new_value):

        self.game.players[0]=Player("player1",100,[1028/2,720/2],[20,20],[0,1],0,"images\player spaceship.png",100)
        self.game.enemies=[]
        self.change_state(new_value)



class Textlabel:
    def __init__(self,text,font,position,size,color):
        self.pure_text=text
        self.font = pygame.font.Font(font, size)
        self.color = color
        self.text = self.font.render(text, 0, self.color)
        self.position=position
        self.pure_text=text

    def update_text(self,text):
        self.text=self.font.render(text, 0, self.color)

    def update_color(self, color):
        self.color=color
        self.text = self.font.render(self.pure_text, 0, self.color)
    def draw(self,surface):
        surface.blit(self.text, self.position)
    def action(self,mouse):
        pass

class Textbutton:
    def __init__(self,text,font,size,rect,color,effector,to_change,new_value):
        self.font=pygame.font.Font(font,size)
        self.text=self.text = self.font.render(text, 0,color)
        self.pure_text=text
        self.size=size
        self.rect=rect
        self.to_change=to_change
        self.new_value=new_value
        self.effector=effector
    def update_text(self, text):
        self.text = self.font.render(text, 0, self.color)

    def update_color(self, color):
        self.color = color
        self.text = self.font.render(self.pure_text, 0, self.color)
    def draw(self,surface):
        surface.blit(self.text, self.rect)
    def action(self,mouse):
        if self.rect.contains(mouse.get_pos()[0], mouse.get_pos()[1], 1, 1) and mouse.get_pressed()[0] == 1:
            self.effector.game.inputter.inputting=None
            time.sleep(0.25)
            if self.to_change == "state_change":
                self.effector.change_state(self.new_value)
            if self.to_change =="game_reset":
                self.effector.reset_game(self.new_value)
            if self.to_change=="play_or_menu":
                # Decides which mode the game was in
                if len(self.effector.game.enemies)>0 or self.effector.game.players[0].global_position!=[20,20]:
                    self.effector.change_state("pause")
                else:
                    self.effector.change_state("menu")

class Inputter:
    def __init__(self):
        self.inputting=None
    def kek(self,letter):
        if self.inputting!=None:
            print(letter)

            if letter=="backspace":
                print("dsdfss")
                self.inputting.word=self.inputting.word[0:len(self.inputting.word)-1]
            if len(letter)==1 and len(self.inputting.word)<=self.inputting.max_len:
                self.inputting.word=self.inputting.word+str(letter.upper())
            self.inputting.text=self.inputting.font.render(self.inputting.word, 0, self.inputting.color)
            if letter == "return":
                self.inputting = None

class Tick_box:
    def __init__(self,color,rect,operation,operator):
        self.color=color
        self.rect=rect
        self.operation=operation
        self.operator=operator
        self.ticked=False
        self.font = pygame.font.Font(None, 60)

    def draw(self,surface):
        pygame.draw.rect(surface,self.color,self.rect,1)
        if self.ticked==True:
            print("lol")
            self.text = self.font.render("x", 0, self.color)
            surface.blit(self.text, self.rect)
        print(self.ticked)


    def action(self,mouse):

         if self.ticked==True:
            if self.operation=="alt_input":

                self.operator.key_mapping={"forward":K_UP,"backward":K_DOWN,"left":K_LEFT,"right":K_RIGHT}


         if self.rect.contains(mouse.get_pos()[0], mouse.get_pos()[1], 1, 1) and mouse.get_pressed()[0] == 1:


             time.sleep(0.4)
             if self.ticked==False:
                 self.ticked=True
             elif self.ticked==True:
                 self.ticked=False







class Text_box:
    def __init__(self,text,font,size,rect,color,inputter,max_len):
        self.font = pygame.font.Font(font, size)
        self.color=color
        self.text = self.font.render(text, 0, color)
        self.pure_text = text
        self.size = size
        self.rect = rect
        self.word=""
        self.max_len=max_len
        self.inputter=inputter
    def draw(self,surface):
        surface.blit(self.text, self.rect)
    def action(self,mouse):
        if self.rect.contains(mouse.get_pos()[0], mouse.get_pos()[1], 1, 1) and mouse.get_pressed()[0] == 1:
            self.word=""
            self.text = self.font.render("", 0, self.color)
            self.inputter.inputting=self

class Representer(Text_box):
    def __init__(self,text,font,size,rect,color,inputter,max_len,class_operator,opertation):
        Text_box.__init__(self,text,font,size,rect,color,inputter,max_len)
        self.font = pygame.font.Font(font, size)
        self.color=color
        self.text = self.font.render(text, 0, color)
        self.pure_text = text
        self.size = size
        self.rect = rect
        self.word=text
        self.max_len=max_len
        self.inputter=inputter
        self.class_operator=class_operator
        self.operation=opertation

    def action(self,mouse):

        if self.operation=="map_forward":
            if len(self.word)>0:
                self.class_operator.key_mapping["forward"]=ord(self.word.lower())
                print(self.class_operator.key_mapping["forward"])
        if self.rect.contains(mouse.get_pos()[0], mouse.get_pos()[1], 1, 1) and mouse.get_pressed()[0] == 1:
            self.word=""
            self.text = self.font.render("", 0, self.color)
            self.inputter.inputting=self

        if self.operation=="map_backward":
            if len(self.word)>0:
                self.class_operator.key_mapping["backward"]=ord(self.word.lower())
                print(self.class_operator.key_mapping["backward"])
        if self.rect.contains(mouse.get_pos()[0], mouse.get_pos()[1], 1, 1) and mouse.get_pressed()[0] == 1:
            self.word=""
            self.text = self.font.render("", 0, self.color)
            self.inputter.inputting=self

        if self.operation=="map_left":
            if len(self.word)>0:
                self.class_operator.key_mapping["left"]=ord(self.word.lower())
                print(self.class_operator.key_mapping["left"])
        if self.rect.contains(mouse.get_pos()[0], mouse.get_pos()[1], 1, 1) and mouse.get_pressed()[0] == 1:
            self.word=""
            self.text = self.font.render("", 0, self.color)
            self.inputter.inputting=self

        if self.operation=="map_right":
            if len(self.word)>0:
                self.class_operator.key_mapping["right"]=ord(self.word.lower())
                print(self.class_operator.key_mapping["right"])
        if self.rect.contains(mouse.get_pos()[0], mouse.get_pos()[1], 1, 1) and mouse.get_pressed()[0] == 1:
            self.word=""
            self.text = self.font.render("", 0, self.color)
            self.inputter.inputting=self

# class Menu:
#     def __init__(self,parts):
#         self.parts=parts
#     def draw(self, surface):
#         for part in self.parts:
#             surface.blit(part.text, part.rect)
#
#

