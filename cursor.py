class Cursor:
    """выполняет действия захвата и перемещения карт, а также нажатия кнопок"""
    def __init__(self, grid, interface):
        self.grid = grid
        self.stack = None
        self.prev_stack = None
        self.interface = interface

    def is_grabbed(self):
        return self.stack

    def grab(self, pos):
        """нажатие лкм"""
        x, y = pos
        if self.grid.on_grid(pos):
            i = y // self.grid.cell_height
            j = x // self.grid.cell_width
            num = self.grid[i][j].on_stack((x, y))
            if num == 0:
                return
            self.stack = self.grid[i][j].take_substack(num)
            self.prev_stack = self.grid[i][j]
        elif self.interface.on_buy(pos):
            self.grid.buy_pack(self.interface)

    def move_stack(self, rel):
        """перемещение карты"""
        if not self.stack:
            raise AttributeError("There is no stack to move")
        self.stack.move_rel(rel)

    def ungrab(self):
        """отпускание карты"""

        x, y = self.stack.centerx, self.stack.centery
        i = y // self.grid.cell_height
        j = x // self.grid.cell_width
        try:
            self.grid[i][j].add_substack(self.stack)
        except (OverflowError, IndexError):
            self.prev_stack.add_substack(self.stack)
        self.stack = None

    def sell(self, pos):
        x, y = pos
        if not self.grid.on_grid(pos):
            return
        i = y // self.grid.cell_height
        j = x // self.grid.cell_width
        num = self.grid[i][j].on_stack((x, y))
        if num == 0:
            return
        self.stack = self.grid[i][j].sell(self.interface, num)
