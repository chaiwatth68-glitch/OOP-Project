# constants.py - Game constants and configurations

import pygame

# Window settings
WIDTH, HEIGHT = 600, 900
FPS = 60

# Colors (Premium Palette)
BG_COLOR = (15, 15, 26)       # Deep Dark Blue
TEXT_COLOR = (240, 240, 255)
HIGHLIGHT_COLOR = (80, 120, 255) # Vibrant Blue
MATCH_COLOR = (46, 204, 113)  # Emerald Green
FAIL_COLOR = (255, 107, 107)  # Coral Red

# Expanded Simon Colors
COLORS = {
    "red": (180, 40, 40), "green": (40, 150, 40), "blue": (40, 40, 180), "yellow": (180, 180, 40),
    "purple": (150, 40, 150), "cyan": (40, 150, 150), "orange": (180, 100, 40), "white": (180, 180, 180)
}
BRIGHT = {
    "red": (255, 80, 80), "green": (80, 255, 80), "blue": (80, 80, 255), "yellow": (255, 255, 120),
    "purple": (220, 100, 220), "cyan": (100, 255, 255), "orange": (255, 180, 80), "white": (255, 255, 255)
}

# Speed values are in milliseconds (ms). This keeps timing consistent even if FPS fluctuates.
DIFFICULTY_CONFIG = {
    "Easy": {"colors": ["red", "green", "blue", "yellow"], "grid": (2, 2), "speed": (1000, 350)},
    "Medium": {"colors": ["red", "green", "blue", "yellow", "purple", "cyan"], "grid": (3, 2), "speed": (1000, 350)},
    "Hard": {"colors": ["red", "green", "blue", "yellow", "purple", "cyan", "orange", "white"], "grid": (4, 2), "speed": (800, 300)}
}

MAX_STAGES = 10

# Initialize Pygame components
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("✨ Premium Memory Game")

# Typography
try:
    font_main = pygame.font.SysFont("Outfit", 32)
    font_title = pygame.font.SysFont("Outfit", 48, bold=True)
    font_small = pygame.font.SysFont("Outfit", 20)
except:
    font_main = pygame.font.SysFont("Arial", 32)
    font_title = pygame.font.SysFont("Arial", 48, bold=True)
    font_small = pygame.font.SysFont("Arial", 20)