import pygame
from constants import WIDTH, TEXT_COLOR, HIGHLIGHT_COLOR, font_main, font_title

class MenuView:
    """Handles rendering for the Menu (Single Responsibility: View)."""
    def draw(self, surface, menu):
        title = font_title.render("SELECT DIFFICULTY", True, HIGHLIGHT_COLOR)
        surface.blit(title, (WIDTH//2 - title.get_width()//2, 100))

        for i, opt in enumerate(menu.options):
            rect = pygame.Rect(WIDTH//2 - 100, 320 + i * 80, 200, 50)
            color = HIGHLIGHT_COLOR if rect.collidepoint(pygame.mouse.get_pos()) else TEXT_COLOR
            pygame.draw.rect(surface, color, rect, 2, border_radius=10)
            txt = font_main.render(opt, True, color)
            surface.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))
