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

        for i, opt in enumerate(menu.options):
            rect = pygame.Rect(WIDTH//2 - 150, 350 + i * 120, 300, 80)
            color = HIGHLIGHT_COLOR if rect.collidepoint(pygame.mouse.get_pos()) else TEXT_COLOR
            pygame.draw.rect(surface, color, rect, 4, border_radius=15)
            txt = font_main.render(opt, True, color)
            surface.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))
