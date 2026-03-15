import pygame
from constants import WIDTH, HEIGHT, TEXT_COLOR, HIGHLIGHT_COLOR, font_main, font_small, MAX_STAGES

class GameView:
    """Handles rendering for the MemoryGame (Single Responsibility: View)."""
    def draw(self, surface, game):
        # Draw title and status
        title = font_main.render("MEMORY GAME", True, HIGHLIGHT_COLOR)
        surface.blit(title, (WIDTH//2 - title.get_width()//2, 20))

        status = font_small.render(f"Stage: {game.stage}/{MAX_STAGES}  |  {game.difficulty}", True, TEXT_COLOR)
        surface.blit(status, (WIDTH//2 - status.get_width()//2, 70))

        # Draw back button (always available)
        game.back_button.draw(surface)

        # Draw buttons
        for button in game.buttons:
            button.draw(surface)

        # Prompt text
        prompt_text = ""
        now = pygame.time.get_ticks()
        if game.state == "waiting" and now >= game.wait_delay:
            prompt_text = "Your turn!"
        elif game.state == "showing":
            prompt_text = "Watch carefully..."

        if prompt_text:
            prompt = font_small.render(prompt_text, True, HIGHLIGHT_COLOR if game.state == "waiting" else TEXT_COLOR)
            surface.blit(prompt, (WIDTH//2 - prompt.get_width()//2, 120))

        # Draw Overlay and Popup
        if game.state in ["won", "failed"]:
            from constants import MATCH_COLOR, FAIL_COLOR
            mouse_pos = pygame.mouse.get_pos()
            
            # Semi-transparent Overlay
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            surface.blit(overlay, (0, 0))
            
            is_win = game.state == "won"
            p_rect = pygame.Rect(WIDTH//2-200, HEIGHT//2-160, 400, 360 if is_win and game.difficulty != "Hard" else 280)
            pygame.draw.rect(surface, (30, 30, 60), p_rect, border_radius=30)
            pygame.draw.rect(surface, MATCH_COLOR if is_win else FAIL_COLOR, p_rect, 4, border_radius=30)
            
            title_t = "YOU WIN!" if is_win else "YOU LOSE!"
            title_s = font_main.render(title_t, True, MATCH_COLOR if is_win else FAIL_COLOR)
            surface.blit(title_s, (WIDTH//2 - title_s.get_width()//2, HEIGHT//2 - 120))
            
            # Buttons definition
            btns = []
            if is_win:
                if game.difficulty != "Hard": btns.append(("NEXT LEVEL", MATCH_COLOR))
                btns.append(("PLAY AGAIN", HIGHLIGHT_COLOR)); btns.append(("MAIN MENU", FAIL_COLOR))
            else:
                btns.append(("TRY AGAIN", MATCH_COLOR)); btns.append(("MAIN MENU", FAIL_COLOR))
            
            btn_w, btn_h = 240, 55
            y_off = HEIGHT//2 + (0 if is_win and game.difficulty != "Hard" else 20)
            for i, (label, color) in enumerate(btns):
                r = pygame.Rect(WIDTH//2-btn_w//2, y_off + i*(btn_h+15), btn_w, btn_h)
                is_h = r.collidepoint(mouse_pos)
                pygame.draw.rect(surface, HIGHLIGHT_COLOR if is_h else color, r, border_radius=15)
                ls = font_main.render(label, True, TEXT_COLOR)
                surface.blit(ls, (r.centerx-ls.get_width()//2, r.centery-ls.get_height()//2))
