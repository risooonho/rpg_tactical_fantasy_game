import pygame as pg

from src.TextElement import TextElement
from src.Button import Button
from src.DynamicButton import DynamicButton
from src.ItemButton import ItemButton
from src.constants import TILE_SIZE, WHITE


MENU_TITLE_FONT = pg.font.Font('fonts/_bitmap_font____romulus_by_pix3m-d6aokem.ttf', 26)
ITEM_FONT = pg.font.Font('fonts/_bitmap_font____romulus_by_pix3m-d6aokem.ttf', 16)
ITEM_FONT_HOVER = pg.font.Font('fonts/_bitmap_font____romulus_by_pix3m-d6aokem.ttf', 17)
ITEM_DESC_FONT = pg.font.Font('fonts/_bitmap_font____romulus_by_pix3m-d6aokem.ttf', 22)

MARGINTOP = 10
MARGINBOX = 20

MAP_WIDTH = TILE_SIZE * 20
MAP_HEIGHT = TILE_SIZE * 10

BUTTON_INACTIVE = "imgs/interface/MenuButtonInactiv.png"
BUTTON_ACTIVE = "imgs/interface/MenuButtonPreLight.png"

BUTTON_SIZE = (150, 30)
ITEM_BUTTON_SIZE = (180, TILE_SIZE + 30)
EQUIP_BUTTON_SIZE = (150, TILE_SIZE + 10)
CLOSE_BUTTON_SIZE = (160, 40)
CLOSE_ACTION_ID = -1
CLOSE_BUTTON_MARGINTOP = 20

DEFAULT_WIDTH = 400


class InfoBox:
    def __init__(self, name, type_id, sprite, entries, width=DEFAULT_WIDTH, el_rect_linked=None, close_button=0,
                 title_color=WHITE):
        self.name = name
        self.type = type_id
        self.element_linked = el_rect_linked
        self.close_button = close_button
        self.title_color = title_color
        self.entries = entries

        self.elements = self.init_elements(self.entries, width)
        height = self.determine_sizepos(close_button)
        self.size = (width, height)
        self.pos = self.determine_pos()

        if self.pos:
            self.determine_elements_pos()
        self.buttons = self.get_buttons()

        self.sprite = pg.transform.scale(pg.image.load(sprite).convert_alpha(), self.size)

    def init_elements(self, entries, width):
        elements = []
        for row in entries:
            element = []
            for entry in row:
                if 'margin' not in entry:
                    entry['margin'] = (0, 0, 0, 0)

                if entry['type'] == 'button':
                    name = ITEM_FONT.render(entry['name'], 1, WHITE)
                    sprite = pg.transform.scale(pg.image.load(BUTTON_INACTIVE).convert_alpha(), BUTTON_SIZE)
                    sprite.blit(name, (sprite.get_width() // 2 - name.get_width() // 2,
                                       sprite.get_height() // 2 - name.get_height() // 2))
                    sprite_hover = pg.transform.scale(pg.image.load(BUTTON_ACTIVE).convert_alpha(), BUTTON_SIZE)
                    sprite_hover.blit(name, (sprite_hover.get_width() // 2 - name.get_width() // 2,
                                             sprite_hover.get_height() // 2 - name.get_height() // 2))
                    if 'args' not in entry:
                        entry['args'] = []

                    element.append(Button(entry['id'], entry['args'], BUTTON_SIZE, (0, 0), sprite, sprite_hover,
                                          entry['margin']))
                elif entry['type'] == 'parameter_button':
                    name = ITEM_FONT.render(entry['name'] + ' ' + entry['values'][entry['current_value_ind']]['label'], 1, WHITE)
                    base_sprite = pg.transform.scale(pg.image.load(BUTTON_INACTIVE).convert_alpha(), BUTTON_SIZE)
                    sprite = base_sprite.copy()
                    sprite.blit(name, (base_sprite.get_width() // 2 - name.get_width() // 2,
                                       base_sprite.get_height() // 2 - name.get_height() // 2))
                    base_sprite_hover = pg.transform.scale(pg.image.load(BUTTON_ACTIVE).convert_alpha(), BUTTON_SIZE)
                    sprite_hover = base_sprite_hover.copy()
                    sprite_hover.blit(name, (base_sprite_hover.get_width() // 2 - name.get_width() // 2,
                                             base_sprite_hover.get_height() // 2 - name.get_height() // 2))
                    element.append(DynamicButton(entry['id'], [], BUTTON_SIZE, (0, 0), sprite, sprite_hover,
                                                 entry['margin'], entry['values'], entry['current_value_ind'], entry['name'],
                                                 base_sprite, base_sprite_hover))
                elif entry['type'] == 'text_button':
                    name = ITEM_FONT.render(entry['name'], 1, entry['color'])
                    name_hover = ITEM_FONT.render(entry['name'], 1, entry['color_hover'])
                    if 'obj' not in entry:
                        entry['obj'] = None
                    element.append(Button(entry['id'], [], name.get_size(), (0, 0), name, name_hover, entry['margin'], entry['obj']))

                elif entry['type'] == 'item_button':
                    button_size = ITEM_BUTTON_SIZE
                    disabled = 'disabled' in entry
                    if 'subtype' in entry:
                        if entry['subtype'] == 'equip':
                            button_size = EQUIP_BUTTON_SIZE
                    if 'price' not in entry:
                        entry['price'] = 0
                    element.append(ItemButton(button_size, (0, 0), entry['item'], entry['margin'], entry['index'],
                                              entry['price'], disabled))
                elif entry['type'] == 'text':
                    if 'font' not in entry:
                        entry['font'] = ITEM_FONT
                    if 'color' not in entry:
                        entry['color'] = WHITE
                    element.append(TextElement(entry['text'], width, (0, 0), entry['font'], entry['margin'], entry['color']))
            elements.append(element)
        elements.insert(0, [TextElement(self.name, width, (0, 0), MENU_TITLE_FONT, (len(entries) + 5, 0, 0, 0),
                                        self.title_color)])
        return elements

    def determine_sizepos(self, close_button):
        # Margin to be add at begin and at end
        height = MARGINBOX * 2
        for row in self.elements:
            max_height = 0
            for el in row:
                el_height = el.get_height() + MARGINTOP
                if el_height > max_height:
                    max_height = el_height
            height += max_height
            row.insert(0, max_height)
        if close_button > 0:
            close_button_height = CLOSE_BUTTON_SIZE[1] + MARGINTOP + CLOSE_BUTTON_MARGINTOP
            height += close_button_height

            # Button sprites
            name = ITEM_FONT.render("Close", 1, WHITE)
            sprite = pg.transform.scale(pg.image.load(BUTTON_INACTIVE).convert_alpha(), CLOSE_BUTTON_SIZE)
            sprite.blit(name, (sprite.get_width() // 2 - name.get_width() // 2,
                               sprite.get_height() // 2 - name.get_height() // 2))
            sprite_hover = pg.transform.scale(pg.image.load(BUTTON_ACTIVE).convert_alpha(), CLOSE_BUTTON_SIZE)
            sprite_hover.blit(name, (sprite_hover.get_width() // 2 - name.get_width() // 2,
                                     sprite_hover.get_height() // 2 - name.get_height() // 2))

            self.elements.append([close_button_height,
                                  Button(CLOSE_ACTION_ID, [close_button], CLOSE_BUTTON_SIZE, (0, 0), sprite,
                                         sprite_hover, (CLOSE_BUTTON_MARGINTOP, 0, 0, 0))])
        return height

    def determine_pos(self):
        if self.element_linked:
            pos = [self.element_linked.x + self.element_linked.width, self.element_linked.y + self.element_linked.height - self.size[1] // 2]
            if pos[1] < 0:
                pos[1] = 0
            elif pos[1] + self.size[1] > MAP_HEIGHT:
                pos[1] = MAP_HEIGHT - self.size[1]
            if pos[0] + self.size[0] > MAP_WIDTH:
                pos[0] = self.element_linked.x - self.size[0]
            return pos
        return []

    def get_type(self):
        return self.type

    def get_buttons(self):
        buttons = []
        for row in self.elements:
            for el in row[1:]:
                if isinstance(el, Button):
                    buttons.append(el)
        return buttons

    def get_entries(self):
        return self.entries

    def determine_elements_pos(self):
        y = self.pos[1] + MARGINBOX
        for row in self.elements:
            base_x = self.pos[0]
            nb_elements = len(row) - 1
            i = 1
            for el in row[1:]:
                base_x += (self.size[0] // (2 * nb_elements)) * i
                x = base_x - el.get_width() // 2
                el.set_pos((x, y + el.get_margin_top()))
                i += 1
            y += row[0]

    def update_content(self, entries):
        self.elements = self.init_elements(entries, self.size[0])
        self.determine_sizepos(self.close_button)
        if self.pos:
            self.determine_elements_pos()
        self.buttons = self.get_buttons()

    def display(self, win):
        if self.pos:
            win.blit(self.sprite, self.pos)
        else:
            win_size = win.get_size()
            self.pos = (win_size[0] // 2 - self.size[0] // 2, win_size[1] // 2 - self.size[1] // 2)
            win.blit(self.sprite, self.pos)
            self.determine_elements_pos()
            self.pos = []

        for row in self.elements:
            for el in row[1:]:
                el.display(win)

    def motion(self, pos):
        for button in self.buttons:
            button.set_hover(button.get_rect().collidepoint(pos))

    def click(self, pos):
        for button in self.buttons:
            if button.get_rect().collidepoint(pos):
                return button.action_triggered()
        return False
