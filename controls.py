import pygame
import sys
from card import Card


def events(screen, gr, cursor, interface):
    """Обработка событий"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN and not interface.selling:
            if event.key == pygame.K_c:
                new_card = Card(screen, interface)
                gr.add(new_card)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not interface.selling:
                cursor.grab(event.pos)
            elif event.button == 3:
                cursor.sell(event.pos)
        elif event.type == pygame.MOUSEMOTION and cursor.is_grabbed() and not interface.selling:
            cursor.move_stack(event.rel)
        elif event.type == pygame.MOUSEBUTTONUP and not interface.selling:
            if cursor.is_grabbed():
                cursor.ungrab()


def update(screen, bg_color, grid, stacks, interface, craft_stacks):
    """Отрисовка движений"""
    screen.fill(bg_color)
    grid.draw_grid()
    for stack in stacks:
        stack.draw(screen)
    if not interface.selling:
        for stack in craft_stacks:
            stack.crafting()
    interface.update()
    interface.draw()
    pygame.display.flip()
