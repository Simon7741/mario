import pygame
from pygame.locals import *
import numpy as np
from pygame.transform import scale

file = 'images/NES - Super Mario Bros - Tileset.png'
file = 'images/map.png'
file_enemy = 'images/NES - Super Mario Bros - Enemies & Bosses.png'
file_player = 'images/NES - Super Mario Bros - Mario & Luigi.png'
file_item = 'images/NES - Super Mario Bros - Items Objects and NPCs.png'

data = np.loadtxt('data/data_data.csv', delimiter=',')
data = np.int_(data)
bg_set = np.loadtxt('data/data_Background.csv', delimiter=',')
bg_set = np.int_(bg_set)
enemy_pos = np.loadtxt('data/data_enemy.csv', delimiter=',')
enemy_pos = np.int_(enemy_pos)
# print(data)

PUP     = pygame.K_w    #pohyb hráče nahoru
PDOWN   = pygame.K_s    #pohyb hráče dolu
PLEFT   = pygame.K_a    #pohyb hráče doleva
PRIGHT  = pygame.K_d    #pohyb hráče doprava
SPACE   = pygame.K_SPACE    #zoom kamery oddálení

SCALE = 4
RESOLUTION = 16

clock = pygame.time.Clock()
pygame.init()

class Game:
    W = 1920
    H = 1080
    SIZE = W, H

    def __init__(self):
        self.fps = 45
        pygame.init()
        # self.screen = pygame.display.set_mode(Game.SIZE,pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode(Game.SIZE)
        # pygame.display.toggle_fullscreen()
        pygame.display.set_caption("'Fake' Mario")
        self.running = True
        self.cam = [0,0]
        self.score = 0
        self.life = 3
        self.texts = [(450,200),(1000,700),[146*RESOLUTION*SCALE,6*RESOLUTION*SCALE],[43*SCALE*RESOLUTION,10*SCALE*RESOLUTION]]
        self.pocet = 0
        self.nevim = 1
        self.timerevent = pygame.USEREVENT + 1


    def run(self):
        while self.running:
            # print(pygame.display.get_window_size())
            RESOLUTION = pygame.display.get_window_size()[1]/15
            # print(clock.get_fps())

            # print(player.sprite.life)
            # print(self.timerevent)
            if player.sprite.life == False:
                pygame.time.set_timer(self.timerevent,5000,1)
                
                # print(enemy_group.sprites())
                # print(ds)

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False

                if event.type == self.timerevent:
                    self.cam = [0,0]
                    enemy_group.empty()
                    data = np.loadtxt('data/data_data.csv', delimiter=',')
                    data = np.int_(data)
                    tilem.set(data)
                    game.score = 0
                    # pygame.time.set_timer(self.timerevent,5000)
            items_group.update()
            game.render(background.image)
            texty[0].render(self.screen, self.texts[0][0] + self.cam[0], self.texts[0][1] + self.cam[1], "justify")
            # texty [1] = pygame.transform.rotate(texty[1],90)
            texty[1].render_rotated(self.screen, self.texts[1][0] + self.cam[0], self.texts[1][1] + self.cam[1], 90, "justify")
            texty[2].render(self.screen, self.texts[2][0] + self.cam[0], self.texts[2][1] + self.cam[1], "justify")
            texty[3].render(self.screen, self.texts[3][0] + self.cam[0], self.texts[3][1] + self.cam[1], "justify")

            game.render(tilem.image)
            # player.draw(self.screen)
            enemy_group.update()
            player.update()
            score.render(f"score: {self.score}")

            pygame.display.update()
            clock.tick(game.fps)

        pygame.quit()

    # def rscore(self):
    #     pass


    def render(self,image):
        self.screen.blit(image,(self.cam[0],self.cam[1]))
        items_group.draw(self.screen)

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
        self.color = color
        self.text_font = pygame.font.Font("font.otf",50)
        self.text_surface = self.text_font.render(str(text), True, color)
        self.text_rect = self.text_surface.get_rect(center=pos)
    def render(self,text):
        self.text_surface = self.text_font.render(str(text), True, self.color)
        game.screen.blit(self.text_surface, self.text_rect)


class MultiLineText:
    def __init__(self, font, color, max_width):
        """
        Inicializuje instanci MultiLineText.

        Argumenty:
            font (pygame.font.Font): Objekt fontu Pygame pro vykreslování textu.
            color (tuple): Barva textu ve formátu RGB (např. (255, 255, 255) pro bílou).
            max_width (int): Maximální šířka bloku textu. Text bude zalomen, aby se vešel.
        """
        self.font = font
        self.color = color
        self.max_width = max_width
        self.lines = []
        self.line_height = self.font.get_linesize()
        self.base_space_width = self.font.size(' ')[0]

    def set_text(self, text):
        """
        Nastaví text pro zobrazení a zalomí ho do řádků.

        Argumenty:
            text (str): Vstupní text, který má být zobrazen.
        """
        self.lines = self._wrap_text(text)

    def _wrap_text(self, text):
        """
        Zalomi text do řádků, aby se vešel do max_width.
        """
        paragraphs = text.replace('\r', '').split('\n')
        all_wrapped_lines = []

        for para in paragraphs:
            if not para.strip():
                all_wrapped_lines.append("")
                continue

            words = para.split(' ')
            current_line_words = []
            current_line_width = 0

            for word in words:
                word_width = self.font.size(word)[0]

                potential_add_width = word_width
                if current_line_words:
                    potential_add_width += self.base_space_width

                if current_line_width + potential_add_width <= self.max_width:
                    current_line_words.append(word)
                    current_line_width += potential_add_width
                else:
                    if not current_line_words: # Slovo samotné je delší než max_width
                        all_wrapped_lines.append(word) # Přidá slovo i když přesahuje
                        current_line_words = []
                        current_line_width = 0
                    else:
                        all_wrapped_lines.append(" ".join(current_line_words))
                        current_line_words = [word]
                        current_line_width = word_width

            if current_line_words:
                all_wrapped_lines.append(" ".join(current_line_words))
        
        return all_wrapped_lines

    def _get_line_actual_width(self, line):
        """
        Vypočítá šířku řádku, pokud by byl vykreslen standardně (s jednou mezerou mezi slovy).
        """
        words = line.split(' ')
        if not words:
            return 0
        
        total_width = 0
        for i, word in enumerate(words):
            total_width += self.font.size(word)[0]
            if i < len(words) - 1: # Přidat šířku mezery pro všechny kromě posledního slova
                total_width += self.base_space_width
        return total_width


    def render(self, surface, x, y, align="left",rotate = 0):
        """
        Vykreslí text na danou plochu.

        Argumenty:
            surface (pygame.Surface): Plocha Pygame, na kterou se má text vykreslit.
            x (int): X-ová souřadnice levého horního rohu bloku textu.
            y (int): Y-ová souřadnice levého horního rohu bloku textu.
            align (str): Zarovnání textu ("left", "center", "right", "justify").
                         "justify" se pokusí zarovnat text do bloku, přidáním mezer mezi slova.
        """
        current_y = y
        for line_index, line in enumerate(self.lines):
            line_surface = None
            
            if not line.strip(): # Pokud je řádek prázdný nebo obsahuje jen mezery
                current_y += self.line_height
                continue

            words_on_line = line.split(' ')
            
            is_last_line_in_list = (line_index == len(self.lines) - 1)
            # Zjišťujeme, zda je to poslední "vizuální" řádek odstavce
            is_last_paragraph_line = is_last_line_in_list
            if not is_last_line_in_list and not self.lines[line_index + 1].strip():
                 is_last_paragraph_line = True
            
            is_single_word_line = (len(words_on_line) == 1)

            # Nová kontrola: Je řádek příliš krátký na to, aby byl justify?
            # Pokud je šířka řádku s normálními mezerami výrazně menší než max_width,
            # NEbudeme ho justify.
            line_actual_width = self._get_line_actual_width(line)
            # Určitá tolerance je zde důležitá, aby se justify neaplikoval na příliš krátké řádky
            is_too_short_for_justify = (line_actual_width < self.max_width * 0.75) # Např. 75% šířky

            if (align == "justify" and
                not is_last_paragraph_line and
                not is_single_word_line and
                not is_too_short_for_justify): # Přidána nová podmínka
                line_surface = self._justify_line(line)
            else:
                line_surface = self.font.render(line, True, self.color)

            if line_surface:
                target_x = x
                if align == "center":
                    target_x = x + (self.max_width - line_surface.get_width()) // 2
                elif align == "right":
                    target_x = x + self.max_width - line_surface.get_width()
                # Pro "left" a "justify" (když justify selže, je to left) je target_x už nastaven na x

                surface.blit(line_surface, (target_x, current_y))
                # print(pygame.time.get_ticks())
            current_y += self.line_height

    def _justify_line(self, line):
        """
        Vytvoří zarovnaný povrch řádku pro zarovnání do bloku.
        """
        words = line.split(' ')
        num_gaps = len(words) - 1

        if num_gaps <= 0:
            return self.font.render(line, True, self.color)

        words_width = sum(self.font.size(word)[0] for word in words)
        current_content_width = words_width + num_gaps * self.base_space_width
        
        extra_space_to_fill = self.max_width - current_content_width

        if extra_space_to_fill <= 0: # Není potřeba přidávat mezery, možná už je plné nebo přeplněné
            return self.font.render(line, True, self.color)

        extra_space_per_gap = extra_space_to_fill // num_gaps
        remaining_extra_space = extra_space_to_fill % num_gaps

        justified_text_surface = pygame.Surface((self.max_width, self.line_height), pygame.SRCALPHA)
        current_x = 0
        for i, word in enumerate(words):
            word_surface = self.font.render(word, True, self.color)
            justified_text_surface.blit(word_surface, (current_x, 0))
            current_x += word_surface.get_width()

            if i < num_gaps:
                gap_width = self.base_space_width + extra_space_per_gap
                if remaining_extra_space > 0:
                    gap_width += 1
                    remaining_extra_space -= 1
                current_x += gap_width
        
        return justified_text_surface

    def render_rotated(self, surface, x, y, angle, align="left"):
        """
        Vykreslí celý textový blok otočený o daný úhel kolem svého středu.

        Argumenty:
            surface (pygame.Surface): Plocha, na kterou se má kreslit.
            x (int): X-ová souřadnice STŘEDU výsledného otočeného bloku.
            y (int): Y-ová souřadnice STŘEDU výsledného otočeného bloku.
            angle (float): Úhel otočení ve stupních.
            align (str): Zarovnání textu uvnitř bloku ("left", "center", "right", "justify").
        """
        # 1. Výpočet rozměrů bloku a vytvoření dočasné plochy
        if not self.lines:
            return # Není co kreslit

        block_height = self.line_height * len(self.lines)
        # Použijeme SRCALPHA pro průhledné pozadí
        text_block_surface = pygame.Surface((self.max_width, block_height), pygame.SRCALPHA)

        # 2. Vykreslení textu na dočasnou plochu pomocí stávající render metody
        # Kreslíme na pozici (0, 0), protože pracujeme v lokálních souřadnicích text_block_surface
        self.render(text_block_surface, 0, 0, align)

        # 3. Otočení celé plochy s textem
        rotated_surface = pygame.transform.rotate(text_block_surface, angle)

        # 4. Získání nového obdélníku a nastavení jeho středu na požadované (x, y)
        rotated_rect = rotated_surface.get_rect(center=(x, y))

        # 5. Vykreslení finálního otočeného povrchu na hlavní obrazovku
        surface.blit(rotated_surface, rotated_rect.topleft)

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
        # print(resolution)
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
        self.character = {
            22 : 1,
            23 : 2,
        }
        self.not_render = [-1,25,26]
        self.player = 24
        if rect:
            self.rect = pygame.Rect(rect)
        else:
            self.rect = self.image.get_rect()

    def render(self):
        m, n = self.map.shape
        # print(self.size)
        # print(m,n)
        # n, m = pygame.display.get_window_size()
        # n, m = (n+game.cam[0])//(RESOLUTION*SCALE), (m+game.cam[0]//(RESOLUTION*SCALE)
        
        # print(m,n)
        for j in range(m):
            for i in range(n):
                # print(i,j,self.map[j,i])


                if self.map[j,i] not in self.not_render:
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
        m, n = self.map.shape
        for j in range(m):
            for i in range(n):
                if self.map[j,i] == self.player:
                    # player.add
                    player.add(Enemy((i*self.resolution,j*self.resolution),"player",player_set))
                    # enemy_group.add(Enemy((i*self.resolution-64,j*self.resolution),"player",enemy_set))
                    self.map[j,i] = -1
                elif self.map[j,i] in self.character:
                    enemy_group.add(Enemy((i*self.resolution,j*self.resolution),self.character[self.map[j,i]],enemy_set))
                    self.map[j,i] = -1

        # print(self.map.shape)
        # print(self.map)
        self.render()

    def __str__(self):
        return f'{self.__class__.__name__} {self.size}'


class Enemy(pygame.sprite.Sprite):
    def __init__(self,pos,type,tileset):
        super().__init__()
        # self.tileset = tileset
        # i,j = pos
        # tile = self.tileset.tiles[pos]
        # self.image.blit(tile, (i*16, j*16))
        # self.image = pygame.image.load("kaktus.png").convert_alpha()
        self.scale = SCALE
        self.life = True
        if type != "player":
            self.life = False
        # self.pos = pos
        dimention = {
            "player" : [2,2],
            1 : [2,2],
            2 : [2,2],
        }
        self.tileset = tileset
        self.gravity = 0
        self.safespace = 2
        self.diametre = dimention[type]
        self.presolution = self.tileset.size[0]
        self.resolution = RESOLUTION*SCALE
        self.dimention = tuple([self.resolution*x for x in data.shape])
        self.key = []
        self.dx, self.dy = 0,0
        # self.scale = self.tileset.scale
        # print(self.resolution)
        self.map = np.zeros(self.diametre, dtype=int)
        self.character = type
        self.size = 8*SCALE
        self.fps = 4
        self.frame = game.fps//self.fps
        self.count = 20
        self.direct = [-1,2]
        self.check_point = pos
        self.rupdate = False
        # self.enemy()
        # print("haha")
        # self.borec = Tilemap(tileset,size,)
        # self.data = 
        # self.borec.set(enemy_pos)
        # self.rect = self.borec.rect
        # self.image = self.borec.image
        h, w = dimention[type]
        self.image = pygame.Surface((self.presolution*w, self.presolution*h)).convert_alpha()
        self.image.fill((0,0,0,0))
        self.rect = self.image.get_rect(topleft = pos)
        self.style = {
            1 : { 1 : [[108,109],[162,163]], 2 : [[110,111],[164,165]] , 0 : [[166,167]], },
            2 : { 1 : [[216,217],[270,271]], 2 : [[218,219],[272,273]] , 0 : [[220,221],[274,275]], },
            "player" : { 1 : [[73,74],[146,147]], 0 : [[85,86],[158,159]]},
        }
        self.image_number = 1
        self.status = 2
        self.last_status = 2
        # print(self.player)
        self.player_image = {
            "stand" : {
                "small" : { 1: [[73,74],[146,147]],},
                "big" : { 1: [[292,293],[365,366],[438,439],[511,512]],},
            },
            "go" : {
                "small" : { 1: [[75,76],[148,149]], 2 : [[77,78],[150,151]], 3 : [[79,80],[152,153]], },
                "big" : { 1: [[294,295],[367,368],[440,441],[513,514]],2: [[296,297],[369,370],[442,443],[515,516]],3: [[298,299],[371,372],[444,445],[517,518]],},
            },
            "dead" : {
                "small" : { 1: [[85,86],[158,159]],},
                "big" : { 1: [[-1,-1],[377,378],[450,451],[523,524]],},
            },
            "jump" : {
                "small" : { 1: [[83,84],[156,157]],},
                "big" : { 1: [[302,303],[375,376],[448,449],[521,522]],},
            },
            "grown" :{
                "small" : {1 : [[803,804],[876,877]], 2 : [[732,733],[805,806],[878,879]], 3 : [[661,662],[734,735],[807,808],[880,881]]},
                "big" : {1 : [[663,664],[736,737],[809,810],[882,883]], 2 : [[665,666],[738,739],[811,812],[884,885]],2 : [[813,814],[886,887]],2 : [[815,816],[888,889]],},
            },
            "crown": {
                "big" :{1: [[304,305],[377,378],[450,451],[523,524]]}

            }
        }
        self.playerstat = ["stand","small"]

        # self.image = pygame.transform.scale(self.image,(size, size))
        self.cam = game.cam[:]
        self.truefalste = False 
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
        print(self)

    def update(self):
        if self.life:
            if self.character == "player":
                self.player_input()
                self.check_camera()
            else:
                self.dx = self.direct[0] * self.direct[1]
                self.check_pos()
                # print(self.status)
            # self.player_input()
            if self.status != 0:
                self.check_border()
                if player.sprite.life:
                    self.destroy()
                self.map_input()
            else: 
                self.gravity += 0.15*self.scale
                self.roundg = int(self.gravity)
                # print(self.gravity)
            self.render()
            self.aply_gravity()
        else:
            if (self.rect.left + game.cam[0] < pygame.display.get_window_size()[0]):
                self.life = True

    def aply_gravity(self):
        self.roundg = int(self.gravity)
        self.rect.bottom += self.roundg

    def player_input(self):
        self.key = pygame.key.get_pressed()
        self.dx = 0
        if (self.key[PDOWN] ):
            self.gravity += 0.5*SCALE
        if (self.key[PLEFT]):
            self.dx = -2*SCALE
            self.direct[0] = 1
            # self.rect.left -= 2
        if (self.key[PRIGHT]):
            self.dx = 2*SCALE
            self.direct[0] = -1
            # self.rect.right += 2
    def render(self):
        # m, n = self.map.shape
        # m = len(self.style[1][self.image_number])
        # n = len(self.style[1][self.image_number][0])

        x,y = 0,0
        # print(self,self.status)
        # print(self.rect.topleft)
        # if self.character == "player":
        #     # print(self.count)
        #     print(self.direct)

        if (self.status != 0 and self.count > self.frame)or self.rupdate == True or self.status != self.last_status:
            self.rupdate = False
            # self.playerstat
            self.image.fill((0,0,0,0))
            if self.character == "player" :
                if self.playerstat[0] == "grown":
                    if self.image_number <= len(self.player_image[self.playerstat[0]][self.playerstat[1]]):
                        self.diametre = (len(self.player_image[self.playerstat[0]][self.playerstat[1]][self.image_number]),len(self.player_image[self.playerstat[0]][self.playerstat[1]][self.image_number][0]))
                        h, w = self.diametre
                        self.image = pygame.Surface((self.presolution*w, self.presolution*h)).convert_alpha()
                        self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
                        self.image.fill((0,0,0,0))
                    else: 
                        if self.playerstat[1] == "small": self.playerstat = ["stand","big"]
                        else: self.playerstat = ["stand","small"]
                    # print(self.diametre,self.playerstat)
                elif self.status == 0:
                    self.playerstat[0] = "dead"
                elif self.playerstat[1] == "big" and self.key[PDOWN]:
                    self.playerstat[0] = "crown"
                elif self.gravity != 0:
                    self.playerstat[0] = "jump"
                elif self.dx != 0:
                    self.playerstat[0] = "go"
                else: self.playerstat[0] = "stand"

                if self.image_number > len(self.player_image[self.playerstat[0]][self.playerstat[1]]):
                    # if self.playerstat == "grown":
                    #     print(self.image_number)
                    self.image_number = 1
                # print(self.player_image[self.playerstat[0]][self.playerstat[1]][self.image_number])
                for j in self.player_image[self.playerstat[0]][self.playerstat[1]][self.image_number]:
                    x = 0
                    for i in j:
                        # print(i,j,self.map[j,i])
                        # if self.map[j,i] != -1:
                        tile = self.tileset.tiles[i].convert_alpha()
                        self.image.blit(tile, (x*self.presolution, y*self.presolution))
                        x+= 1
                    y+= 1
                # if self.image_number == len(self.player_image[self.playerstat[0]][self.playerstat[1]]):
                #
                #     self.image_number = 1
                self.count = 0
                self.image_number += 1
                # print(self.dx)
            else:
                # print(self.count)
                
                # self.count  = 0
                for j in self.style[self.character][self.image_number]:
                    x = 0
                    for i in j:
                        # print(i,j,self.map[j,i])
                        # if self.map[j,i] != -1:
                        tile = self.tileset.tiles[i].convert_alpha()
                        self.image.blit(tile, (x*self.presolution, y*self.presolution))
                        x+= 1
                    y+= 1
                if self.status > 1:
                    self.count = 0
                    # if self.count > self.frame:
                    if self.image_number == len(self.style[self.character])-1:
                        self.image_number = 1
                    else: self.image_number += 1
                elif self.status == 1:
                    self.count = 0
                    self.image_number = 0 
                    pass
                # print(self.dx)
        if self.count > 80: 
            if self.character != "player":
                self.kill()
        if self.direct[0] > 0:
            self.truefalste = True
        elif self.direct[0] < 0:
            self.truefalste = False
            # print(self.direct)
        self.surface_final = pygame.transform.flip(self.image, self.truefalste, False)
        game.screen.blit(self.surface_final,(self.rect.left,self.rect.top))
        # if self.status == 0:    print(self.count)
        self.count += 1
        self.last_status = self.status
            # if self.character != "player":
            #     print(self,self.count)

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
        self.help_borders = [[36,40],[43,45],[54,55],[151,153],[169,171],[185,188],[203,206],[144,150]]
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
        
        # if self.rect.top < 0:
        #     self.rect.top = 0
        #     self.gravity = 0

        if self.character == "player":
            # print(self.rect.top)
            if self.rect.left < 0:
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
            test = [[0],[0]]
            for i in range(0,int(self.gravity),1):
                self.type["gbottomleft"] = tilem.map[(self.player["bottom"] + i)//self.resolution , (self.player["left"] + self.safespace)//self.resolution]
                self.type["gbottomright"] = tilem.map[(self.player["bottom"] + i)//self.resolution , (self.player["right"] - self.safespace)//self.resolution]
                if self.type["gbottomleft"] not in self.borders["down"]:
                    test[0].append(i)
                    
                if self.type["gbottomright"] not in self.borders["down"]:
                    test[1].append(i)
                # pass
            
            # print([max(test[0]),max(test[1])])
            self.gravity = min([max(test[0]),max(test[1])])
            if self.character == "player":
                if self.gravity != self.roundg :
                    self.rupdate = True
            
                # print(self.roundg)

            if self.character == "player" and (self.key[PUP] or self.key[SPACE]) :
                self.gravity = -4.5*SCALE
                self.rupdate = True
            else:
                pass
                # self.rect.bottom = self.rect.bottom//16 *16
        elif self.type["gtopleft"] in self.borders["up"] or self.type["gtopright"] in self.borders["up"]:
            self.gravity += 2*SCALE
            # print("xx")
            # for i in ["gtopleft","gtopright"]:
            test = [i for i in range(self.player["left"]+2,self.player["right"]-2)]
            # print(test)
            # if 234 in test:

            for i in test:
                # print(tilem.map[(self.player["top"] + self.roundg)//self.resolution , i//self.resolution])
                if tilem.map[(self.player["top"] + self.roundg)//self.resolution , i//self.resolution] == 44:
            # if self.type["gtopmid"] == 234:
                # print("yy")
                # if i == "gtopright":
                #     tilem.map[(self.player["top"] + self.roundg)//self.resolution , (self.player["right"] + self.safespace)//self.resolution] = 0
                # else:
                    tilem.map[(self.player["top"] + self.roundg)//self.resolution , i//self.resolution] = 39
                    icon = tilem.map[(self.player["top"] + self.roundg - 2 * self.size)//self.resolution , i//self.resolution]
                    tilem.render()
                    if icon != -1:
                        pos = [round(i,self.size), round(self.rect.top-self.resolution,self.size)]
                        items_group.add(items(pos,tiles.tiles[icon]))
                    else: game.score += 100



        elif 5 in self.type.values():
            # self.dead()
            print("dead")
            self.status = 0
            self.life = False
        else:
            self.gravity += 0.15*self.scale
        # self.aply_gravity()

        # if self.type["mbottomleft"] in self.borders["left"] or self.type["mtopleft"] in self.borders["left"]:
            # self.rect.right = self.rect.right//16 *16 + 16

        test = [i for i in range(self.player["top"]+self.safespace,self.player["bottom"]-self.safespace)]
        # print(test)
        # if 234 in test:

        for i in test:
            # print(tilem.map[(self.player["top"] + self.roundg)//self.resolution , i//self.resolution])
            if tilem.map[(i)//self.resolution , (self.player["left"]+self.dx)//self.resolution] in self.borders["left"]:


                self.direct[0] = 1
                self.dx = -1*self.scale
                self.map_input()
                # if self.type["mbottomleft"] in self.borders["left"] or self.type["mtopleft"] in self.borders["left"]:
                if tilem.map[(i)//self.resolution , (self.player["left"]+self.dx)//self.resolution] in self.borders["left"]:
                    self.dx = 0
            
            if tilem.map[(i)//self.resolution , (self.player["right"]+self.dx)//self.resolution] in self.borders["right"]:
        # elif self.type["mbottomright"] in self.borders["right"] or self.type["mtopright"] in self.borders["right"]:
            # self.rect.left = self.rect.left//16 *16 -1
                self.direct[0] = -1
                self.dx = 1*self.scale
                self.map_input()
                # if self.type["mbottomright"] in self.borders["right"] or self.type["mtopright"] in self.borders["right"]:
                if tilem.map[(i)//self.resolution , (self.player["right"]+self.dx)//self.resolution] in self.borders["right"]:
                    self.dx = 0

        self.rect.x += self.dx


    def check_camera(self):
        x = int(pygame.display.get_window_size()[0]/3)
        shiftleft = self.rect.centerx - x*2
        shiftright = x - self.rect.centerx
        # print(shiftleft,shiftright,game.cam[0],self.rect.centerx)
        # print(self.rect.x)
        if shiftleft > 0:
            game.cam[0] -= shiftleft
            self.rect.centerx = x*2
        if shiftright > 0 and game.cam[0]<0:
            game.cam[0] += shiftright
            self.rect.centerx = x

    def destroy(self):
        # print(player.sprite.life)
        # print(self)
        # print(pygame.sprite.spritecollide(player.sprite, enemy_group, False))
        if -2 >player.sprite.gravity or player.sprite.gravity > 3 and self.character != "player":
            if self in pygame.sprite.spritecollide(player.sprite, enemy_group, False): # False na konci určuje, zda-li má kolidující items zabít
                # print(self)
                if self.character == 2 and self.status == 2 :
                    self.status = 1
                    self.direct[0] = 0
                    # print(self.count)
                elif self.status == 1 and self.count < 3:
                    # print(self.count)
                    # continue
                    return
                    pass
                else:
                    self.gravity = 11
                    self.status = 0
                    
                self.image_number = 0
                print("xx")
                game.score += 100
                self.count = 0
                player.sprite.gravity = -5
                # self.kill()
                # pygame.time.set_timer(self.kill(),3000)
        elif self.character == "player" and -2 < self.gravity < 3:
            if pygame.sprite.spritecollide(player.sprite, enemy_group, False): # False na konci určuje, zda-li má kolidující items zabít
                if self.playerstat[1] == "small":
                    # print("player")
                    self.status = 0
                    self.count = 0
                    self.gravity = -10
                    self.life = False
                    
                    
                else:
                    self.playerstat[0] = "grown"
                    self.image_number = 1

            item =  pygame.sprite.spritecollide(player.sprite, items_group, True)
            for i in item:
                if self.playerstat[1] == "small":
                    self.playerstat[0] = "grown"
                game.score += 1000

                # print(self.playerstat)
                self.image_number = 1

        
        # else:
        #     print(self.status)

    def dead(self):
        if self.character == "player":
            game.cam[0] = 0
            self.rect.bottomleft = self.check_point
            self.status = 2
            self.life = True
        else:
            self.status = 0

    def __str__(self):
        return f'{self.__class__.__name__} {self.character, self.rect.center}'


class items(pygame.sprite.Sprite):
    def __init__(self,pos,image):
        super().__init__()
        print("start")
        self.image = image
        size = RESOLUTION*SCALE
        self.image = pygame.transform.scale(self.image,(size, size))
        self.cam = game.cam[:]
        self.rect = self.image.get_rect(bottomleft = (pos[0] + self.cam[0],pos[1]+ self.cam[1]))
        # self.speed  = 4

    def update(self):
        self.check_pos()
        # self.destroy()
    
    def check_pos(self):
        # print(game.cam,self.cam)
        if game.cam != self.cam:
            self.rect.x -= -game.cam[0] + self.cam[0] 
            # print(self.rect.x)
            self.cam = game.cam[:]
         


    def destroy(self):
        if pygame.sprite.spritecollide(player.sprite, items_group, True): # False na konci určuje, zda-li má kolidující items zabít
            print("xx")
            # game.score += 100:0
            # self.kill()

def round(pos,round_number):
    if type(pos) == tuple:
        print("t")
    if type(pos) == int:
        pos = pos//round_number*round_number
        # print(pos)
        return pos


# player.add(Player(RESOLUTION,SCALE))
text_block_width = 600
long_text1 = """Pokud se vam zda, ze tato hra se podoba Mario Bros, tak je to cista, ale opravdu cistá nahoda, v teto hre budete hrat za postavicku, která ma za cil vysvobodit princeznu(neni zde), tak, ze projdete pres ruzne prekazky, zabijete nekolik monster.
Ve hre se muzete pohybovat pomoci wsad. Dale take muzete v ? sebrat bud houbicku na zvetseni ."""
WHITE = (255, 255, 255)
long_text2 = "Zde spadnete a umrete"
long_text3 = "Jsi v cili muzes to uz ukoncit"
long_text4 = "houbicky"
font = pygame.font.Font("font.otf", 20)
texty = [MultiLineText(font, WHITE, text_block_width) for _ in range(5)]
texty[0].set_text(long_text1)
texty[1].set_text(long_text2)
texty[2].set_text(long_text3)
texty[3].set_text(long_text4)
game = Game()
enemy_set = Tileset(file_enemy,(8,8),scale = SCALE)
player_set = Tileset(file_player,(8,8),scale = SCALE)
enemy_group = pygame.sprite.Group()

player = pygame.sprite.GroupSingle()
tiles = Tileset(file,scale = SCALE)
tilem = Tilemap(tiles,data.shape)
tilem.set(data)
score = Text(game.score,(0,0,0),(20,20))
# player.add(Enemy((100,100),"player",enemy_set,(2,2)))

background = Tilemap(tiles,bg_set.shape)
background.set(bg_set)

items_group = pygame.sprite.Group()
game.run()

