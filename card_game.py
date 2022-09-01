import time

import pygame
import controls

from grid import Grid
from cursor import Cursor
from interface import Interface


def main():
    pygame.init()
    screen = pygame.display.set_mode((1490, 960))
    pygame.display.set_caption("Стеки карт")
    bg_color = (116, 154, 242)
    stacks = []
    craft_stacks = []
    interface = Interface(screen, bg_color, stacks)
    gr = Grid(screen, stacks, craft_stacks, interface)
    cursor = Cursor(gr, interface)
    interface.set_cursor(cursor)

    clock = pygame.time.Clock()

    while interface.run:
        controls.events(screen, gr, cursor, interface)
        controls.update(screen, bg_color, gr, stacks, interface, craft_stacks)
        clock.tick(60)

    time.sleep(5)

if __name__ == "__main__":
    main()
