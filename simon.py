import pygame
import random
import sys

# --- Configuration ---
WIDTH, HEIGHT = 600, 600
FPS = 60

# Colors
COLORS = {
    "red": (200, 0, 0),
    "green": (0, 200, 0),
    "blue": (0, 0, 200),
    "yellow": (200, 200, 0),
}
BRIGHT = {
    "red": (255, 80, 80),
    "green": (80, 255, 80),
    "blue": (80, 80, 255),
    "yellow": (255, 255, 120),
}
BG_COLOR = (30, 30, 30)
TEXT_COLOR = (240, 240, 240)

# Game timing
FLASH_TIME = 600      # milliseconds each flash stays on
PAUSE_TIME = 250      # milliseconds between flashes

# Layout
PADDING = 20
BUTTON_SIZE = (WIDTH - (PADDING * 3)) // 2

# Map quadrant to colors
BUTTONS = [
    {"name": "red", "rect": pygame.Rect(PADDING, PADDING, BUTTON_SIZE, BUTTON_SIZE)},
    {"name": "green", "rect": pygame.Rect(PADDING * 2 + BUTTON_SIZE, PADDING, BUTTON_SIZE, BUTTON_SIZE)},
    {"name": "blue", "rect": pygame.Rect(PADDING, PADDING * 2 + BUTTON_SIZE, BUTTON_SIZE, BUTTON_SIZE)},
    {"name": "yellow", "rect": pygame.Rect(PADDING * 2 + BUTTON_SIZE, PADDING * 2 + BUTTON_SIZE, BUTTON_SIZE, BUTTON_SIZE)},
]


def draw_buttons(screen, highlight=None):
    for button in BUTTONS:
        name = button["name"]
        rect = button["rect"]
        color = BRIGHT[name] if name == highlight else COLORS[name]
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (220, 220, 220), rect, 4)


def draw_text(screen, text, y):
    font = pygame.font.SysFont("Arial", 30, bold=True)
    surf = font.render(text, True, TEXT_COLOR)
    screen.blit(surf, (WIDTH // 2 - surf.get_width() // 2, y))


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simon Says")
    clock = pygame.time.Clock()

    sequence = []
    player_index = 0
    state = "waiting"  # waiting, showing, playing, failed
    show_index = 0
    last_flash_time = 0
    current_flash = None
    score = 0

    def add_step():
        sequence.append(random.choice(list(COLORS.keys())))

    def start_round():
        nonlocal state, show_index, last_flash_time, current_flash, player_index
        player_index = 0
        show_index = 0
        current_flash = None
        last_flash_time = pygame.time.get_ticks() - PAUSE_TIME
        state = "showing"

    # Initial start
    add_step()
    start_round()

    while True:
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if state == "playing" and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                for button in BUTTONS:
                    if button["rect"].collidepoint(pos):
                        choice = button["name"]
                        # flash button immediately
                        current_flash = choice
                        last_flash_time = now

                        # validate
                        if choice == sequence[player_index]:
                            player_index += 1
                            if player_index >= len(sequence):
                                score += 1
                                add_step()
                                start_round()
                        else:
                            state = "failed"
                        break

            if state == "failed" and event.type == pygame.KEYDOWN:
                # Restart on any key
                sequence = []
                add_step()
                score = 0
                start_round()
                state = "showing"

        # State machine
        if state == "showing":
            if current_flash is None and now - last_flash_time >= PAUSE_TIME:
                # start next flash
                if show_index < len(sequence):
                    current_flash = sequence[show_index]
                    last_flash_time = now
                else:
                    state = "playing"
            elif current_flash is not None and now - last_flash_time >= FLASH_TIME:
                # end current flash
                current_flash = None
                show_index += 1
                last_flash_time = now

        # Draw
        screen.fill(BG_COLOR)
        draw_buttons(screen, highlight=current_flash)

        if state == "playing":
            draw_text(screen, f"Score: {score}", HEIGHT - 60)
        elif state == "showing":
            draw_text(screen, "Watch the sequence...", HEIGHT - 60)
        elif state == "failed":
            draw_text(screen, "Wrong! Press any key to retry", HEIGHT - 60)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    run_game()
