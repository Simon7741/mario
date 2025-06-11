import pygame
from pygame.locals import *
import numpy as np
from pygame.transform import scale

file = 'images/NES - Super Mario Bros - Tileset.png'
file_enemy = 'images/NES - Super Mario Bros - Enemies & Bosses.png'

data = np.loadtxt('data_data.csv', delimiter=',')
data = np.int_(data)
bg_set = np.loadtxt('data_Background.csv', delimiter=',')
bg_set = np.int_(bg_set)
enemy_pos = np.loadtxt('data_enemy.csv', delimiter=',')
enemy_pos = np.int_(enemy_pos)
# print(data)

PUP     = pygame.K_w    #pohyb hráče nahoru
PDOWN   = pygame.K_s    #pohyb hráče dolu
PLEFT   = pygame.K_a    #pohyb hráče doleva
PRIGHT  = pygame.K_d    #pohyb hráče doprava
SPACE   = pygame.K_SPACE    #zoom kamery oddálení

FPS = 45
Life = 3
SCALE = 3
RESOLUTION = 16

clock = pygame.time.Clock()

class Game:
    W = 1280
    H = 720
    SIZE = W, H

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(Game.SIZE)
        pygame.display.set_caption("'Fake' Mario")
        self.running = True
        self.cam = [0,0]
        self.score = 0
        self.life = Life

    def run(self):
        while self.running:

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False

                elif event.type == KEYDOWN:
                    if event.key == K_l:
                        tilem.set_random()

                                        
                        # self.load_image(file)
            player.update()
            obstacle_group.update()
            game.render(background.image)
            game.render(tilem.image)
            player.draw(self.screen)
            enemy_group.update()
            score.render()

            pygame.display.update()
            clock.tick(FPS)

        pygame.quit()

    # def rscore(self):
    #     pass


    def render(self,image):
        self.screen.blit(image,(self.cam[0],self.cam[1]))
        obstacle_group.draw(self.screen)

    def load_image(self, file):
        self.file = file
        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect()

        self.screen = pygame.display.set_mode(self.rect.size)
        pygame.display.set_caption(f'size:{self.rect.size}')
        self.screen.blit(self.image, self.rect)
        pygame.display.update()

class Text:
    def __init__(self,text,color,pos):
        self.text_font = pygame.font.Font("PixelifySans.ttf",50)
        self.text_surface = self.text_font.render(str(text), True, color)
        self.text_rect = self.text_surface.get_rect(center=pos)
    def render(self):
        game.screen.blit(self.text_surface, self.text_rect)

class Tileset:
    def __init__(self, file, size=(16, 16), margin=0, spacing=0, scale=1):
        self.scale = scale
        self.file = file
        self.size = tuple([scale*x for x in size])
        self.margin = margin
        self.spacing = spacing
        self.image = pygame.image.load(file).convert_alpha()
        resolution = self.image.get_size()
        resolution = tuple([scale*x for x in resolution])
        print(resolution)
        self.image = pygame.transform.scale(self.image,resolution)
        self.rect = self.image.get_rect()
        self.tiles = []
        self.load()


    def load(self):
        self.tiles = []
        x0 = y0 = self.margin
        w, h = self.rect.size
        dx = self.size[0] + self.spacing
        dy = self.size[1] + self.spacing
        
        for y in range(y0, h, dy):
            for x in range(x0, w, dx):
                tile = pygame.Surface(self.size).convert_alpha()
                tile.fill((0,0,0,0))
                tile.blit(self.image, (0, 0), (x, y, *self.size))
                self.tiles.append(tile)

    def __str__(self):
        return f'{self.__class__.__name__} file:{self.file} tile:{self.size}'

class Tilemap:
    def __init__(self, tileset, size=(50, 50), rect=None):
        self.size = size
        self.tileset = tileset
        # self.scale = self.tileset.scale
        self.resolution = self.tileset.size[0]
        # print(self.resolution)
        self.map = np.zeros(size, dtype=int)

        h, w = self.size
        self.image = pygame.Surface((self.resolution*w, self.resolution*h)).convert_alpha()
        self.image.fill((0,0,0,0))
        # self.image.set_alpha(50)
        if rect:
            self.rect = pygame.Rect(rect)
        else:
            self.rect = self.image.get_rect()

    def render(self):
        m, n = self.map.shape
        for j in range(m):
            for i in range(n):
                # print(i,j,self.map[j,i])
                if self.map[j,i] != -1:
                    tile = self.tileset.tiles[self.map[j, i]].convert_alpha()
                    self.image.blit(tile, (i*self.resolution, j*self.resolution))
                # else:
                    # tile = self.tileset.tiles[183]
                    # self.image.blit(tile, (i*16, j*16))
                    

    def set_zero(self):
        self.map = np.zeros(self.size, dtype=int)
        print(self.map)
        print(self.map.shape)
        self.render()

    def set_random(self):
        n = len(self.tileset.tiles)
        self.map = np.random.randint(n, size=self.size)
        print(self.map)
        self.render()

    def set(self, data):
        self.map = data
        # print(self.map.shape)
        # print(self.map)
        self.render()

    def __str__(self):
        return f'{self.__class__.__name__} {self.size}'

class Player(pygame.sprite.Sprite):
    def __init__(self,resolution = 16, scale = 1):
        super().__init__()
        self.resolution = resolution*scale
        self.scale = scale
        self.image = pygame.image.load('dinosaur.png')
        self.image = pygame.transform.scale(self.image,(self.resolution-1,self.resolution-1))
        self.rect = self.image.get_rect(midbottom = (100,100))
        self.gravity = 0
        self.safespace = 2
        self.dimention = tuple([self.resolution*x for x in data.shape])
        self.key = []
        self.check_point = (100,170)
        self.dx, self.dy = 0,0

        # self.dimention
    def player_input(self):
        self.key = pygame.key.get_pressed()
        self.dx = 0
        if (self.key[PDOWN] ):
            self.gravity += 0.5*SCALE
        if (self.key[PLEFT]):
            self.dx = -2*SCALE
            # self.rect.left -= 2
        if (self.key[PRIGHT]):
            self.dx = 2*SCALE
            # self.rect.right += 2
    def aply_gravity(self):
        self.rect.bottom += self.roundg

    def map_input(self):
        self.player = {
            "bottom": self.rect.bottom+game.cam[1], 
            "top": self.rect.top+game.cam[1], 
            "centerx" : self.rect.centerx - game.cam[0],
            "left": self.rect.left-game.cam[0], 
            "right": self.rect.right-game.cam[0]}
        self.roundg = int(self.gravity)
        self.type = {
            "gbottomleft" : tilem.map[(self.player["bottom"] + self.roundg)//self.resolution , (self.player["left"] + self.safespace)//self.resolution],
            "gbottomright" : tilem.map[(self.player["bottom"] + self.roundg)//self.resolution , (self.player["right"] - self.safespace)//self.resolution],
            "gtopleft" : tilem.map[(self.player["top"] + self.roundg)//self.resolution , (self.player["left"] + self.safespace)//self.resolution],
            "gtopright" : tilem.map[(self.player["top"] + self.roundg)//self.resolution , (self.player["right"] - self.safespace)//self.resolution],
            "gtopmid" : tilem.map[(self.player["top"] + self.roundg)//self.resolution , (self.player["right"])//self.resolution],
            "mbottomleft" : tilem.map[(self.player["bottom"] - self.safespace)//self.resolution , (self.player["left"] + self.dx)//self.resolution],
            "mbottomright" : tilem.map[(self.player["bottom"] - self.safespace)//self.resolution , (self.player["right"] + self.dx)//self.resolution],
            "mtopleft" : tilem.map[(self.player["top"] + self.safespace)//self.resolution , (self.player["left"] + self.dx)//self.resolution],
            "mtopright" : tilem.map[(self.player["top"] + self.safespace)//self.resolution , (self.player["right"] + self.dx)//self.resolution],
        }
    def check_border(self):
        self.help_borders = [[43,60],[86,103],[233,252]]
        self.borders = {
            "up": [i for i in range(self.help_borders[0][0],self.help_borders[0][1])],
            "down": [i for i in range(self.help_borders[0][0],self.help_borders[0][1])],
            "left": [i for i in range(self.help_borders[0][0],self.help_borders[0][1])],
            "right": [i for i in range(self.help_borders[0][0],self.help_borders[0][1])],
        }
        for x in self.help_borders[1:]:
            for i in range(x[0],x[1]):
                self.borders["up"].append(i)
                self.borders["down"].append(i)
                self.borders["left"].append(i)
                self.borders["right"].append(i)
        
        if self.rect.top < 0:
            self.rect.top = 0
            self.gravity = 0
        elif self.rect.left < 0:
            self.rect.left = 0
            self.gravity = 0
        elif self.rect.bottom > self.dimention[0]-1:
            self.rect.bottom = self.dimention[0]-1
        elif self.rect.right > self.dimention[1]-1:
            self.rect.right = self.dimention[1]-1

        self.map_input()
        
        
        if self.type["gbottomleft"] in self.borders["down"] or self.type["gbottomright"] in self.borders["down"]:
            if (self.key[PUP] or self.key[SPACE]) :
                self.gravity = -4*SCALE
            else:
                # self.rect.bottom = self.rect.bottom//16 *16
                self.gravity -= 1
        elif self.type["gtopleft"] in self.borders["up"] or self.type["gtopright"] in self.borders["up"]:
            self.gravity += 2*SCALE
            # print("xx")
            # for i in ["gtopleft","gtopright"]:
            test = [i for i in range(self.player["left"],self.player["right"])]
            print(test)
            # if 234 in test:

            for i in test:
                if tilem.map[(self.player["top"] + self.roundg)//self.resolution , i//self.resolution] == 234:
            # if self.type["gtopmid"] == 234:
                # print("yy")
                # if i == "gtopright":
                #     tilem.map[(self.player["top"] + self.roundg)//self.resolution , (self.player["right"] + self.safespace)//self.resolution] = 0
                # else:
                    tilem.map[(self.player["top"] + self.roundg)//self.resolution , i//self.resolution] = 46
                    tilem.render()
                    pos = [i, self.rect.top-self.resolution]
                    obstacle_group.add(Obstacle(pos,tiles.tiles[276]))



        elif 108 in self.type.values():
            self.dead()
        else:
            self.gravity += 0.15*self.scale
            self.aply_gravity()

        if self.type["mbottomleft"] in self.borders["left"] or self.type["mtopleft"] in self.borders["left"]:
            # self.rect.right = self.rect.right//16 *16 + 16
            self.dx = -1*self.scale
            self.map_input()
            if self.type["mbottomleft"] in self.borders["left"] or self.type["mtopleft"] in self.borders["left"]:
                self.dx = 0
            
        elif self.type["mbottomright"] in self.borders["right"] or self.type["mtopright"] in self.borders["right"]:
            # self.rect.left = self.rect.left//16 *16 -1
            self.dx = 1
            self.map_input()
            if self.type["mbottomright"] in self.borders["right"] or self.type["mtopright"] in self.borders["right"]:
                self.dx = 0

        self.rect.x += self.dx
    def dead(self):
        game.cam[0] = 0
        self.rect.bottomleft = self.check_point

    def check_camera(self):
        x = int(pygame.display.get_window_size()[0]/3)
        shiftleft = self.rect.centerx - x*2
        shiftright = x - self.rect.centerx
        # print(shiftleft,shiftright,game.cam[0],self.rect.centerx)
        if shiftleft > 0:
            game.cam[0] -= shiftleft
            self.rect.centerx = x*2
        if shiftright > 0 and game.cam[0]<0:
            game.cam[0] += shiftright
            self.rect.centerx = x



        

    def update(self):
        # self.position.render()
        # print(self.rect.center)
        self.player_input()
        self.check_border()
        self.check_camera()

class Enemy(pygame.sprite.Sprite):
    def __init__(self,pos,type,tileset,size):
        super().__init__()
        # self.tileset = tileset
        # i,j = pos
        # tile = self.tileset.tiles[pos]
        # self.image.blit(tile, (i*16, j*16))
        # self.image = pygame.image.load("kaktus.png").convert_alpha()
        self.scale = SCALE
        self.life = True
        # self.pos = pos
        self.size = size
        dimention = {
            "player" : [2,2]
        }
        self.tileset = tileset
        self.gravity = 0
        self.safespace = 2
        self.presolution = self.tileset.size[0]
        self.resolution = RESOLUTION*SCALE
        self.dimention = tuple([self.resolution*x for x in data.shape])
        self.key = []
        self.dx, self.dy = 0,0
        self.check_point = (100,170)
        # self.scale = self.tileset.scale
        # print(self.resolution)
        self.map = np.zeros(size, dtype=int)
        self.character = type
        self.status = 2
        self.size = 8*SCALE
        self.fps = 4
        self.frame = FPS//self.fps
        self.count = 0
        self.direct = [1,2]
        # self.enemy()
        # print("haha")
        # self.borec = Tilemap(tileset,size,)
        # self.data = 
        # self.borec.set(enemy_pos)
        # self.rect = self.borec.rect
        # self.image = self.borec.image
        h, w = size
        self.image = pygame.Surface((self.presolution*w, self.presolution*h)).convert_alpha()
        self.image.fill((0,0,0,100))
        self.rect = self.image.get_rect(midbottom = pos)
        self.style = {
            1 : { 1 : [[108,109],[162,163]], 2 : [[110,111],[164,165]] , 0 : [[1572,1572],[166,167]]},
            "player" : { 1 : [[108,109],[162,163]], 2 : [[110,111],[164,165]] , 0 : [[166,167]], },
        }
        self.status = 1

        # self.image = pygame.transform.scale(self.image,(size, size))
        self.cam = game.cam[:]
        # self.rect = self.image.get_rect(bottomleft = (pos))
        # self.speed  = 4
    # def enemy(self):
        # if self.type == 1:
        #     self.image = pygame.Surface((self.size * 2, self.size * 3)).convert_alpha()
        #     for j in range(3):
        #         for i in range(2):
        #             # print(i,j,self.map[j,i])
        #             if self.map[j,i] != -1:
        #                 tile = self.tileset.tiles[self.map[j, i]].convert_alpha()
        #                 self.image.blit(tile, (i*self.resolution, j*self.resolution))

    def update(self):
        if self.character == "player":
            self.player_input()
        else:
            self.dx = self.direct[0] * self.direct[1]
        # self.player_input()
        if self.status != 0:
            self.check_border()
            if player.sprite.life:
                self.destroy()
            self.map_input()
        else: self.aply_gravity()
        self.render()
        self.check_pos()

    def aply_gravity(self):
        self.rect.bottom += self.roundg

    def player_input(self):
        self.key = pygame.key.get_pressed()
        self.dx = 0
        if (self.key[PDOWN] ):
            self.gravity += 0.5*SCALE
        if (self.key[PLEFT]):
            self.dx = -2*SCALE
            # self.rect.left -= 2
        if (self.key[PRIGHT]):
            self.dx = 2*SCALE
            # self.rect.right += 2
    def render(self):
        # m, n = self.map.shape
        # m = len(self.style[1][self.status])
        # n = len(self.style[1][self.status][0])

        self.image.fill((0,0,0,0))
        x,y = 0,0
        # print(self.rect.topleft)
        if self.status >= 0:
            for j in self.style[self.character][self.status]:
                x = 0
                for i in j:
                    # print(i,j,self.map[j,i])
                    # if self.map[j,i] != -1:
                    tile = self.tileset.tiles[i].convert_alpha()
                    self.image.blit(tile, (x*self.presolution, y*self.presolution))
                    x+= 1
                y+= 1
            if self.status > 0:
                if self.count > self.frame:
                    self.count = 0
                    if self.status == len(self.style[self.character])-1:
                        self.status = 1
                    else: self.status += 1
            else:
                if self.count > 20:
                    if self.character != "player":
                        self.kill()
                    else:
                        self.status = -1
        game.screen.blit(self.image,(self.rect.left+self.cam[0],self.rect.top+self.cam[1]))
        self.count += 1

    def check_pos(self):
        # print(game.cam,self.cam)
        if game.cam != self.cam:
            self.rect.x -= -game.cam[0] + self.cam[0] 
            # print(self.rect.x)
            self.cam = game.cam[:]
         
    def map_input(self):
        self.player = {
            "bottom": self.rect.bottom+game.cam[1], 
            "top": self.rect.top+game.cam[1], 
            "centerx" : self.rect.centerx - game.cam[0],
            "left": self.rect.left-game.cam[0], 
            "right": self.rect.right-game.cam[0]}
        self.roundg = int(self.gravity)
        self.type = {
            "gbottomleft" : tilem.map[(self.player["bottom"] + self.roundg)//self.resolution , (self.player["left"] + self.safespace)//self.resolution],
            "gbottomright" : tilem.map[(self.player["bottom"] + self.roundg)//self.resolution , (self.player["right"] - self.safespace)//self.resolution],
            "gtopleft" : tilem.map[(self.player["top"] + self.roundg)//self.resolution , (self.player["left"] + self.safespace)//self.resolution],
            "gtopright" : tilem.map[(self.player["top"] + self.roundg)//self.resolution , (self.player["right"] - self.safespace)//self.resolution],
            "gtopmid" : tilem.map[(self.player["top"] + self.roundg)//self.resolution , (self.player["right"])//self.resolution],
            "mbottomleft" : tilem.map[(self.player["bottom"] - self.safespace)//self.resolution , (self.player["left"] + self.dx)//self.resolution],
            "mbottomright" : tilem.map[(self.player["bottom"] - self.safespace)//self.resolution , (self.player["right"] + self.dx)//self.resolution],
            "mtopleft" : tilem.map[(self.player["top"] + self.safespace)//self.resolution , (self.player["left"] + self.dx)//self.resolution],
            "mtopright" : tilem.map[(self.player["top"] + self.safespace)//self.resolution , (self.player["right"] + self.dx)//self.resolution],
        }

    def check_border(self):
        self.help_borders = [[43,60],[86,103],[233,252]]
        self.borders = {
            "up": [i for i in range(self.help_borders[0][0],self.help_borders[0][1])],
            "down": [i for i in range(self.help_borders[0][0],self.help_borders[0][1])],
            "left": [i for i in range(self.help_borders[0][0],self.help_borders[0][1])],
            "right": [i for i in range(self.help_borders[0][0],self.help_borders[0][1])],
        }
        for x in self.help_borders[1:]:
            for i in range(x[0],x[1]):
                self.borders["up"].append(i)
                self.borders["down"].append(i)
                self.borders["left"].append(i)
                self.borders["right"].append(i)
        
        if self.rect.top < 0:
            self.rect.top = 0
            self.gravity = 0
        elif self.rect.left < 0:
            self.rect.left = 0
            self.gravity = 0
        # elif self.rect.bottom > self.dimention[0]-1:
        #     self.rect.bottom = self.dimention[0]-1
        # elif self.rect.right > self.dimention[1]-1:
        #     self.rect.right = self.dimention[1]-1

        self.map_input()
        # print(self.rect)
        
        
        # print ([(self.player["bottom"] + self.roundg)//self.resolution , (self.player["right"] - self.safespace)//self.resolution])

        if self.type["gbottomleft"] in self.borders["down"] or self.type["gbottomright"] in self.borders["down"]:
            # print ([(self.player["bottom"] + self.roundg)//self.resolution , (self.player["right"] - self.safespace)//self.resolution])
            # print(self.resolution)

            if self.character == "player" and (self.key[PUP] or self.key[SPACE]) :
                self.gravity = -4*SCALE
            else:
                # self.rect.bottom = self.rect.bottom//16 *16
                self.gravity -= 1
                pass
        elif self.type["gtopleft"] in self.borders["up"] or self.type["gtopright"] in self.borders["up"]:
            self.gravity += 2*SCALE
            # print("xx")
            # for i in ["gtopleft","gtopright"]:
            test = [i for i in range(self.player["left"],self.player["right"])]
            # print(test)
            # if 234 in test:

            for i in test:
                # print(tilem.map[(self.player["top"] + self.roundg)//self.resolution , i//self.resolution])
                if tilem.map[(self.player["top"] + self.roundg)//self.resolution , i//self.resolution] == 234:
            # if self.type["gtopmid"] == 234:
                # print("yy")
                # if i == "gtopright":
                #     tilem.map[(self.player["top"] + self.roundg)//self.resolution , (self.player["right"] + self.safespace)//self.resolution] = 0
                # else:
                    tilem.map[(self.player["top"] + self.roundg)//self.resolution , i//self.resolution] = 46
                    tilem.render()
                    pos = [i, self.rect.top-self.resolution]
                    obstacle_group.add(Obstacle(pos,tiles.tiles[276]))



        elif 108 in self.type.values():
            self.dead()
        else:
            self.gravity += 0.15*self.scale
            self.aply_gravity()

        if self.type["mbottomleft"] in self.borders["left"] or self.type["mtopleft"] in self.borders["left"]:
            # self.rect.right = self.rect.right//16 *16 + 16
            self.direct[1] = 1
            self.dx = -1*self.scale
            self.map_input()
            if self.type["mbottomleft"] in self.borders["left"] or self.type["mtopleft"] in self.borders["left"]:
                self.dx = 0
            
        elif self.type["mbottomright"] in self.borders["right"] or self.type["mtopright"] in self.borders["right"]:
            # self.rect.left = self.rect.left//16 *16 -1
            self.direct[1] = -1
            self.dx = 1*self.scale
            self.map_input()
            if self.type["mbottomright"] in self.borders["right"] or self.type["mtopright"] in self.borders["right"]:
                self.dx = 0

        self.rect.x += self.dx


    def check_camera(self):
        x = int(pygame.display.get_window_size()[0]/3)
        shiftleft = self.rect.centerx - x*2
        shiftright = x - self.rect.centerx
        # print(shiftleft,shiftright,game.cam[0],self.rect.centerx)
        if shiftleft > 0:
            game.cam[0] -= shiftleft
            self.rect.centerx = x*2
        if shiftright > 0 and game.cam[0]<0:
            game.cam[0] += shiftright
            self.rect.centerx = x

    def destroy(self):
        print(player.sprite.life)
        if player.sprite.gravity > 3 and self.character != "player":
            if pygame.sprite.spritecollide(player.sprite, enemy_group, False): # False na konci určuje, zda-li má kolidující obstacle zabít
                print("xx")
                self.status = 0
                self.count = 0
                self.gravity = 11
                # self.kill()
                # pygame.time.set_timer(self.kill(),3000)
        elif self.character == "player" and self.gravity < 3:
            if pygame.sprite.spritecollide(player.sprite, enemy_group, False): # False na konci určuje, zda-li má kolidující obstacle zabít
                print("player")
                print(self.gravity)
                self.status = 0
                self.count = 0
                self.gravity = 7
                self.life = False

    def dead(self):
        game.cam[0] = 0
        self.rect.bottomleft = self.check_point


class Obstacle(pygame.sprite.Sprite):
    def __init__(self,pos,image):
        super().__init__()
        print("start")
        # self.tileset = tileset
        # i,j = pos
        # tile = self.tileset.tiles[pos]
        # self.image.blit(tile, (i*16, j*16))
        # self.image = pygame.image.load("kaktus.png").convert_alpha()
        self.image = image
        size = 32
        self.image = pygame.transform.scale(self.image,(size, size))
        self.cam = game.cam[:]
        self.rect = self.image.get_rect(bottomleft = (pos))
        # self.speed  = 4

    def update(self):
        self.check_pos()
        self.destroy()
    
    def check_pos(self):
        # print(game.cam,self.cam)
        if game.cam != self.cam:
            self.rect.x -= -game.cam[0] + self.cam[0] 
            # print(self.rect.x)
            self.cam = game.cam[:]
         


    def destroy(self):
        if pygame.sprite.spritecollide(player.sprite, obstacle_group, True): # False na konci určuje, zda-li má kolidující obstacle zabít
            print("xx")
            # self.kill()

def round(pos,round_number):
    if type(pos) == tuple:
        print("t")
    if type(pos) == int:
        pos = pos//round_number*round_number
        print(pos)
        return pos

player = pygame.sprite.GroupSingle()
player.add(Player(RESOLUTION,SCALE))
game = Game()
tiles = Tileset(file,scale = SCALE)
tilem = Tilemap(tiles,data.shape)
tilem.set(data)
score = Text(game.score,(0,0,0),(20,20))
enemy_set = Tileset(file_enemy,(8,8),scale = SCALE)
player.add(Enemy((100,100),"player",enemy_set,(2,2)))

background = Tilemap(tiles,bg_set.shape)
background.set(bg_set)

obstacle_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
# game.render(background.image)
# game.render(tilem.image)
enemy_group.add(Enemy((round(220,RESOLUTION),200),1,enemy_set,(2,2)))
enemy_group.add(Enemy((round(260,RESOLUTION),200),1,enemy_set,(2,2)))
# game.screen.blit(tilem.image,(0,0))
# pygame.display.update()
# tilem.render()
game.run()

