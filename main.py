import pygame
import random
import time

# --- Setup & Configuration ---
pygame.init()

# Window settings
WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("✨ Premium Memory Match")

# Modern Premium Color Palette
BG_COLOR = (15, 15, 26)       # Deep Dark Blue
CARD_BACK = (30, 30, 50)     # Slightly lighter card back
CARD_FRONT = (240, 240, 255)  # Off-white front
HIGHLIGHT = (80, 120, 255)    # Vibrant Blue
MATCH_COLOR = (46, 204, 113)  # Emerald Green
TEXT_COLOR = (255, 255, 255)
ACCENT_COLOR = (255, 107, 107)# Coral Red

# Typography
try:
    font_main = pygame.font.SysFont("Outfit", 32)
    font_title = pygame.font.SysFont("Outfit", 48, bold=True)
    font_small = pygame.font.SysFont("Outfit", 20)
except:
    font_main = pygame.font.SysFont("Arial", 32)
    font_title = pygame.font.SysFont("Arial", 48, bold=True)
    font_small = pygame.font.SysFont("Arial", 20)

# Game Constants
ROWS, COLS = 4, 4
CARD_SIZE = 110
MARGIN = 20
GRID_OFFSET_X = (WIDTH - (COLS * (CARD_SIZE + MARGIN) - MARGIN)) // 2
GRID_OFFSET_Y = 150

# --- Classes ---
class Card:
    def __init__(self, x, y, value):
        self.rect = pygame.Rect(x, y, CARD_SIZE, CARD_SIZE)
        self.value = value
        self.is_flipped = False
        self.is_matched = False
        self.animation_progress = 0  # 0 to 1
        self.hovered = False

    def draw(self, surface):
        # Determine color and scale based on state
        color = CARD_BACK
        if self.is_matched:
            color = MATCH_COLOR
        elif self.is_flipped:
            color = CARD_FRONT
        
        # Draw shadow
        shadow_rect = self.rect.copy()
        shadow_rect.move_ip(4, 4)
        pygame.draw.rect(surface, (5, 5, 10), shadow_rect, border_radius=15)

        # Draw main card body
        draw_rect = self.rect.copy()
        if self.hovered and not self.is_matched and not self.is_flipped:
            draw_rect.inflate_ip(4, 4)
            pygame.draw.rect(surface, color, draw_rect, border_radius=15)
            pygame.draw.rect(surface, HIGHLIGHT, draw_rect, 2, border_radius=15)
        else:
            pygame.draw.rect(surface, color, draw_rect, border_radius=15)

        # Draw content if flipped or matched
        if self.is_flipped or self.is_matched:
            text_val = font_main.render(str(self.value), True, BG_COLOR if not self.is_matched else TEXT_COLOR)
            text_rect = text_val.get_rect(center=self.rect.center)
            surface.blit(text_val, text_rect)

# --- Game Logic ---
def init_game():
    values = list(range(1, (ROWS * COLS // 2) + 1)) * 2
    random.shuffle(values)
    
    cards = []
    for r in range(ROWS):
        for c in range(COLS):
            x = GRID_OFFSET_X + c * (CARD_SIZE + MARGIN)
            y = GRID_OFFSET_Y + r * (CARD_SIZE + MARGIN)
            cards.append(Card(x, y, values.pop()))
    return cards

def main():
    cards = init_game()
    selected = []
    waiting_timer = 0
    score = 0
    moves = 0
    game_over = False
    
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BG_COLOR)
        
        # --- Event Handling ---
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and not waiting_timer and not game_over:
                for card in cards:
                    if card.rect.collidepoint(event.pos) and not card.is_flipped and not card.is_matched:
                        card.is_flipped = True
                        selected.append(card)
                        
                        if len(selected) == 2:
                            moves += 1
                            if selected[0].value == selected[1].value:
                                selected[0].is_matched = True
                                selected[1].is_matched = True
                                score += 10
                                selected = []
                                # Check Win Condition
                                if all(c.is_matched for c in cards):
                                    game_over = True
                            else:
                                score = max(0, score - 2)
                                waiting_timer = pygame.time.get_ticks()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_over:
                    cards = init_game()
                    score = 0
                    moves = 0
                    game_over = False

        # --- Update ---
        if waiting_timer:
            if pygame.time.get_ticks() - waiting_timer > 800:
                for card in selected:
                    card.is_flipped = False
                selected = []
                waiting_timer = 0

        # Hover effect
        for card in cards:
            card.hovered = card.rect.collidepoint(mouse_pos)

        # --- Drawing ---
        # Draw Header
        title_surf = font_title.render("MEMORY MASTER", True, HIGHLIGHT)
        screen.blit(title_surf, (WIDTH//2 - title_surf.get_width()//2, 40))
        
        info_text = f"Score: {score}   |   Moves: {moves}"
        info_surf = font_main.render(info_text, True, TEXT_COLOR)
        screen.blit(info_surf, (WIDTH//2 - info_surf.get_width()//2, 100))

        # Draw Grid
        for card in cards:
            card.draw(screen)

        # Game Over Overlay
        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            
            win_msg = font_title.render("YOU WIN!", True, MATCH_COLOR)
            screen.blit(win_msg, (WIDTH//2 - win_msg.get_width()//2, HEIGHT//2 - 50))
            
            restart_msg = font_main.render("Press 'R' to Play Again", True, TEXT_COLOR)
            screen.blit(restart_msg, (WIDTH//2 - restart_msg.get_width()//2, HEIGHT//2 + 20))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()