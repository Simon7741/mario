import pygame
from pygame.locals import *
import numpy as np
from pygame.transform import scale

file = 'images/sky.png'

data = np.loadtxt('normal.csv', delimiter=';')
data = np.int_(data)
print(data)

PUP     = pygame.K_w    #pohyb hráče nahoru
PDOWN   = pygame.K_s    #pohyb hráče dolu
PLEFT   = pygame.K_a    #pohyb hráče doleva
PRIGHT  = pygame.K_d    #pohyb hráče doprava
SPACE   = pygame.K_SPACE    #zoom kamery oddálení

FPS = 45
Life = 1
SCALE = 1
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
                        pygame.image.save(self.screen,"screen_sky.png")
                                        
                        # self.load_image(file)
            game.render(tilem.image)

            pygame.display.update()
            clock.tick(FPS)

        pygame.quit()

    # def rscore(self):
    #     pass


    def render(self,image):
        self.screen.blit(image,(self.cam[0],self.cam[1]))

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
    def __init__(self, file, size=(16, 16), margin=0, spacing=1, scale=1):
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


game = Game()
tiles = Tileset(file,scale = SCALE)
tilem = Tilemap(tiles,data.shape)
tilem.set(data)

game.render(tilem.image)
# game.screen.blit(tilem.image,(0,0))
# pygame.display.update()
# tilem.render()
game.run()

