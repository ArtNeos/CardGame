import random
import pygame
from pygame.sprite import Group
from pygame.surface import Surface
import cartopedia
from recipes import recipes, Recipe


class Card(pygame.sprite.Sprite):
    """Класс карт добавляемых на игровое поле"""
    nm_h = 40
    width = 150
    height = 200

    def __init__(self, screen: Surface, interface, card_id=None):
        super(Card, self).__init__()
        self.screen = screen
        self.interface = interface
        interface.cards += 1
        if card_id is None:
            card_id = random.choice(cartopedia.resources)
        self.properties = cartopedia.cards[card_id]
        self.image = pygame.image.load(self.properties['path']).convert()
        self.id = card_id
        if self.properties.get('food_needed'):
            interface.food_needed += self.properties['food_needed']
        if self.properties.get('food'):
            interface.food += self.properties['food']
        if self.properties.get('card_cap'):
            interface.cards_cap += self.properties['card_cap']
        self.screen_rect = self.screen.get_rect()
        self.rect = pygame.Rect(self.screen_rect.centerx - self.width / 2,
                                self.screen_rect.centery - self.height / 2,
                                self.width, self.height)

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def sell(self, interface):
        if self.properties['sellable']:
            interface.coins += self.properties['price']
            if self.properties.get('food_needed'):
                interface.food_needed -= self.properties['food_needed']
            if self.properties.get('food'):
                interface.food -= self.properties['food']
            if self.properties.get('card_cap'):
                interface.cards_cap -= self.properties['card_cap']
            self.kill()
            self.interface.cards -= 1
            del self
            return True
        return False


class Stack(Group):
    """класс стопки карт"""
    max_len = 4

    def __init__(self, pos, stacks, craft_stacks, grid, screen, interface):
        """Создание стопки"""
        super(Stack, self).__init__()
        self._left, self._top = pos
        self._right = self._left + Card.width
        self._bottom = self._top + Card.height - Card.nm_h
        self._centerx = (self._left + self._right) // 2
        self._centery = (self._top + self._bottom) // 2
        self.container = stacks
        self.craft_container = craft_stacks
        self.grid = grid
        self.screen = screen
        self.interface = interface
        stacks.append(self)

    def __del__(self):
        self.container.remove(self)

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, value):
        self._left = value
        self._right = self._left + Card.width
        self._centerx = (self._left + self._right) // 2

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, value):
        self._right = value
        self._left = self._right - Card.width
        self._centerx = (self._left + self._right) // 2

    @property
    def centerx(self):
        return self._centerx

    @centerx.setter
    def centerx(self, value):
        self._centerx = value
        self._left = self._centerx - Card.width // 2
        self._right = self._left + Card.width

    @property
    def top(self):
        return self._top

    @top.setter
    def top(self, value):
        self._top = value
        self._bottom = self._top + Card.height
        self._centery = (self._top + self._bottom) // 2

    @property
    def bottom(self):
        return self._bottom

    @bottom.setter
    def bottom(self, value):
        self._bottom = value
        self._top = self._bottom - Card.height
        self._centery = (self._top + self._bottom) // 2

    @property
    def centery(self):
        return self._centery

    @centery.setter
    def centery(self, value):
        self._centery = value
        self._top = self._centery - Card.height // 2
        self._bottom = self._top + Card.height

    def add(self, *crds):
        """Добавление карт в стопку"""
        for card in crds:
            if isinstance(card, list):
                for subcard in card:
                    self.add(subcard)
            else:
                if len(self) >= 4:
                    raise OverflowError(f"Стек не может быть больше {self.max_len} карт")
                super(Group, self).add(card)
                self._top -= Card.nm_h // 2
                self._bottom += Card.nm_h // 2
        self.align_cards()

    def remove(self, *cards):
        """Удаление карты из стопки"""
        for card in cards:
            if isinstance(card, list):
                self.remove(*card)
            else:
                super(Group, self).remove(card)
                self._top += Card.nm_h // 2
                self._bottom -= Card.nm_h // 2
        self.align_cards()

    def empty(self):
        """Опустошение стопки"""
        for sprite in self.sprites():
            self.remove(sprite)
            sprite.remove(self)

    def add_substack(self, substack):
        """Перекладывание одной стопки в другую"""
        if len(self) + len(substack) > 4:
            raise OverflowError(f"Стек не может быть больше {self.max_len} карт")
        if self in self.craft_container:
            self.craft_container.remove(self)
        cards = substack.sprites().copy()
        substack.empty()
        self.add(cards)
        del substack
        craft = self.check_recipe()
        if craft:
            self.start_craft(craft)

    def on_stack(self, pos):
        """Проверка положения курсора относительно карт стопки,
        возвращает номер карты сверху стопки над которой стоит указатель"""
        if len(self) == 0:
            return 0
        x, y = pos
        if not self.left < x <= self.right:
            return 0
        if self.bottom > y >= self.bottom - Card.height:
            return 1
        for i in range(Stack.max_len - 1):
            if self.bottom - Card.height - Card.nm_h * i > y >= self.bottom - Card.height - Card.nm_h * (i + 1) and \
                    len(self) >= i + 2:
                return i + 2
        return 0

    def take_substack(self, num):
        """Снять часть карт создав новую стопку"""
        if self in self.craft_container:
            self.craft_container.remove(self)
        first_card = self.sprites()[-num]
        new_stack_left = first_card.rect.left
        new_stack_top = first_card.rect.top + num * Card.nm_h // 2
        substack = Stack((new_stack_left, new_stack_top), self.container, self.craft_container, self.grid, self.screen,
                         self.interface)
        substack.add(*self.sprites()[len(self) - num:])
        self.remove(*substack.sprites())
        self.align_cards()
        craft = self.check_recipe()
        if craft:
            self.start_craft(craft)
        return substack

    def move(self, pos):
        """переместить стопку в данную позицию"""
        self.left, self.top = pos
        self.align_cards()

    def move_rel(self, rel):
        """переместить стопку на данный вектор"""
        self.left += rel[0]
        self.top += rel[1]
        self.align_cards()

    def check_recipe(self):
        """проверка соотвествия стопки какому-либо рецепту. Возвращает результат рецепта в случае его существования"""
        id_set = Recipe([card.id for card in self.sprites()])
        res = recipes.get(id_set)
        return res

    def sell(self, interface, num):
        """продажа всех карт в стаке"""
        if self in self.craft_container:
            self.craft_container.remove(self)
        for i in range(min(num, len(self))):
            if self.sprites()[-1].sell(interface):
                self._top += Card.nm_h // 2
                self._bottom -= Card.nm_h // 2
        self.align_cards()
        craft = self.check_recipe()
        if craft:
            self.start_craft(craft)

    def align_cards(self):
        """Выравнивает все карты в стопке"""
        for i, card in enumerate(self.sprites()):
            card.rect.left = self._left
            card.rect.top = self._top + i * Card.nm_h

    def start_craft(self, craft):
        """начинает процесс крафта"""
        self.craft = craft
        self.progress = 0
        self.craft_container.append(self)

    def crafting(self):
        """обновление прогресс бара крафта и завершение крафта"""
        self.progress += 1 / self.craft['duration']
        if self.progress >= 1:
            for card in self:
                if card.properties.get('food_needed'):
                    self.interface.food_needed -= card.properties['food_needed']
                self.interface.cards -= 1
            self.empty()
            for card_id in self.craft['result']:
                self.add(Card(self.screen, self.interface, card_id))
            self.craft_container.remove(self)
        else:
            bg_for_bar = pygame.Rect(self.left + 10, self.bottom - 30, self.right - self.left - 20, 10)
            pygame.draw.rect(self.screen, (0, 0, 0), bg_for_bar)
            bar_rect = pygame.Rect(self.left + 10, self.bottom - 30, (self.right - self.left - 20) * self.progress, 10)
            pygame.draw.rect(self.screen, (255, 255, 255), bar_rect)
