import pygame
from pygame.locals import *
import numpy as np

file = 'images/world_tileset.png'

data = np.loadtxt('data.csv', delimiter=',')
data = np.int_(data)
print(data)

PUP     = pygame.K_w    #pohyb hráče nahoru
PDOWN   = pygame.K_s    #pohyb hráče dolu
PLEFT   = pygame.K_a    #pohyb hráče doleva
PRIGHT  = pygame.K_d    #pohyb hráče doprava
SPACE   = pygame.K_SPACE    #zoom kamery oddálení

FPS = 45
Life = 3

clock = pygame.time.Clock()

class Game:
    W = 1280
    H = 480
    SIZE = W, H

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(Game.SIZE)
        pygame.display.set_caption("Pygame Tiled Demo")
        self.running = True

    def run(self):
        while self.running:

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False

                elif event.type == KEYDOWN:
                    if event.key == K_l:
                        tilem.set_random()

                                        
                        # self.load_image(file)
            game.render(tilem.image)
            player.draw(self.screen)
            player.update()

            pygame.display.update()
            clock.tick(FPS)

        pygame.quit()
    def render(self,image):
        self.screen.blit(image,(0,0))

    def load_image(self, file):
        self.file = file
        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect()

        self.screen = pygame.display.set_mode(self.rect.size)
        pygame.display.set_caption(f'size:{self.rect.size}')
        self.screen.blit(self.image, self.rect)
        pygame.display.update()

class Tileset:
    def __init__(self, file, size=(16, 16), margin=0, spacing=0):
        self.file = file
        self.size = size
        self.margin = margin
        self.spacing = spacing
        self.image = pygame.image.load(file)
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
                tile = pygame.Surface(self.size)
                tile.blit(self.image, (0, 0), (x, y, *self.size))
                self.tiles.append(tile)

    def __str__(self):
        return f'{self.__class__.__name__} file:{self.file} tile:{self.size}'

class Tilemap:
    def __init__(self, tileset, size=(50, 50), rect=None):
        self.size = size
        self.tileset = tileset
        self.map = np.zeros(size, dtype=int)

        h, w = self.size
        self.image = pygame.Surface((16*w, 16*h))
        if rect:
            self.rect = pygame.Rect(rect)
        else:
            self.rect = self.image.get_rect()

    def render(self):
        m, n = self.map.shape
        for j in range(m):
            for i in range(n):
                print(i,j,self.map[j,i])
                tile = self.tileset.tiles[self.map[j, i]]
                self.image.blit(tile, (i*16, j*16))

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
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('dinosaur.png')
        self.image = pygame.transform.scale(self.image,(16,16))
        self.rect = self.image.get_rect(midbottom = (100,100))
        self.gravity = 0
        self.dimention = tuple([16*x for x in data.shape])
        self.key = []
        self.check_point = (100,200)
        self.dx, self.dy = 0,0

        # self.dimention
    def player_input(self):
        self.key = pygame.key.get_pressed()
        # if (self.key[PUP] or self.key[SPACE]) :
        #     self.gravity = -1
        if (self.key[PDOWN] ):
            self.gravity += 0.5
        if (self.key[PLEFT]):
            self.rect.left -= 2
        if (self.key[PRIGHT]):
            self.rect.right += 2
    def aply_gravity(self):
        self.rect.bottom += self.gravity
    #     if (self.rect.bottom >= 0.9*SCREEN_HEIGHT) and self.gravity > 0:
    #         self.gravity = 0 
    #         # class Player(pygame.sprite.Sprite):
    #         # class Player(pygame.sprite.Sprite):
    #         self.rect.bottom = round(0.9*SCREEN_HEIGHT)
    #     else:
    #         self.gravity += 1
    #     self.rect.bottom += self.gravity
    #     # print(hrac_ctverec.bottom)

    def map_input(self):
        self.type = [
            tilem.map[(self.rect.bottom)//16 , (self.rect.left + 2)//16],
            tilem.map[(self.rect.bottom)//16 , (self.rect.right - 2)//16],
            tilem.map[self.rect.top//16 , (self.rect.left + 2)//16],
            tilem.map[self.rect.top//16 , (self.rect.right - 2)//16],
            tilem.map[(self.rect.bottom - 2)//16 , (self.rect.left)//16],
            tilem.map[(self.rect.bottom - 2)//16 , (self.rect.right)//16],
            tilem.map[(self.rect.top + 2)//16 , (self.rect.left)//16],
            tilem.map[(self.rect.top + 2)//16 , (self.rect.right)//16],
        ]
    def check_border(self):
        # print(data.shape[0])
        # print(tilem.size)
        # print(self.rect.bottomright)
        # self.dimention = data.shape
        
        # if self.rect.top
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.bottom > self.dimention[0]-1:
            self.rect.bottom = self.dimention[0]-1
        elif self.rect.right > self.dimention[1]-1:
            self.rect.right = self.dimention[1]-1

        self.map_input()
        
        if self.type[0] in [0,1,32] or self.type[1] in [0,1,32]:
            # print("dd")
            if (self.key[PUP] or self.key[SPACE]) :
                self.gravity = -4
            else:
                self.rect.bottom = self.rect.bottom//16 *16
                self.gravity = 0
        elif self.type[0] in [0,1,32] or self.type[1] in [0,1,32]:
                self.rect.top = self.rect.top//16 *16 +16
                self.gravity = 0
        elif 33 in self.type:
            self.rect.bottomleft = self.check_point
        elif 32 in self.type[6:7]:
            print("hds")
        else:
            self.gravity += 0.12

        self.map_input()
            
        if self.type[4] in [0,1] or self.type[6] in [0,1]:
            self.rect.right = self.rect.right//16 *16 + 16
        elif self.type[5] in [0,1] or self.type[7] in [0,1]:
            self.rect.left = self.rect.left//16 *16 -1
            
        # if pygame.sprite.spritecollide(player.sprite, , False): # False na konci určuje, zda-li má kolidující obstacle zabít




    def update(self):
        self.player_input()
        self.check_border()
        self.aply_gravity()



class Obstacle(pygame.sprite.Sprite):
     def __init__(self,pos,tileset):
        super().__init__()
        self.tileset = tileset
        i,j = pos
        tile = self.tileset.tiles[pos]
        self.image.blit(tile, (i*16, j*16))
        self.image = pygame.image.load("kaktus.png").convert_alpha()
        size = 16
        self.image = pygame.transform.scale(self.image,(size, size))
        self.rect = self.image.get_rect(bottomleft = (pos))
        self.speed  = 4

player = pygame.sprite.GroupSingle()
player.add(Player())
game = Game()
tiles = Tileset(file)
tilem = Tilemap(tiles,data.shape)
tilem.set(data)
game.render(tilem.image)
# game.screen.blit(tilem.image,(0,0))
# pygame.display.update()
# tilem.render()
game.run()

