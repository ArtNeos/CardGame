import pygame.draw
from pygame.surface import Surface
from card import Card, Stack


class Grid:
    cell_width = Card.width + 30
    cell_height = Card.height + (Stack.max_len - 1) * Card.nm_h

    def __init__(self, screen: Surface, stacks, craft_stacks, interface):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.row_len = min(7, int(self.screen_rect.width / self.cell_width))
        self.col_len = int(self.screen_rect.height / self.cell_height)
        self.grid = [
            [
                Stack((int(Grid.cell_width * (i + 0.5) - Card.width * 0.5), Grid.cell_height * j+80),
                      stacks, craft_stacks, self, self.screen, interface) for i in range(self.row_len)
            ] for j in range(self.col_len)
        ]
        center_row = self.grid[len(self.grid) // 2]
        center_cell = center_row[len(center_row) // 2]
        start_pack = [Card(screen, interface, 9),
                      Card(screen, interface, 10),
                      Card(screen, interface, 3),
                      Card(screen, interface, 5)
                      ]

        center_cell.add(start_pack)

    def __getitem__(self, index):
        return self.grid[index]

    def first_empty(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if not self.grid[i][j]:
                    return i, j
        return None, None

    def add(self, card: Card):
        i, j = self.first_empty()
        if i is None or j is None:
            raise OverflowError("Grid is already full")
        self.grid[i][j].add(card)

    def draw_grid(self):
        for i in range(self.row_len):
            pygame.draw.line(self.screen, (0, 0, 0),
                             (self.cell_width * (i + 1), 0), (self.cell_width * (i + 1), 960))
        for i in range(self.col_len - 1):
            pygame.draw.line(self.screen, (0, 0, 0),
                             (0, self.cell_height * (i + 1)), (1260, self.cell_height * (i + 1)))

    def on_grid(self, pos):
        return pos[0] < self.row_len * self.cell_width

    def buy_pack(self, interface):
        if interface.coins < 3:
            return
        i, j = self.first_empty()
        if i is None:
            return
        interface.coins -= 3
        for _ in range(3):
            self.grid[i][j].add(Card(self.screen, interface))