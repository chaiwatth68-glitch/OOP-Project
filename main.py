import pygame
import random
import sys

# --- Configuration & Premium Theme ---
pygame.init()

WIDTH, HEIGHT = 600, 900
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("✨ Premium Simon Says")

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

DIFFICULTY_CONFIG = {
    "Easy": {"colors": ["red", "green", "blue", "yellow"], "grid": (2, 2), "speed": (600, 300)},
    "Medium": {"colors": ["red", "green", "blue", "yellow", "purple", "cyan"], "grid": (3, 2), "speed": (450, 200)},
    "Hard": {"colors": ["red", "green", "blue", "yellow", "purple", "cyan", "orange", "white"], "grid": (4, 2), "speed": (300, 150)}
}

# Typography
try:
    font_main = pygame.font.SysFont("Outfit", 32); font_title = pygame.font.SysFont("Outfit", 48, bold=True); font_small = pygame.font.SysFont("Outfit", 20)
except:
    font_main = pygame.font.SysFont("Arial", 32); font_title = pygame.font.SysFont("Arial", 48, bold=True); font_small = pygame.font.SysFont("Arial", 20)

MAX_STAGES = 7

def generate_buttons(difficulty_name):
    config = DIFFICULTY_CONFIG[difficulty_name]; color_keys = config["colors"]; rows, cols = config["grid"]
    padding = 25; grid_start_y = 240
    avail_w = WIDTH - (padding * (cols + 1)); avail_h = HEIGHT - grid_start_y - 120 - (padding * rows)
    sz = min(avail_w // cols, avail_h // rows)
    start_x = (WIDTH - ((sz * cols) + (padding * (cols-1)))) // 2
    return [{"name": c_n, "rect": pygame.Rect(start_x + (i%cols)*(sz+padding), grid_start_y + (i//cols)*(sz+padding), sz, sz)} for i, c_n in enumerate(color_keys)]

def draw_header(score, diff_name):
    title = font_title.render("SIMON SAYS", True, HIGHLIGHT_COLOR); screen.blit(title, (WIDTH//2 - title.get_width()//2, 40))
    st_text = f"Stage: {score}/{MAX_STAGES}  |  {diff_name}"; st_surf = font_main.render(st_text, True, TEXT_COLOR)
    screen.blit(st_surf, (WIDTH//2 - st_surf.get_width()//2, 100))

def draw_buttons(buttons, highlight=None, flash_type="AI"):
    for b in buttons:
        name, rect = b["name"], b["rect"]; is_h = (name == highlight); d_rect = rect.copy(); b_t, b_c = 4, (60, 60, 80)
        if is_h:
            if flash_type == "Player": d_rect = rect.inflate(10, 10); b_c = BRIGHT[name]; b_t = 6
            else: b_c = (255, 255, 255); b_t = 8
        s_rect = d_rect.copy(); s_rect.move_ip(6, 6); pygame.draw.rect(screen, (5, 5, 10), s_rect, border_radius=20)
        pygame.draw.rect(screen, BRIGHT[name] if is_h else COLORS[name], d_rect, border_radius=20)
        pygame.draw.rect(screen, b_c, d_rect, b_t, border_radius=20)

def draw_status(txt, clr=TEXT_COLOR):
    surf = font_main.render(txt, True, clr); screen.blit(surf, (WIDTH//2 - surf.get_width()//2, 182))

def main_menu():
    clock = pygame.time.Clock(); options = ["Easy", "Medium", "Hard"]; selected = 0
    while True:
        screen.fill(BG_COLOR); title = font_title.render("SELECT DIFFICULTY", True, HIGHLIGHT_COLOR)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        for i, opt in enumerate(options):
            clr = HIGHLIGHT_COLOR if i == selected else TEXT_COLOR
            txt = font_main.render(f"{'> ' if i == selected else '  '}{opt}", True, clr)
            rect = txt.get_rect(center=(WIDTH//2, 320 + i * 80)); screen.blit(txt, rect)
            if i == selected: pygame.draw.rect(screen, clr, rect.inflate(40, 10), 2, border_radius=10)
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP: selected = (selected - 1) % len(options)
                elif e.key == pygame.K_DOWN: selected = (selected + 1) % len(options)
                elif e.key == pygame.K_RETURN: return options[selected]
        clock.tick(FPS)

def run_game(diff_name):
    clock = pygame.time.Clock(); config = DIFFICULTY_CONFIG[diff_name]; f_t, p_t = config["speed"]
    color_pool = config["colors"]; buttons = generate_buttons(diff_name)
    sequence, p_seq, state, show_i, last_t, cur_f, f_type, score = [], [], "showing", 0, 0, None, "AI", 0
    
    def add_step(): sequence.append(random.choice(color_pool))
    def reset_r(): nonlocal show_i, cur_f, last_t, state, p_seq; show_i, cur_f, p_seq, last_t, state = 0, None, [], pygame.time.get_ticks(), "showing"
    add_step(); reset_r()

    while True:
        now = pygame.time.get_ticks(); screen.fill(BG_COLOR); m_pos = pygame.mouse.get_pos()
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if state == "playing" and e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                for b in buttons:
                    if b["rect"].collidepoint(e.pos):
                        cur_f, f_type, last_t = b["name"], "Player", now
                        if b["name"] == sequence[len(p_seq)]:
                            p_seq.append(b["name"])
                            if len(p_seq) == len(sequence): score += 1; state = "success"; last_t = now
                        else: state = "failed"
            
            if state in ["won", "failed"] and e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                # Logic for popup buttons
                center_y = HEIGHT // 2
                if state == "won":
                    btn_w, btn_h = 240, 55
                    has_next = diff_name != "Hard"
                    y_start = center_y + (0 if has_next else 40)
                    if has_next and pygame.Rect(WIDTH//2-btn_w//2, y_start, btn_w, btn_h).collidepoint(e.pos): return "next"
                    if pygame.Rect(WIDTH//2-btn_w//2, y_start + (70 if has_next else 0), btn_w, btn_h).collidepoint(e.pos): return "retry"
                    if pygame.Rect(WIDTH//2-btn_w//2, y_start + (140 if has_next else 70), btn_w, btn_h).collidepoint(e.pos): return "menu"
                else:
                    btn_w, btn_h = 240, 60
                    if pygame.Rect(WIDTH//2-btn_w//2, center_y + 20, btn_w, btn_h).collidepoint(e.pos): return "retry"
                    if pygame.Rect(WIDTH//2-btn_w//2, center_y + 100, btn_w, btn_h).collidepoint(e.pos): return "menu"

        if state == "showing":
            if cur_f is None:
                if now - last_t > p_t:
                    if show_i < len(sequence): cur_f, f_type, last_t = sequence[show_i], "AI", now
                    else: state = "playing"
            elif now - last_t > f_t: cur_f, show_i, last_t = None, show_i + 1, now
        elif state in ["playing", "success"]:
            if cur_f and now - last_t > 200:
                cur_f = None
                if state == "success":
                    if score >= MAX_STAGES: state = "won"
                    else: add_step(); reset_r()

        draw_header(score, diff_name); draw_buttons(buttons, highlight=cur_f, flash_type=f_type)
        if state == "showing": draw_status("Watch closely...", HIGHLIGHT_COLOR)
        elif state == "playing": draw_status("Your turn!", MATCH_COLOR)

        if state in ["won", "failed"]:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA); overlay.fill((0, 0, 0, 180)); screen.blit(overlay, (0, 0))
            is_win = state == "won"
            p_rect = pygame.Rect(WIDTH//2-200, HEIGHT//2-160, 400, 360 if is_win and diff_name != "Hard" else 300)
            pygame.draw.rect(screen, (30, 30, 60), p_rect, border_radius=30)
            pygame.draw.rect(screen, MATCH_COLOR if is_win else FAIL_COLOR, p_rect, 4, border_radius=30)
            
            title_t = "YOU WIN!" if is_win else "YOU LOSE!"
            title_s = font_title.render(title_t, True, MATCH_COLOR if is_win else FAIL_COLOR)
            screen.blit(title_s, (WIDTH//2 - title_s.get_width()//2, HEIGHT//2 - 120))
            
            # Popup Buttons
            btns = []
            if is_win:
                if diff_name != "Hard": btns.append(("NEXT LEVEL", MATCH_COLOR))
                btns.append(("PLAY AGAIN", HIGHLIGHT_COLOR)); btns.append(("MAIN MENU", FAIL_COLOR))
            else: btns.append(("TRY AGAIN", MATCH_COLOR)); btns.append(("MAIN MENU", FAIL_COLOR))
            
            btn_w, btn_h = 240, 55 if is_win else 60
            y_off = HEIGHT//2 + (0 if is_win and diff_name != "Hard" else 20)
            for i, (label, color) in enumerate(btns):
                r = pygame.Rect(WIDTH//2-btn_w//2, y_off + i*(btn_h+15), btn_w, btn_h)
                is_h = r.collidepoint(m_pos); pygame.draw.rect(screen, HIGHLIGHT_COLOR if is_h else color, r, border_radius=15)
                ls = font_main.render(label, True, TEXT_COLOR); screen.blit(ls, (r.centerx-ls.get_width()//2, r.centery-ls.get_height()//2))

        pygame.display.flip(); clock.tick(FPS)

if __name__ == "__main__":
    cur_d = None
    while True:
        if cur_d is None: cur_d = main_menu()
        res = run_game(cur_d)
        if res == "menu": cur_d = None
        elif res == "next":
            if cur_d == "Easy": cur_d = "Medium"
            elif cur_d == "Medium": cur_d = "Hard"
        # "retry" will just loop with same cur_d
