import pygame
from constants import WIDTH, TEXT_COLOR, HIGHLIGHT_COLOR, font_main, font_title

class MenuView:
    """Handles rendering for the Menu (Single Responsibility: View)."""
    def draw(self, surface, menu):
        # Game title
        game_title = font_title.render("MEMORY GAME", True, HIGHLIGHT_COLOR)
        surface.blit(game_title, (WIDTH//2 - game_title.get_width()//2, 80))

        # Subtitle
        title = font_main.render("SELECT DIFFICULTY", True, TEXT_COLOR)
        surface.blit(title, (WIDTH//2 - title.get_width()//2, 200))

        # Draw buttons
        for button in menu.buttons:
            button.draw(surface)
