# main.py - Main game loop

import pygame
import sys
from constants import screen, BG_COLOR, FPS
from sound_manager import SoundManager
from menu import Menu
from game import SimonGame

# --- Main Loop ---
sound_manager = SoundManager()
menu = Menu()
game = None
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(BG_COLOR)
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game is None:
        menu.update(mouse_pos, event if 'event' in locals() else None)
        menu.draw(screen)
        if menu.selected:
            game = SimonGame(menu.selected, sound_manager)
    else:
        game.update(mouse_pos, event if 'event' in locals() else None)
        game.draw(screen)
        if game.get_state() in ["won", "failed"]:
            # Simple restart for demo
            game = None

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

