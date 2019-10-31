#My modules that I will be using
import pygame
import sys
import math
import random
from pygame.locals import *
import time
from player import Player
from enemies import*
from ui import *
from gamefiles import Text_files
from info import  Information
from powerup import *

pygame.init()

game=True
FPS=60
clock=pygame.time.Clock()

screen=pygame.display.set_mode((1028,720),DOUBLEBUF|HWSURFACE|ANYFORMAT)

def inverse_position(fixed_pos,invert_pos):
    inversed_position=[invert_pos[0]-fixed_pos[0],invert_pos[1]-fixed_pos[1]]
    return inversed_position

class Viewport:
    def __init__(self,name,width,height):
        self.name=name
        self.width=width
        self.height=height
        self.surface=pygame.display.set_mode((self.width,self.height))
    def get_surface(self):
        return self.surface


class SpawnLocation:
    def __init__(self,player):
        self.player=player
    def spawn(self):
        pass





class Game:
    def __init__(self,name,viewport,players) :   #,,files):
        self.game=True
        self.state="menu"
        self.viewport=viewport
        self.players=players
        self.enemies=[Destroyer("die",200,[200,200],[0,100],1,"images/hg")]
        self.guis={}
        self.text_files={"highscore":Text_files("highscore","textfiles\highscore.txt"),
                         "average score":Text_files("avsd","textfiles/average score.txt"),
                         "total bullets":Text_files("total bullets","textfiles/total bullets.txt"),
                         "hit bullets":Text_files("hit bullets","textfiles/hit bullets.txt"),
                         "total deaths":Text_files("total deaths","textfiles/total deaths.txt"),
                         "bullet accuracy":Text_files("bullet accuracy","textfiles/bullet accuracy.txt")}
        self.difficulty={"number":1}
        self.loader=Enemyloader(self.enemies)
        self.delta_time=pygame.time.get_ticks()
        self.spawn=SpawnLocation(self.players[0])
        self.bullets=[]
        self.information=Information(self)
        self.active_upgrade_booth=None
        self.inactive_upgrade_booths=[]
        self.instance_number=0.0010
        self.time=pygame.time.get_ticks()
        self.ticks_of_last_frame=0
        self.delta_time=0
        self.effector=Effector(self)
        self.inputter=Inputter()


        self.main_menu=Menus([Textbutton("play",None,32,pygame.Rect(500,300,200,100),(255,0,0),self.effector,"state_change","play"),
                              Textbutton("stats",None,32,pygame.Rect(500,400,200,100),(255,0,0),self.effector,"state_change","stats"),
                              Textbutton("options",None,32,pygame.Rect(500,500,200,100),(255,0,0),self.effector,"state_change","options"),
                              Textbutton("exit", None, 32, pygame.Rect(500, 600, 200, 100), (255, 0, 0),self.effector, "state_change", "exit"),
                              Text_box("Your Initials",None,32,pygame.Rect(500,200,200,100),(255,0,0),self.inputter,2)])


        self.stats_menu=Menus([Textlabel("Stats",None,[500,100],32,(255,0,0)),
                             Textlabel("highscore:  "+self.text_files["highscore"].read(),None,[500,300],32,(255,0,0)),
                             Textlabel("average score:  "+self.text_files["average score"].read(),None,[500,350],32,(255,0,0)),
                             Textlabel("total bullets:  "+self.text_files["total bullets"].read(),None,[500,400],32,(255,0,0)),
                             Textlabel("total deaths:  "+self.text_files["total deaths"].read(),None,[500,450],32,(255,0,0)),
                             Textlabel("hit accuracy:  "+self.text_files["bullet accuracy"].read()[0:3]+"%",None,[500,500],32,(255,0,0)),
                             Textbutton("back",None,32,pygame.Rect(0,600,100,100),(255,0,0),self.effector,"state_change","menu")])

        self.options_menu=Menus([Textbutton("reset",None,32,pygame.Rect(400,100,100,400),(255,0,0),self.effector,"state_change","lol"),
                                 Textlabel("acceleration is",None,[400,200],32,(255,0,0)),
                                 Textlabel("up,down,left,right",None,[400,150],32,(255,0,0))
                                 ,
                                 Textlabel("deceleration is", None, [400, 300], 32, (255, 0, 0)),
                                 Textlabel("left is", None, [400, 400], 32, (255, 0, 0)),
                                 Textlabel("right is", None, [400, 500], 32, (255, 0, 0)),
                                 Textbutton("back",None,32,pygame.Rect(0,600,100,100),(255,0,0),self.effector,"play_or_menu","choice"),
                                 Representer(pygame.key.name(self.players[0].key_mapping["forward"]), None, 32, pygame.Rect(600, 200, 200, 100), (255, 0, 0),self.inputter, 4,self.players[0],"map_forward"),
                                 Representer("S", None, 32, pygame.Rect(600, 300, 200, 100), (255, 0, 0), self.inputter,  4,self.players[0],"map_backward"),
                                 Representer("A", None, 32, pygame.Rect(600, 400, 200, 100), (255, 0, 0), self.inputter,  4,self.players[0],"map_left"),
                                 Representer("D", None, 32, pygame.Rect(600, 500, 200, 100), (255, 0, 0), self.inputter,  4,self.players[0],"map_right"),
                                 Tick_box((255, 0, 0),pygame.Rect(600,150,32,32),"alt_input",self.players[0])])

        self.game_overlay=Menus([Textlabel("score:"+str(self.information.score), None, [0, 0], 32, (255, 0, 0)),
                                 Textlabel("highscore:"+str(self.information.highscore), None, [200, 0], 32, (255, 0, 0))])

        self.pause_menu=Menus([Textlabel("pause",None,[400,400],32,(255,0,0)),
                               Textbutton("resume", None, 32, pygame.Rect(500, 600, 200, 100), (255, 0, 0), self.effector,"state_change", "play"),
                               Textbutton("options",None,32,pygame.Rect(500,400,200,100),(255,0,0),self.effector,"state_change","options"),
                               Textbutton("exit to menu", None, 32, pygame.Rect(500, 500, 200, 100), (255, 0, 0),self.effector, "game_reset", "menu")
                               ])

        self.game_over_screen=Menus([Textlabel("Game Over",None,[400,400],32,(255,0,0)),
                                     Textbutton("reset", None, 32, pygame.Rect(400, 100, 100, 400), (255, 0, 0),self.effector, "game_reset", "play"),
                                     Textbutton("quit to menu", None, 32, pygame.Rect(400, 200, 100, 400), (255, 0, 0),self.effector, "game_reset", "menu")
                                     ])

        self.current_menu=self.main_menu

    # def initialisation(self):
    #     #in_game_gui
    #     self.guis.update({"game_over":Textlabel("Game Over",None,(200,200),32,(255, 0, 0))})
    #     self.guis.update({"score": Textlabel("Score: 0", None, (10, 00), 32, (255, 0, 0))})
    #
    #     self.guis.update({"highscore": Textlabel("highscore:"+str(self.text_files["highscore"].read()), None, (300, 00), 32, (255, 0, 0))})
    #     self.information.highscore=str(self.text_files["highscore"].read())
    #
    #     #main_mene_gui
    #     self.guis.update({"playbutton":Textbutton("play",None,32,pygame.Rect(100,500,200,100),(255,0,0))})
    #     self.guis.update({"options":Textbutton("options",None,32,pygame.Rect(400,400,200,100),(255,0,0))})
    #     self.guis.update({"exit":Textbutton("exit",None,32,pygame.Rect(400,300,200,100),(255,0,0))})
    #     #options gui
    #
    #
    #     self.guis.update({"reset":Textbutton("reset high score",None,32,pygame.Rect(400,50,200,100),(255,0,0))})
    #     self.guis.update({"options back":Textbutton("back",None,32,pygame.Rect(40,500,200,100),(255,0,0))})
    #     self.guis.update({"map_forward": Textbutton("change_acceleration", None, 32, pygame.Rect(400, 100, 200, 100), (255, 0, 0))})
    #     self.guis.update({"map_backward": Textbutton("change_deceleration", None, 32, pygame.Rect(400, 200, 200, 100), (255, 0, 0))})
    #     self.guis.update({"map_left": Textbutton("change_left", None, 32, pygame.Rect(400, 300, 200, 100), (255, 0, 0))})
    #     self.guis.update({"map_right": Textbutton("change_right", None, 32, pygame.Rect(400, 400, 200, 100), (255, 0, 0))})
    #     self.guis.update({"chosen_key":Textlabel("w",None,[0,0],32,(255, 0, 0))})
    #
    #     #pause
    #     self.guis.update({"resume": Textbutton("resume", None, 32, pygame.Rect(400, 500, 200, 100), (255, 0, 0))})
    #     self.guis.update({"options": Textbutton("options", None, 32, pygame.Rect(400,600, 200, 100), (255, 0, 0))})
    #     self.guis.update({"exit_main_menu": Textbutton("exit to main menu", None, 32, pygame.Rect(400, 300, 200, 100), (255, 0, 0))})
    #     # main_mene_gui
    #     self.guis.update({"resume": Textbutton("resume", None, 32, pygame.Rect(400, 500, 200, 100), (255, 0, 0))})
    #     self.guis.update({"options": Textbutton("options", None, 32, pygame.Rect(400,
    #                                                                              600, 200, 100), (255, 0, 0))})
    #     self.guis.update({"exit_main_menu": Textbutton("exit to main menu", None, 32, pygame.Rect(400, 300, 200, 100), (255, 0, 0))})
    #
    #     #difficulty menu
    #     self.guis.update({"easy": Textbutton("Easy", None, 32, pygame.Rect(400, 200, 200, 100), (255, 0, 0))})
    #     self.guis.update({"medium": Textbutton("Medium", None, 32, pygame.Rect(400, 300, 200, 100), (255, 0, 0))})
    #     self.guis.update({"hard": Textbutton("Hard", None, 32, pygame.Rect(400, 400, 200, 100), (255, 0, 0))})
    #     self.guis.update({"ultra hard": Textbutton("Ultra Hard", None, 32, pygame.Rect(400, 500, 200, 100), (75,0,130))})
    #
    #     #pause menu
    #     self.guis.update({"resume": Textbutton("resume", None, 32, pygame.Rect(100, 200, 200, 100), (255, 0, 0))})
    #     self.guis.update({"to_main_menu": Textbutton("exit to main menu", None, 32, pygame.Rect(100, 300, 200, 100), (255, 0, 0))})
    #
    #
    #     #play again
    #     self.guis.update({"play again": Textbutton("Play Again", None, 32, pygame.Rect(400, 500, 200, 100), (255,0,0))})


    def draw_upgrade_booths(self):

        if self.active_upgrade_booth!=None:
            diffrence =inverse_position(self.players[0].global_position,self.active_upgrade_booth.global_position)


            self.active_upgrade_booth.viewport_position = [int(diffrence[0] + self.players[0].viewport_position[0]),
                                       int(diffrence[1] + self.players[0].viewport_position[1])]
            self.active_upgrade_booth.rect[0],self.active_upgrade_booth.rect[1]=self.active_upgrade_booth.viewport_position[0],self.active_upgrade_booth.viewport_position[1]
            if self.players[0].rect.colliderect(self.active_upgrade_booth.rect):
                self.active_upgrade_booth.activated(self.players[0])
                self.inactive_upgrade_booths.append(self.active_upgrade_booth.global_position)
            self.active_upgrade_booth.draw(self.viewport)




    def upgrade_booth_generate(self):
        invalid=False
        for i in range(-1000, 1000, 1000):
            random.seed(233422)
            nearest_2000_x=i+self.players[0].global_position[0]-(i+self.players[0].global_position[0]%2000)
            nearest_2000_y =i+self.players[0].global_position[1] - (i+self.players[0].global_position[1] % 2000)

            x=random.randrange(i+nearest_2000_x,i+nearest_2000_x+2000)
            y=random.randrange(i+nearest_2000_y,i+nearest_2000_y+2000)
            for position in self.inactive_upgrade_booths:
                if position==[x,y]:
                    invalid=True
            if invalid!=True:
                self.active_upgrade_booth=Upgrade_booth("booth", 100, [0, 0], [x, y],"images\ok.png")



    def upgrade_booth_function(self):
        self.active_upgrade_booth.inactive_position(self.inactive_upgrade_booths)
        if self.active_upgrade_booth.dead==True:
            self.active_upgrade_booth=None


    def check_quit(self):

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state=="play":
                        self.state="pause"
                        time.sleep(0.25)

                    elif self.state=="pause":
                        self.state="play"

                self.inputter.kek(pygame.key.name(event.key))


    def enemy_functions(self):
        random.seed()

        for enemy in self.enemies:
            enemy.enemy_update(self.players[0],self.players[0].bullets,self.delta_time,self.information,self.difficulty)
            # self.guis["highscore"].update_text("highscore:" + str(self.information.highscore))
            # self.guis["score"].update_text("score:" + str(self.information.score))
        self.loader.load(self.players[0])

        # if len(self.enemies) < 50 and self.players[0].health>0:
        #     plr_glob_pos=self.players[0].global_position
        #     self.instance_number+=0.0001
        #     self.enemies.update({str(self.instance_number):(Basic([19, 10], "enemy_no_" + str(3423534), 1, [0, 0],[plr_glob_pos[0]+random.randrange(-1000,1000,1999),plr_glob_pos[1]+random.randrange(-1000,1000,1999)],
        #                                  "images/basic enemy.png",random.randint(self.players[0].max_speed-2,self.players[0].max_speed)))})
        self.loader.die()


    def enemy_draw(self):
        for enemy in self.enemies:
            enemy.render_enemy(self.viewport)

    # def bullet_function(self):
    #     for bullet in self.players[0].bullets:
    #         bullet.shooting(self.players[0])
    #         diffrence=inverse_position(self.players[0].global_position,bullet.global_position)
    #
    #         bullet.viewport_position=[int(diffrence[0]+self.players[0].viewport_position[0]),int(diffrence[1]+self.players[0].viewport_position[1])]
    #
    #         if bullet.get_dead()==True:
    #             self.players[0].bullets.remove(bullet)

    # def bullet_draw(self):
    #     for bullet in self.players[0].bullets:
    #         bullet.draw(self.viewport)
    # def game_over_screen(self):
    #     if self.players[0].health <= 0:
    #
    #         self.guis["game_over"].draw(self.viewport)
    #         self.guis["play again"].draw(self.viewport)
    #         if self.guis["play again"].rect.contains(pygame.Rect(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],1,1)) and pygame.mouse.get_pressed()[0]!=0:
    #             self.players=[Player("player1",100,[1028/2,720/2],[20,20],[0,1],0,"images\player spaceship.png",100)]
    #             self.enemies=self.enemies={"0.00001":Destroyer("main_destroyer",100,[0,0],[400,400],0,"djsdh")}
    #             self.state="play"
    #     self.guis["score"].draw(self.viewport)
    #     self.guis["highscore"].draw(self.viewport)
    #
    # def main_menu(self):
    #     self.viewport.fill((0, 0, 0))
    #     if self.guis["playbutton"].rect.contains(pygame.Rect(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],1,1)) and pygame.mouse.get_pressed()[0]!=0:
    #
    #                  self.state="difficulty_menu"
    #
    #
    #     if self.guis["exit"].rect.contains(pygame.Rect(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],1,1)) and pygame.mouse.get_pressed()[0]!=0:
    #                 pygame.quit()
    #                 sys.exit()
    #     if self.guis["options"].rect.contains(pygame.Rect(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],1,1)) and pygame.mouse.get_pressed()[0]!=0:
    #                 self.state="options"
    #     self.guis["playbutton"].draw(self.viewport)
    #     self.guis["options"].draw(self.viewport)
    #     self.guis["exit"].draw(self.viewport)
    #
    # def choose_key_loop(self,direction):
    #     self.guis["chosen_key"].draw(self.viewport)
    #     for event in pygame.event.get():
    #         if event.type == pygame.KEYDOWN:
    #             self.players[0].key_mapping[direction] = event.key
    #
    #             self.guis["chosen_key"].update_text(str(pygame.key.name(event.key)))
    #             return True
    # def options_menu(self):
    #     self.viewport.fill((0, 0, 0))
    #
    #     if self.guis["reset"].rect.contains(pygame.Rect(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],1,1)) and pygame.mouse.get_pressed()[0]!=0:
    #         self.text_files["highscore"].write(str(0))
    #     if self.guis["map_forward"].rect.contains(pygame.Rect(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],1,1)):
    #         self.guis["chosen_key"].update_text(str(pygame.key.name(self.players[0].key_mapping["forward"])))
    #         if pygame.mouse.get_pressed()[0]!=0:
    #             chosen=False
    #
    #             while chosen==False:
    #                 if self.choose_key_loop("forward")==True:
    #                     chosen=True
    #     elif self.guis["map_backward"].rect.contains(
    #             pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)):
    #         self.guis["chosen_key"].update_text(
    #             str(pygame.key.name(self.players[0].key_mapping["backward"])))
    #         if pygame.mouse.get_pressed()[0] != 0:
    #             chosen = False
    #
    #             while chosen == False:
    #                 if self.choose_key_loop("backward")==True:
    #                     chosen=True
    #
    #
    #     elif self.guis["map_left"].rect.contains(
    #             pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)):
    #         self.guis["chosen_key"].update_text(str(pygame.key.name(self.players[0].key_mapping["left"])))
    #         if pygame.mouse.get_pressed()[0] != 0:
    #             chosen = False
    #             while chosen == False:
    #                 if self.choose_key_loop("left")==True:
    #                     chosen=True
    #
    #     elif self.guis["map_right"].rect.contains(
    #             pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)):
    #         self.guis["chosen_key"].update_text(str(pygame.key.name(self.players[0].key_mapping["right"])))
    #         if pygame.mouse.get_pressed()[0] != 0:
    #             chosen = False
    #             while chosen == False:
    #                 if self.choose_key_loop("right")==True:
    #                     chosen=True
    #
    #
    #
    #
    #
    #
    #     if self.guis["options back"].rect.contains(pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)) and pygame.mouse.get_pressed()[0] !=0:
    #         self.state="menu"
    #
    # def pause_menu(self):
    #     self.guis["resume"].draw(self.viewport)
    #     self.guis["to_main_menu"].draw(self.viewport)
    #     if self.guis["to_main_menu"].rect.contains(pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)) and pygame.mouse.get_pressed()[0] !=0:
    #         self.players=[Player("player1",100,[1028/2,720/2],[20,20],[0,1],0,"images\player spaceship.png",100)]
    #         self.enemies=self.enemies={"0.00001":Destroyer("main_destroyer",100,[0,0],[400,400],0,"djsdh")}
    #         self.state="menu"
    #
    #
    #     if self.guis["resume"].rect.contains(pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)) and pygame.mouse.get_pressed()[0] !=0:
    #         self.state="play"
    #
    #
    #
    # def draw_options(self):
    #     self.guis["reset"].draw(self.viewport)
    #     self.guis["map_forward"].draw(self.viewport)
    #
    #     self.guis["chosen_key"].draw(self.viewport)
    #     self.guis["options back"].draw(self.viewport)
    #     self.guis["map_backward"].draw(self.viewport)
    #     self.guis["map_left"].draw(self.viewport)
    #
    #     self.guis["map_right"].draw(self.viewport)
    #
    # def difficult_menu(self):
    #
    #     if self.guis["easy"].rect.contains(pygame.Rect(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],1,1)) and pygame.mouse.get_pressed()[0]!=0:
    #         self.state="play"
    #         self.difficulty={"number":0.75}
    #
    #     if self.guis["medium"].rect.contains(pygame.Rect(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],1,1)) and pygame.mouse.get_pressed()[0]!=0:
    #         self.state="play"
    #         self.difficulty={"number":1}
    #     if self.guis["hard"].rect.contains(pygame.Rect(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],1,1)) and pygame.mouse.get_pressed()[0]!=0:
    #         self.state="play"
    #         self.difficulty={"number":1.5}
    #     if self.guis["ultra hard"].rect.contains(pygame.Rect(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],1,1)) and pygame.mouse.get_pressed()[0]!=0:
    #         self.state="play"
    #         self.difficulty={"number":2.5}
    #     self.guis["easy"].draw(self.viewport)
    #     self.guis["medium"].draw(self.viewport)
    #     self.guis["hard"].draw(self.viewport)
    #     self.guis["ultra hard"].draw(self.viewport)
    #
    # def gui_functions(self):
    #     for gui in self.guis:
    #         gui.draw()
    # def set_game_state(self):
    #     if pygame.key.get_pressed()[K_ESCAPE] != 0 and self.state=="play":
    #         self.state="pause"
    #     if pygame.key.get_pressed()[K_TAB] != 0:
    #         self.state="play"


    def main_loop(self):
         while self.game==True:

             self.time=pygame.time.get_ticks()
             self.viewport.fill((0, 0, 0))

             self.check_quit()

             # if self.state=="menu":
             #     self.main_menu()
             #
             # if self.state=="options":
             #
             #    self.options_menu()
             #    self.draw_options()
             #
             # if self.state=="difficulty_menu":
             #     self.viewport.fill((0, 0, 0))
             #     self.difficult_menu()

             for part in self.current_menu.ui_parts:
                 part.action(pygame.mouse)

                 part.draw(self.viewport)

             if self.state=="stats":
                 self.current_menu=self.stats_menu

             if self.state=="menu":
                 self.current_menu=self.main_menu
             if self.state=="options":
                 self.current_menu=self.options_menu
             if self.state=="exit":
                self.game=False

             if self.state=="play":
                self.current_menu=self.game_overlay
                self.loader.loaderarray=self.enemies
                for player in self.players:
                    player.update(self.delta_time,self.information)

                self.current_menu.ui_parts[0]=Textlabel("score:"+str(self.information.score), None, [0, 0], 32, (255, 0, 0))

                self.current_menu.ui_parts[1]=Textlabel("highscore:"+str(self.information.highscore), None, [200, 0], 32, (255, 0, 0))

                self.upgrade_booth_generate()
                self.enemy_functions()
                # self.bullet_function()

                # self.set_game_state()

                # self.viewport.fill((0, 0, 0))
                # self.bullet_draw()
                for player in self.players:
                    player.draw(self.viewport)
                self.draw_upgrade_booths()
                self.enemy_draw()
                self.draw_upgrade_booths()
                # self.game_over_screen()
                if self.players[0].health<=0:
                    self.state="game_over"

                    self.information.game_over_routine()




             if self.state == "pause":
                # self.set_game_state()
                self.current_menu=self.pause_menu
                for player in self.players:
                    player.draw(self.viewport)
                self.enemy_draw()
                # self.bullet_draw()
                # self.pause_menu()





             if self.state=="game_over":

                # if int(self.information.highscore)>int(self.text_files["highscore"].read()):
                #     self.text_files["highscore"].write(str(self.information.highscore))

                self.enemy_functions()

                # self.bullet_function()
                self.current_menu=self.game_over_screen

                # self.bullet_draw()
                for player in self.players:
                    player.draw(self.viewport)
                self.enemy_draw()
                # self.game_over_screen()




             self.delta_time=(self.time-self.ticks_of_last_frame)*2

             self.ticks_of_last_frame=self.time

             clock.tick(FPS)
             pygame.display.flip()

game=Game("the_game",screen,[Player("player1",100,[1028/2,720/2],[20,20],[0,1],0,"images\player spaceship.png",100)])

game.main_loop()
