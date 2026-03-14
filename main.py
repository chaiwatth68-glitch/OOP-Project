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

# Game Colors
COLORS = {
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'yellow': (255, 255, 0),
    'blue': (0, 0, 255),
    'orange': (255, 165, 0),
    'pink': (255, 192, 203),
    'white': (255, 255, 255),
    'light_purple': (221, 160, 221)
}

LEVEL_COLORS = {
    'easy': ['red', 'green', 'yellow', 'blue'],
    'medium': ['red', 'green', 'yellow', 'blue', 'orange', 'pink'],
    'hard': ['red', 'green', 'yellow', 'blue', 'orange', 'pink', 'white', 'light_purple']
}

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
CARD_SIZE = 110
MARGIN = 20

def get_grid_geometry(level):
    """Return (rows, cols, offset_x, offset_y) for the given difficulty."""
    if level == 'easy':
        rows, cols = 2, 2
    elif level == 'medium':
        rows, cols = 3, 4
    else:
        rows, cols = 4, 4

    grid_width = cols * CARD_SIZE + (cols - 1) * MARGIN
    grid_height = rows * CARD_SIZE + (rows - 1) * MARGIN
    offset_x = (WIDTH - grid_width) // 2
    offset_y = 150
    return rows, cols, offset_x, offset_y

# --- Classes ---
class Card:
    def __init__(self, x, y, value):
        self.rect = pygame.Rect(x, y, CARD_SIZE, CARD_SIZE)
        self.value = value
        self.is_flipped = False
        self.is_matched = False
        self.is_visible = value is not None
        self.animation_progress = 0  # 0 to 1
        self.hovered = False

    def draw(self, surface):
        if not self.is_visible:
            return

        # Determine display color
        if self.is_matched:
            color = MATCH_COLOR
        elif self.is_flipped:
            color = COLORS.get(self.value, CARD_FRONT)
        else:
            color = CARD_BACK

        # Draw card (simple rounded rectangle)
        pygame.draw.rect(surface, color, self.rect, border_radius=20)

# --- Game Logic ---
def init_game(level):
    rows, cols, offset_x, offset_y = get_grid_geometry(level)

    colors = LEVEL_COLORS[level]
    values = colors * 2
    total_cards = rows * cols
    if len(values) < total_cards:
        values += [None] * (total_cards - len(values))
    random.shuffle(values)
    
    cards = []
    for r in range(rows):
        for c in range(cols):
            x = offset_x + c * (CARD_SIZE + MARGIN)
            y = offset_y + r * (CARD_SIZE + MARGIN)
            cards.append(Card(x, y, values.pop()))
    return cards, rows, cols

def main(level):
    cards, rows, cols = init_game(level)
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
                    if card.is_visible and card.rect.collidepoint(event.pos) and not card.is_flipped and not card.is_matched:
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
                                visible_cards = [c for c in cards if c.is_visible]
                                if all(c.is_matched for c in visible_cards):
                                    game_over = True
                            else:
                                score = max(0, score - 2)
                                waiting_timer = pygame.time.get_ticks()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_over:
                    cards, rows, cols = init_game(level)
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
            card.hovered = card.is_visible and card.rect.collidepoint(mouse_pos)

        # --- Drawing ---
        # Draw Header
        title_surf = font_title.render("MEMORY MASTER", True, HIGHLIGHT)
        screen.blit(title_surf, (WIDTH//2 - title_surf.get_width()//2, 40))
        
        info_text = f"Score: {score}   |   Moves: {moves}   |   Level: {level.capitalize()}"
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

def show_menu():
    clock = pygame.time.Clock()
    selected_level = None
    
    while selected_level is None:
        screen.fill(BG_COLOR)
        
        # Title
        title_surf = font_title.render("MEMORY MASTER", True, HIGHLIGHT)
        screen.blit(title_surf, (WIDTH//2 - title_surf.get_width()//2, 100))
        
        # Instructions
        instr_surf = font_main.render("Select Difficulty Level:", True, TEXT_COLOR)
        screen.blit(instr_surf, (WIDTH//2 - instr_surf.get_width()//2, 200))
        
        # Levels
        levels = [
            ("1 - Easy (4 Colors)", 'easy'),
            ("2 - Medium (6 Colors)", 'medium'),
            ("3 - Hard (8 Colors)", 'hard')
        ]
        
        for i, (text, level) in enumerate(levels):
            color = HIGHLIGHT if i == 0 else TEXT_COLOR  # Highlight first option
            level_surf = font_main.render(text, True, color)
            screen.blit(level_surf, (WIDTH//2 - level_surf.get_width()//2, 280 + i * 50))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_level = 'easy'
                elif event.key == pygame.K_2:
                    selected_level = 'medium'
                elif event.key == pygame.K_3:
                    selected_level = 'hard'
        
        clock.tick(60)
    
    return selected_level

if __name__ == "__main__":
    level = show_menu()
    if level:
        main(level)