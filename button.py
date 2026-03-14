# button.py - Button classes for the game

import pygame
from constants import COLORS, BRIGHT, HIGHLIGHT_COLOR, TEXT_COLOR, font_main

class Button:
    """Abstract base class for buttons (Abstraction: common button behavior)."""
    def __init__(self, rect, text="", color=TEXT_COLOR):
        self.rect = rect
        self.text = text
        self.color = color
        self._hovered = False  # Encapsulation: private attribute

    def update_hover(self, mouse_pos):
        self._hovered = self.rect.collidepoint(mouse_pos)

    def is_hovered(self):
        return self._hovered

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)

    def draw(self, surface):
        # Polymorphism: subclasses can override
        pygame.draw.rect(surface, self.color, self.rect, border_radius=10)
        if self.text:
            txt_surf = font_main.render(self.text, True, TEXT_COLOR)
            surface.blit(txt_surf, (self.rect.centerx - txt_surf.get_width()//2, self.rect.centery - txt_surf.get_height()//2))

class ColorButton(Button):
    """Color button for Simon game (Inheritance: extends Button)."""
    def __init__(self, rect, color_name):
        super().__init__(rect)
        self.color_name = color_name
        self._is_highlighted = False
        self._is_hover = False
        self._press_t = 0

    def set_highlight(self, highlight, hover=False):
        self._is_highlighted = highlight
        self._is_hover = hover

    def press(self):
        """Animate a quick press effect."""
        self._press_t = 6

    def draw(self, surface):
        # Polymorphism: override draw for color-specific rendering
        # Add a subtle drop shadow for modern depth
        shadow_rect = self.rect.move(6, 6)
        pygame.draw.rect(surface, (20, 20, 30), shadow_rect, border_radius=24)

        # Press animation (shrinks slightly)
        inset = 0
        if self._press_t > 0:
            inset = 6
            self._press_t -= 1
        elif self._is_hover:
            inset = 3

        draw_rect = self.rect.inflate(-inset, -inset)

        color = COLORS[self.color_name]
        border_color = (55, 55, 70)
        border_width = 4

        if self._is_highlighted:
            color = BRIGHT[self.color_name]
            border_color = (200, 220, 255)
            border_width = 4
        elif self._is_hover:
            # More obvious hover effect: brighter border + slight scale
            color = tuple(min(255, c + 30) for c in color)
            border_color = (255, 240, 255)
            border_width = 8

        pygame.draw.rect(surface, color, draw_rect, border_radius=24)
        pygame.draw.rect(surface, border_color, draw_rect, border_width, border_radius=24)
