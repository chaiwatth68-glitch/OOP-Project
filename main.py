# main.py - Main game loop

import pygame
import sys
from constants import screen, BG_COLOR, FPS
from sound_manager import SoundManager
from menu import Menu
from game import SimonGame

from menu_view import MenuView
from game_view import GameView

# --- Main Loop ---
sound_manager = SoundManager()
menu = Menu()
menu_view = MenuView()
game = None
game_view = GameView()
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(BG_COLOR)
    mouse_pos = pygame.mouse.get_pos()

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    if game is None:
        menu.update(mouse_pos, events)
        menu_view.draw(screen, menu)
        if menu.selected:
            game = SimonGame(menu.selected, sound_manager)
    else:
        # Update game and read return flags (next, retry, menu)
        result = game.update(mouse_pos, events)
        game_view.draw(screen, game)
        
        if result == "menu":
            game = None
            menu.selected = None # Reset choice
        elif result == "retry":
            game = SimonGame(menu.selected, sound_manager)
        elif result == "next":
            if menu.selected == "Easy": menu.selected = "Medium"
            elif menu.selected == "Medium": menu.selected = "Hard"
            game = SimonGame(menu.selected, sound_manager)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

