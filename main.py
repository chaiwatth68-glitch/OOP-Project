import pygame
import random

# 1. ตั้งค่าพื้นฐาน
pygame.init()
WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Game - จับคู่ตัวเลข")
font = pygame.font.SysFont("Arial", 36)

# สี
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (50, 50, 255)

# 2. สร้างข้อมูลเกม (ตาราง 4x4 = 16 ใบ)
rows, cols = 4, 4
card_size = 80
margin = 15

# สร้างคู่ตัวเลข 1-8 (อย่างละ 2 ใบ) แล้วสุ่มตำแหน่ง
numbers = list(range(1, 9)) * 2
random.shuffle(numbers)

# เก็บสถานะไพ่: [ตัวเลข, หงายอยู่ไหม, จับคู่ได้แล้วหรือยัง]
cards = []
for i in range(16):
    x = (i % cols) * (card_size + margin) + margin
    y = (i // cols) * (card_size + margin) + margin
    cards.append({'rect': pygame.Rect(x, y, card_size, card_size), 
                  'val': numbers[i], 'flipped': False, 'matched': False})

# ตัวแปรควบคุมการคลิก
selected_cards = []
waiting = False
timer = 0

# 3. Game Loop
running = True
while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # คลิกเมาส์ (เฉพาะตอนที่ไม่รอคว่ำไพ่)
        if event.type == pygame.MOUSEBUTTONDOWN and not waiting:
            for card in cards:
                if card['rect'].collidepoint(event.pos) and not card['flipped'] and not card['matched']:
                    card['flipped'] = True
                    selected_cards.append(card)
                    
                    if len(selected_cards) == 2:
                        waiting = True
                        timer = pygame.time.get_ticks()

    # ตรวจสอบการจับคู่ (เมื่อหงายครบ 2 ใบแล้วผ่านไป 1 วินาที)
    if waiting:
        if pygame.time.get_ticks() - timer > 1000: # รอ 1 วินาทีให้เห็นไพ่
            c1, c2 = selected_cards
            if c1['val'] == c2['val']:
                c1['matched'] = c2['matched'] = True
            else:
                c1['flipped'] = c2['flipped'] = False
            selected_cards = []
            waiting = False

    # 4. วาดไพ่
    for card in cards:
        if card['flipped'] or card['matched']:
            pygame.draw.rect(screen, GRAY, card['rect'])
            text = font.render(str(card['val']), True, BLACK)
            text_rect = text.get_rect(center=card['rect'].center)
            screen.blit(text, text_rect)
        else:
            pygame.draw.rect(screen, BLUE, card['rect'])

    pygame.display.flip()

pygame.quit()