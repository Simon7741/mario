import pygame 
import time
import pygame.font
from pygame.math import clamp

pygame.init()

# SCREEN_WIDHT = 1920
# SCREEN_HEIGHT = 1080
SCREEN_WIDHT = 960
SCREEN_HEIGHT = 540

FPS = 45
Life = 3

PUP     = pygame.K_w    #pohyb hráče nahoru
PDOWN   = pygame.K_s    #pohyb hráče dolu
PLEFT   = pygame.K_a    #pohyb hráče doleva
PRIGHT  = pygame.K_d    #pohyb hráče doprava
SPACE   = pygame.K_SPACE    #zoom kamery oddálení

screen = pygame.display.set_mode((SCREEN_WIDHT,SCREEN_HEIGHT))

run = True

clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('dinosaur.png')
        self.image = pygame.transform.scale(self.image,(100,100))
        self.rect = self.image.get_rect(midbottom = (100,0.9*SCREEN_HEIGHT))
        self.gravity = 0
    def player_input(self):
        key = pygame.key.get_pressed()
        if (key[PUP] or key[SPACE]) and self.rect.bottom >= 0.9*SCREEN_HEIGHT:
            self.gravity = -20
    def aply_gravity(self):
        if (self.rect.bottom >= 0.9*SCREEN_HEIGHT) and self.gravity > 0:
            self.gravity = 0 
            # class Player(pygame.sprite.Sprite):
            # class Player(pygame.sprite.Sprite):
            self.rect.bottom = round(0.9*SCREEN_HEIGHT)
        else:
            self.gravity += 1
        self.rect.bottom += self.gravity
        # print(hrac_ctverec.bottom)
    def update(self):
        self.player_input()
        self.aply_gravity()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # self.image = pygame.image.load('dinosaur.png')
        # size = random.randint(30,80)
        # self.image = pygame.transform.scale(self.image,(size, size))
        self.image = pygame.Surface((50,50))
        self.image.fill("black")
        self.rect = self.image.get_rect(midbottom = (300,50))
        # self.rect = self.image.get_rect(midbottom = (100,0.9*SCREEN_HEIGHT))
        self.speed  = 4
        self.direction = 1

    def update(self,x):
        self.move()
        self.destroy()

    def move(self):


    def destroy(self):
        if self.rect.x <= -100: 
            self.kill()

    # def update(self):
    #     pass
        # self.rect.bottom += 40;
    # def pos(self,x,y):
    #     self.rect.bottom += x;


player = pygame.sprite.GroupSingle()
player.add(Player())
sky_surface = pygame.Surface((SCREEN_WIDHT,SCREEN_HEIGHT))
sky_surface.fill("lightblue")
obstacle_group = pygame.sprite.Group()
# obstacle_group = pygame.sprite
obstacle_group.add(Obstacle())

while True:
    screen.blit(sky_surface,(0,0))
    if run:
        # Score += 1

        # screen.blit(bottom,(0,SCREEN_HEIGHT*0.9))
        # font = pygame.font.Font(None, int(SCREEN_HEIGHT/10))
        # text = font.render(str(Score), True, (0,0,0))
        # text_rect = text.get_rect(topleft=(0,0))
        # screen.blit(text, text_rect)
        
        

        # if kaktus_ctverec.left < 0: kaktus_ctverec.left = SCREEN_WIDHT
        # screen.blit(kaktus,kaktus_ctverec)
        # kaktus_ctverec.left -= 10

        # if hrac_ctverec.colliderect(kaktus_ctverec):
        #     run = False
        player.draw(screen)
        player.update()
        # obstacle_group.draw(screen)
        obstacle_group.add(Obstacle())
        obstacle_group.update(40)
        obstacle_group.draw(screen)
        
    # else: 
        # textF = fontF.render(f"Game Over \n {Score}", True, (0,0,0))
        # screen.blit(textF, textF_rect)
        # key = pygame.key.get_pressed()
        # if key[P]:
        #     run = True
        #     kaktus_ctverec.left = SCREEN_WIDHT
        #     Score = 0

    for event in pygame.event.get(): #error is here
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
    pygame.display.update()
    clock.tick(FPS)
