# menu.py - Menu system for difficulty selection

import pygame
from constants import WIDTH, TEXT_COLOR, HIGHLIGHT_COLOR, font_main, font_title

class Menu:
    """Handles menu logic (Single Responsibility: menu management)."""
    def __init__(self):
        self.options = ["Easy", "Medium", "Hard"]
        self.selected = None

    def update(self, mouse_pos, event):
        self.selected = None
        for i, opt in enumerate(self.options):
            rect = pygame.Rect(WIDTH//2 - 100, 320 + i * 80, 200, 50)
            if rect.collidepoint(mouse_pos):
                if event and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.selected = opt
                break

    def draw(self, surface):
        title = font_title.render("SELECT DIFFICULTY", True, HIGHLIGHT_COLOR)
        surface.blit(title, (WIDTH//2 - title.get_width()//2, 100))

        for i, opt in enumerate(self.options):
            rect = pygame.Rect(WIDTH//2 - 100, 320 + i * 80, 200, 50)
            color = HIGHLIGHT_COLOR if rect.collidepoint(pygame.mouse.get_pos()) else TEXT_COLOR
            pygame.draw.rect(surface, color, rect, 2, border_radius=10)
            txt = font_main.render(opt, True, color)
            surface.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))