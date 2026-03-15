import random
import pygame
from abc import ABC, abstractmethod
from constants import WIDTH, HEIGHT, DIFFICULTY_CONFIG, MAX_STAGES, TEXT_COLOR, HIGHLIGHT_COLOR, font_main, font_small
from button import TextButton, ColorButton

class SequenceStrategy(ABC):
    """Abstract Strategy for sequence generation (Abstraction: Strategy Pattern)."""
    @abstractmethod
    def generate_next(self, current_sequence, colors):
        pass

class NoRepeatStrategy(SequenceStrategy):
    """Strategy that prevents consecutive identical colors (Polymorphism)."""
    def generate_next(self, current_sequence, colors):
        new_color = random.choice(colors)
        if current_sequence:
            while new_color == current_sequence[-1]:
                new_color = random.choice(colors)
        return new_color

class MemoryGame:
    """Main game logic (Encapsulation: game state management)."""
    def __init__(self, difficulty, sound_manager, strategy=None):
        self.difficulty = difficulty
        self.sound_manager = sound_manager
        self.strategy = strategy if strategy else NoRepeatStrategy() # Dependency Injection
        self.config = DIFFICULTY_CONFIG[difficulty]
        self.colors = self.config["colors"]

        self.grid_rows, self.grid_cols = self.config["grid"]
        self.ai_delay_ms, self.player_delay_ms = self.config["speed"]

        self.sequence = []
        self.player_input = []
        self.stage = 0
        self.state = "showing"  # showing, waiting, won, failed
        self.show_index = 0
        self.next_time = 0  # next time to advance the state (ms)
        self.highlight_end = 0  # when to clear the current highlight
        self.wait_delay = 0  # delay before showing "Your turn!"

        # Create buttons (with spacing and centered grid)
        self.buttons = []
        padding = 20

        grid_start_y = 210
        available_w = WIDTH - (padding * (self.grid_cols + 1))
        available_h = HEIGHT - grid_start_y - 120 - (padding * (self.grid_rows + 1))
        
        # Calculate size that fits both width and height
        size_w = available_w // self.grid_cols
        size_h = available_h // self.grid_rows
        button_size = min(size_w, size_h)
        
        # Center horizontally
        total_grid_w = (button_size * self.grid_cols) + (padding * (self.grid_cols - 1))
        start_x = (WIDTH - total_grid_w) // 2
        
        # Center vertically in the available area
        total_grid_h = (button_size * self.grid_rows) + (padding * (self.grid_rows - 1))
        start_y = grid_start_y + (available_h - total_grid_h) // 2
        
        for i, color in enumerate(self.colors):
            row = i // self.grid_cols
            col = i % self.grid_cols
            x = start_x + col * (button_size + padding)
            y = start_y + row * (button_size + padding)
            rect = pygame.Rect(x, y, button_size, button_size)
            self.buttons.append(ColorButton(rect, color))

        # Back button (always available during gameplay)
        from constants import HIGHLIGHT_COLOR
        self.back_button = TextButton(pygame.Rect(20, 20, 140, 44), "BACK", bg_color=HIGHLIGHT_COLOR)

        self._start_new_round()


    def _start_new_round(self):
        self.stage += 1
        
        # ใช้ Strategy Pattern ในการเจเนเรทลำดับสี
        new_color = self.strategy.generate_next(self.sequence, self.colors)
        self.sequence.append(new_color)

        self.player_input = []

        self.state = "showing"
        self.show_index = 0
        # Add a short delay before AI starts showing the sequence
        self.next_time = pygame.time.get_ticks() + 400  # 0.4 second delay
        self.highlight_end = 0
        self.wait_delay = 0

    def update(self, mouse_pos, events):
        for button in self.buttons:
            button.update_hover(mouse_pos)
        self.back_button.update_hover(mouse_pos)

        # Back button is always available during gameplay
        for event in events:
            if self.back_button.is_clicked(event):
                return "menu"

        # Handle Win/Lose Popups
        if self.state in ["won", "failed"]:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    center_y = HEIGHT // 2
                    is_win = self.state == "won"
                    btn_w, btn_h = 240, 55
                    
                    # Setup buttons rects
                    if is_win:
                        has_next = self.difficulty != "Hard"
                        y_start = center_y + (0 if has_next else 40)
                        next_r = pygame.Rect(WIDTH//2-btn_w//2, y_start, btn_w, btn_h)
                        retry_r = pygame.Rect(WIDTH//2-btn_w//2, y_start + (70 if has_next else 0), btn_w, btn_h)
                        menu_r = pygame.Rect(WIDTH//2-btn_w//2, y_start + (140 if has_next else 70), btn_w, btn_h)
                        
                        if has_next and next_r.collidepoint(event.pos): return "next"
                        if retry_r.collidepoint(event.pos): return "retry"
                        if menu_r.collidepoint(event.pos): return "menu"
                    else:
                        retry_r = pygame.Rect(WIDTH//2-btn_w//2, center_y + 20, btn_w, btn_h)
                        menu_r = pygame.Rect(WIDTH//2-btn_w//2, center_y + 90, btn_w, btn_h)
                        if retry_r.collidepoint(event.pos): return "retry"
                        if menu_r.collidepoint(event.pos): return "menu"
            return None

        # Show hover state only during player turn (to avoid confusion during AI turn)
        if self.state == "waiting":
            for button in self.buttons:
                if button._press_t == 0:
                    button.set_highlight(False, hover=button.is_hovered())
        else:
            for button in self.buttons:
                if button._press_t == 0:
                    button.set_highlight(False, hover=False)

        # Player input
        if self.state == "waiting":
            clicked = False
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for button in self.buttons:
                        if button.is_clicked(event):
                            self.sound_manager.play_player()
                            self.player_input.append(button.color_name)
                            button.set_highlight(True)
                            button.press()
                            
                            idx = len(self.player_input) - 1
                            if idx < len(self.sequence):
                                if self.player_input[idx] != self.sequence[idx]:
                                    self.state = "failed"
                                    # Clear highlights
                                    for b in self.buttons: b.set_highlight(False)
                                    clicked = True
                                    break
                            
                            if len(self.player_input) == len(self.sequence):
                                if self.stage >= MAX_STAGES:
                                    self.state = "won"
                                else:
                                    self._start_new_round()
                                clicked = True
                                break
                            clicked = True
                            break
                    if clicked:
                        break

        # AI showing sequence
        if self.state == "showing":
            now = pygame.time.get_ticks()

            # Clear highlight shortly after it appears so it doesn't stay on indefinitely
            if now >= self.highlight_end:
                for button in self.buttons:
                    if button._press_t == 0:
                        button.set_highlight(False)
                if self.show_index >= len(self.sequence):
                    self.wait_delay = now
                    self.state = "waiting"

            if now >= self.next_time:
                if self.show_index < len(self.sequence):
                    color = self.sequence[self.show_index]
                    for button in self.buttons:
                        if button.color_name == color:
                            button.set_highlight(True)
                            self.sound_manager.play_ai()
                            break
                    self.show_index += 1
                    self.next_time = now + self.ai_delay_ms
                    self.highlight_end = now + self.ai_delay_ms - 80
                else:
                    # No delay before switching to player turn
                    self.wait_delay = now  # Immediate start
                    self.state = "waiting"


        return None



    def get_state(self):
        return self.state