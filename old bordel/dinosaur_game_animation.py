import pygame # klíčová knihovna umožňující vytvářet jednoduše nejen hry
import random
pygame.init() # nutný příkaz hned na začátku pro správnou inicializaci knihovny


class Player(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__() # volá konstruktor třídy Sprite, od které dědíme
        
        self.image = pygame.transform.scale(self.image,(50,50))
        self.image = pygame.image.load("dinosaur.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(50,50))
        self.rect = self.image.get_rect(bottomleft=(100,0.75*window_height))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def update(self):
        self.player_input()
        self.apply_gravity()
        # self.animation_state()

    
class Obstacle(pygame.sprite.Sprite):
     def __init__(self):
        super().__init__()
        self.image = pygame.image.load("kaktus.png").convert_alpha()
        size = random.randint(30,80)
        self.image = pygame.transform.scale(self.image,(size, size))
        self.rect = self.image.get_rect(bottomleft = (600, 0.75*window_height))
        self.speed  = 4
        
     def update(self):
        self.rect.x -= 6
        self.destroy()
        
     def destroy(self):
          if self.rect.x <= -100: 
              self.kill()

def is_collision():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False): # False na konci určuje, zda-li má kolidující obstacle zabít
        obstacle_group.empty()
        return False
    return True


# herní okno
window_width = 800
window_height = 400
screen = pygame.display.set_mode((window_width, window_height))
    # dvojice (w,h) v parametru se nazývá *tuple*
pygame.display.set_caption("Dinosauří hra") # nastavíme do hlavičky okna název hry
# Load and set the window icon
icon = pygame.image.load("dinosaur.png")  # Make sure the image is in the same directory
pygame.display.set_icon(icon)

clock = pygame.time.Clock() # díky hodinám nastavíme frekvenci obnovování herního okna

# přidání objektů (tzv. surface) do scény
sky_surface = pygame.Surface((window_width,0.75*window_height))
sky_surface.fill("darkslategray1")
ground_surface = pygame.Surface((window_width,0.25*window_height))
ground_surface.fill("lightsalmon4")

# text
text_font = pygame.font.Font("PixelifySans.ttf",100)
text_surface = text_font.render("GAME OVER!", True, "Black")
text_rect = text_surface.get_rect(center=(window_width/2, window_height/2))

# Groups
# nepřátelé
obstacle_group = pygame.sprite.Group()

# hráč
player = pygame.sprite.GroupSingle()
player.add(Player())

game_active = is_collision()

counter = 0

# herní smyčka
while True:
    # zjistíme co dělá hráč za akci
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() # zavřeme herní okno
            exit() # úplně opustíme herní smyčku, celý program se ukončí
        if event.type == pygame.KEYDOWN:
            if game_active == False:
                game_active=True


    if game_active:
        # pozadí
        screen.blit(sky_surface,(0,0)) # položíme sky_surface na souřadnice [0,0]
        screen.blit(ground_surface,(0,0.75*window_height)) # položíme ground_surface na souřadnice [0,300] (pod oblohu)

        if counter > 120:
            counter = 0
            obstacle_group.add(Obstacle())
        else:
            counter += 1

        # nepřítel
        obstacle_group.draw(screen)
        obstacle_group.update()

        # hráč
        player.draw(screen)
        player.update()
        
        game_active = is_collision()

    else:
        screen.blit(text_surface, text_rect)



    pygame.display.update() # updatujeme vykreslené okno
    clock.tick(60) # herní smyčka proběhne maximálně 60x za sekundu

