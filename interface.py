import pygame


class Interface:
    """Статистика игрока"""
    def __init__(self, screen, bg_color, stacks):
        # Statuses
        self.run = True
        self.selling = False
        # external instances
        self.stacks = stacks
        self.cursor = None
        # properties
        self._coins = 0
        self._cards = 0
        self._cards_cap = 20
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.text_color = (1, 1, 1)
        self.bg_color = bg_color
        self.food_duration = 3000
        self.food_progress = 0
        self._food_needed = 0
        self._food = 0
        self.subimages = {}

        self.create_interface()

    def set_cursor(self, cursor):
        self.cursor = cursor

    @property
    def food(self):
        return self._food

    @food.setter
    def food(self, value):
        self._food = value
        food_nums_font = pygame.font.SysFont('arial', 40)
        food_nums = f'{self.food} / {self.food_needed}'
        self.subimages['food']['img'] = self.create_image(food_nums_font, food_nums)
        pygame.draw.rect(self.image, self.bg_color, self.subimages['food']['rect'])
        self.image.blit(self.subimages['food']['img'], self.subimages['food']['rect'])

    @property
    def food_needed(self):
        return self._food_needed

    @food_needed.setter
    def food_needed(self, value):
        self._food_needed = value
        food_nums_font = pygame.font.SysFont('arial', 40)
        food_nums = f'{self.food} / {self.food_needed}'
        self.subimages['food']['img'] = self.create_image(food_nums_font, food_nums)
        pygame.draw.rect(self.image, self.bg_color, self.subimages['food']['rect'])
        self.image.blit(self.subimages['food']['img'], self.subimages['food']['rect'])


    @property
    def coins(self):
        return self._coins

    @coins.setter
    def coins(self, value):
        self._coins = value
        coin_path = 'card_images/coin.png'
        coin_font = pygame.font.SysFont('arial', 72)
        coin_text = f'X {self.coins}'
        self.subimages['coins']['img'] = self.create_image(coin_font, coin_text, coin_path)
        self.image.blit(self.subimages['coins']['img'], self.subimages['coins']['rect'])


    @property
    def cards(self):
        return self._cards

    @cards.setter
    def cards(self, value):
        self._cards = value
        cards_path = 'card_images/cards_img.png'
        cards_font = pygame.font.SysFont('arial', 54)
        cards_text = f'X {self.cards}/{self.cards_cap}'
        self.subimages['cards']['img'] = self.create_image(cards_font, cards_text, cards_path)
        self.image.blit(self.subimages['cards']['img'], self.subimages['cards']['rect'])

    @property
    def cards_cap(self):
        return self._cards_cap

    @cards_cap.setter
    def cards_cap(self, value):
        self._cards_cap = value
        cards_path = 'card_images/cards_img.png'
        cards_font = pygame.font.SysFont('arial', 54)
        cards_text = f'X {self.cards}/{self.cards_cap}'
        self.subimages['cards']['img'] = self.create_image(cards_font, cards_text, cards_path)
        self.image.blit(self.subimages['cards']['img'], self.subimages['cards']['rect'])

    def create_image(self, font, text, path=None):
        if path:
            icon = pygame.image.load(path)
            icon_rect = icon.get_rect()
        text = font.render(text, True, self.text_color)
        text_rect = text.get_rect()
        text_rect.left = icon_rect.right if path else 0
        w = (icon_rect.width if path else 0) + text_rect.width
        h = max((icon_rect.height if path else 0), text_rect.height)
        image = pygame.Surface((w, h)).convert(self.image)
        image.fill(self.bg_color)
        if path:
            image.blit(icon, icon_rect)
        image.blit(text, text_rect)
        return image

    def create_interface(self):
        self.image = pygame.Surface((229, 960)).convert()
        self.image.fill(self.bg_color)
        rect = self.image.get_rect()

        #  Отрисовка монет
        coin_path = 'card_images/coin.png'
        coin_font = pygame.font.SysFont('arial', 72)
        coin_text = f'X {self.coins}'
        coin_image = self.create_image(coin_font, coin_text, coin_path)
        coin_rect = coin_image.get_rect()
        self.image.blit(coin_image, coin_rect)
        self.subimages['coins'] = {'img': coin_image, 'rect': coin_rect}

        # отрисовка количества карт
        cards_path = 'card_images/cards_img.png'
        cards_font = pygame.font.SysFont('arial', 54)
        cards_text = f'X {self.cards}/{self.cards_cap}'
        cards_image = self.create_image(cards_font, cards_text, cards_path)
        cards_rect = cards_image.get_rect()
        cards_rect.top = coin_rect.bottom + 5
        self.image.blit(cards_image, cards_rect)
        self.subimages['cards'] = {'img': cards_image, 'rect': cards_rect}

        # отрисовка количества имеющейся и необходимой еды
        food_text_image = pygame.font.SysFont('arial', 30).render('Food requirement', True,
                                                                  self.text_color).convert_alpha(self.image)
        food_text_rect = food_text_image.get_rect()
        food_text_rect.top = cards_rect.bottom + 5
        self.image.blit(food_text_image, food_text_rect)

        food_nums_font = pygame.font.SysFont('arial', 40)
        food_nums = f'{self.food} / {self.food_needed}'
        food_image = self.create_image(food_nums_font, food_nums)
        food_rect = food_image.get_rect()
        food_rect.left += 30
        food_rect.top = food_text_rect.bottom + 2
        self.image.blit(food_image, food_rect)
        self.subimages['food'] = {'img': food_image, 'rect': food_rect}

        pygame.draw.rect(self.image, (0, 0, 0), pygame.Rect(15, 270, 200, 10))

        # отрисовка предупреждения
        text = pygame.font.SysFont('arial', 28).render("Слишком много карт", True, (255, 0, 0),
                                                       self.bg_color).convert(self.image)
        text_rect = text.get_rect()
        text_rect.top = 280
        text_rect.right = self.image.get_rect().right
        self.subimages['warning'] = {'img': text, 'rect': text_rect}

        #  отрисовка кнопки купить
        buy_image = pygame.image.load('card_images/buy_button.png').convert(self.image)
        self.image.blit(buy_image, (15, 900))

        self.rect = rect
        self.rect.right = self.screen.get_rect().right

    def update(self):
        if not self.selling:
            self.food_progress += 1 / self.food_duration
            if self.food_progress < 1:
                pygame.draw.rect(self.image, (255, 255, 255), pygame.Rect(15, 270, 200*self.food_progress, 10))
            else:
                pygame.draw.rect(self.image, (0, 0, 0), pygame.Rect(15, 270, 200, 10))
                if self.check_food():
                    self.food_progress = 0
                else:
                    self.run = False
                    text = pygame.font.SysFont('arial', 200).render('Game over!', True, (255, 0, 0))
                    text_rect = text.get_rect()
                    text_rect.center = self.screen_rect.center
                    self.screen.blit(text, text_rect)
                    return
                self.check_selling()
        else:
            self.check_selling()

    def check_food(self):
        food_to_eat = self.food_needed
        for stack in self.stacks:
            for i in range(len(stack.sprites())-1, -1, -1):
                card = stack.sprites()[i]
                if card.properties.get('food'):
                    food_to_eat -= card.properties['food']
                    self.food -= card.properties['food']
                    stack.remove(card)
                    self.cards -= 1
                if food_to_eat <= 0:
                    return True
        return False

    def check_selling(self):

        if self.cards > self.cards_cap and not self.selling:
            self.selling = True
            self.image.blit(self.subimages['warning']['img'], self.subimages['warning']['rect'])
        elif self.cards <= self.cards_cap and self.selling:
            self.selling = False
            pygame.draw.rect(self.image, self.bg_color, self.subimages['warning']['rect'])

    def on_buy(self, pos):
        x, y = pos
        return 1275 < x < 1475 and 900 < y < 950

    def draw(self):
        self.screen.blit(self.image, self.rect)
