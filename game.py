# game.py - Main Simon game logic

import random
import pygame
from constants import WIDTH, HEIGHT, DIFFICULTY_CONFIG, MAX_STAGES, TEXT_COLOR, HIGHLIGHT_COLOR, font_main, font_small
from button import ColorButton

class SimonGame:
    """Main game logic (Encapsulation: game state management)."""
    def __init__(self, difficulty, sound_manager):
        self.difficulty = difficulty
        self.sound_manager = sound_manager
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
        margin = 32
        available_width = WIDTH - margin * (self.grid_cols + 1)
        available_height = (HEIGHT - 240) - margin * (self.grid_rows + 1)
        button_width = available_width // self.grid_cols
        button_height = available_height // self.grid_rows
        grid_top = 180

        for i, color in enumerate(self.colors):
            row = i // self.grid_cols
            col = i % self.grid_cols
            x = margin + col * (button_width + margin)
            y = grid_top + margin + row * (button_height + margin)
            rect = pygame.Rect(x, y, button_width, button_height)
            self.buttons.append(ColorButton(rect, color))

        self._start_new_round()

    def _start_new_round(self):
        self.stage += 1
        self.sequence.append(random.choice(self.colors))
        self.player_input = []
        self.state = "showing"
        self.show_index = 0
        # Add a short delay before AI starts showing the sequence
        self.next_time = pygame.time.get_ticks() + 800  # 0.8 second delay
        self.highlight_end = 0
        self.wait_delay = 0

    def update(self, mouse_pos, event):
        for button in self.buttons:
            button.update_hover(mouse_pos)

        # Show hover state only during player turn (to avoid confusion during AI turn)
        if self.state == "waiting":
            for button in self.buttons:
                button.set_highlight(False, hover=button.is_hovered())
        else:
            for button in self.buttons:
                button.set_highlight(False, hover=False)

        # Player input
        if self.state == "waiting" and event and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.buttons:
                if button.is_clicked(event):
                    self.sound_manager.play_player()
                    self.player_input.append(button.color_name)
                    button.set_highlight(True)
                    button.press()
                    self.next_time = pygame.time.get_ticks() + self.player_delay_ms
                    self.state = "checking"
                    break

        # AI showing sequence
        if self.state == "showing":
            now = pygame.time.get_ticks()

            # Clear highlight shortly after it appears so it doesn't stay on indefinitely
            if now >= self.highlight_end:
                for button in self.buttons:
                    button.set_highlight(False)

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
                    self.highlight_end = now + (self.ai_delay_ms // 2)
                else:
                    # Add delay before switching to player turn
                    self.wait_delay = now + 600  # 0.6 second delay
                    self.state = "waiting"

        # Check player input timing
        elif self.state == "checking":
            now = pygame.time.get_ticks()
            if now >= self.next_time:
                for button in self.buttons:
                    button.set_highlight(False)
                if len(self.player_input) == len(self.sequence):
                    if self.player_input == self.sequence:
                        if self.stage >= MAX_STAGES:
                            self.state = "won"
                        else:
                            self._start_new_round()
                    else:
                        self.state = "failed"
                else:
                    self.state = "waiting"

    def draw(self, surface):
        # Draw title and status
        title = font_main.render("SIMON SAYS", True, HIGHLIGHT_COLOR)
        surface.blit(title, (WIDTH//2 - title.get_width()//2, 20))

        status = font_small.render(f"Stage: {self.stage}/{MAX_STAGES}  |  {self.difficulty}", True, TEXT_COLOR)
        surface.blit(status, (WIDTH//2 - status.get_width()//2, 70))

        # Draw buttons
        for button in self.buttons:
            button.draw(surface)

        # Prompt text
        prompt_text = ""
        now = pygame.time.get_ticks()
        if self.state == "waiting" and now >= self.wait_delay:
            prompt_text = "Your turn!"
        elif self.state == "showing":
            prompt_text = "Watch carefully..."
        elif self.state == "won":
            prompt_text = "You win!"
        elif self.state == "failed":
            prompt_text = "Wrong move!"

        if prompt_text:
            prompt = font_small.render(prompt_text, True, HIGHLIGHT_COLOR if self.state == "waiting" else TEXT_COLOR)
            surface.blit(prompt, (WIDTH//2 - prompt.get_width()//2, 120))

    def get_state(self):
        return self.state