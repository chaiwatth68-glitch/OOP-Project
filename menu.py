# menu.py - Menu system for difficulty selection

import pygame
from constants import WIDTH, TEXT_COLOR, HIGHLIGHT_COLOR, font_main, font_title

class Menu:
    """Handles menu logic (Single Responsibility: menu management)."""
    def __init__(self):
        self.options = ["Easy", "Medium", "Hard"]
        self.selected = None

    def update(self, mouse_pos, events):
        self.selected = None
        for i, opt in enumerate(self.options):
            rect = pygame.Rect(WIDTH//2 - 100, 320 + i * 80, 200, 50)
            if rect.collidepoint(mouse_pos):
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.selected = opt
                        break
                break
