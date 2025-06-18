import pygame
import pygame.font

import pygame

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


    def render(self, surface, x, y, align="left"):
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

pygame.init()
# Nastavení obrazovky
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Multi-line Text Example")

# Barvy
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Font
font = pygame.font.Font("font.otf", 35)

# Vytvoření instance MultiLineText
# Zde nastavíme maximální šířku na 300 pixelů
text_block_width = 300
multi_line_text_left = MultiLineText(font, WHITE, text_block_width)
multi_line_text_center = MultiLineText(font, WHITE, text_block_width)
multi_line_text_right = MultiLineText(font, WHITE, text_block_width)
multi_line_text_justify = MultiLineText(font, WHITE, text_block_width)


# Ukázkový text
long_text = """
Toto je poměrně dlouhý text, který se bude muset zalomit na více řádků.
Ukazuje, jak třída MultiLineText zvládá automatické zalomení textu, aby se vešel do definované šířky.
Můžete si vybrat různé typy zarovnání: doleva, na střed, doprava a do bloku (justify).
Zkuste změnit šířku bloku nebo velikost fontu, abyste viděli, jak se text přizpůsobí.
"""

multi_line_text_left.set_text(long_text)
multi_line_text_center.set_text(long_text)
multi_line_text_right.set_text(long_text)
multi_line_text_justify.set_text(long_text)


# Herní smyčka
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Vyplnění pozadí
    screen.fill(BLACK)

    # Vykreslení textu s různými zarovnáními
    pygame.draw.rect(screen, RED, (50, 50, text_block_width, multi_line_text_left.line_height * len(multi_line_text_left.lines)), 1)
    multi_line_text_left.render(screen, 50, 50, "left")
    
    pygame.draw.rect(screen, RED, (350, 50, text_block_width, multi_line_text_center.line_height * len(multi_line_text_center.lines)), 1)
    multi_line_text_center.render(screen, 350, 50, "center")

    pygame.draw.rect(screen, RED, (50, 300, text_block_width, multi_line_text_right.line_height * len(multi_line_text_right.lines)), 1)
    multi_line_text_right.render(screen, 50, 300, "right")

    pygame.draw.rect(screen, RED, (350, 300, text_block_width, multi_line_text_justify.line_height * len(multi_line_text_justify.lines)), 1)
    multi_line_text_justify.render(screen, 350, 300, "justify")

    # Aktualizace obrazovky
    pygame.display.flip()

pygame.quit()
