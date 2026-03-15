# menu.py - Menu system for difficulty selection

import pygame
from constants import WIDTH, TEXT_COLOR, HIGHLIGHT_COLOR, font_main, font_title
from button import TextButton

class Menu:
    """Handles menu logic (Single Responsibility: menu management)."""
    def __init__(self):
        self.options = ["Easy", "Medium", "Hard"]
        self.buttons = []
        for i, opt in enumerate(self.options):
            rect = pygame.Rect(WIDTH//2 - 150, 350 + i * 120, 300, 80)
            self.buttons.append(TextButton(rect, opt))
        self.selected = None

    def update(self, mouse_pos, events):
        self.selected = None
        for button in self.buttons:
            button.update_hover(mouse_pos)
            for event in events:
                if button.is_clicked(event):
                    self.selected = button.text
                    return

