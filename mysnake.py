import pygame
import random
import sys
import os

# 1. Setup - Window Size
pygame.init()
WIDTH, HEIGHT = 1200, 550
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('Ultimate Snake - Final Edition')
clock = pygame.time.Clock()

# Colors
BLACK, WHITE, RED = (0, 0, 0), (255, 255, 255), (255, 0, 0)
GREEN, YELLOW, BLUE = (76, 175, 80), (255, 215, 0), (33, 150, 243)

# Food Emojis
FOOD_EMOJIS = ["🍎", "🍔", "🍕", "🍓", "🍩", "🍦", "🍉", "🍍", "🍇", "🌮", "🍰"]
HS_FILE = "high_score.txt"

def load_hs():
    if not os.path.exists(HS_FILE): return 0
    with open(HS_FILE, "r") as f:
        try: return int(f.read())
        except: return 0

def save_hs(score):
    if score > load_hs():
        with open(HS_FILE, "w") as f: f.write(str(score))

def draw_text(text, size, color, x, y, is_emoji=False):
    font_name = "Segoe UI Emoji" if is_emoji else "consolas"
    font = pygame.font.SysFont(font_name, size, bold=True)
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(x, y))
    SCREEN.blit(surf, rect)
    return rect

def game_menu():
    while True:
        W, H = SCREEN.get_size()
        SCREEN.fill(BLACK)
        draw_text("SNAKE WORLD", 80, GREEN, W//2, H//4)
        draw_text(f"HIGH SCORE: {load_hs()}", 30, YELLOW, W//2, H//2 - 60)
        
        start_btn = pygame.Rect(W//2 - 150, H//2 + 20, 300, 60)
        quit_btn = pygame.Rect(W//2 - 150, H//2 + 100, 300, 60)
        
        m_pos = pygame.mouse.get_pos()
        pygame.draw.rect(SCREEN, (50, 150, 50) if start_btn.collidepoint(m_pos) else GREEN, start_btn, border_radius=10)
        pygame.draw.rect(SCREEN, (150, 0, 0) if quit_btn.collidepoint(m_pos) else RED, quit_btn, border_radius=10)
        
        draw_text("START (S)", 30, WHITE, W//2, H//2 + 50)
        draw_text("QUIT (Q)", 30, WHITE, W//2, H//2 + 130)
        
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.VIDEORESIZE:
                pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.collidepoint(event.pos): return
                if quit_btn.collidepoint(event.pos): pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s: return
                if event.key == pygame.K_q: pygame.quit(); sys.exit()

def main_game():
    W, H = SCREEN.get_size()
    snake_pos = [200, 200]
    snake_body = [[200, 200], [180, 200], [160, 200]]
    food_pos = [random.randrange(1, (W//20)) * 20, random.randrange(1, (H//20)) * 20]
    current_emoji = random.choice(FOOD_EMOJIS)
    
    direction, change_to = 'RIGHT', 'RIGHT'
    score, current_speed = 0, 5  # Speed 5 Fixed
    snake_color = GREEN
    game_over = False

    while True:
        W, H = SCREEN.get_size()
        SCREEN.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key == pygame.K_UP and direction != 'DOWN': change_to = 'UP'
                    elif event.key == pygame.K_DOWN and direction != 'UP': change_to = 'DOWN'
                    elif event.key == pygame.K_LEFT and direction != 'RIGHT': change_to = 'LEFT'
                    elif event.key == pygame.K_RIGHT and direction != 'LEFT': change_to = 'RIGHT'
                else:
                    if event.key == pygame.K_r: main_game()
                    if event.key == pygame.K_q: return

        if not game_over:
            direction = change_to
            if direction == 'UP': snake_pos[1] -= 20
            elif direction == 'DOWN': snake_pos[1] += 20
            elif direction == 'LEFT': snake_pos[0] -= 20
            elif direction == 'RIGHT': snake_pos[0] += 20

            snake_body.insert(0, list(snake_pos))
            
            if abs(snake_pos[0] - food_pos[0]) < 20 and abs(snake_pos[1] - food_pos[1]) < 20:
                score += 10; current_speed += 0.4
                snake_color = (random.randint(50,255), random.randint(50,255), random.randint(50,255))
                current_emoji = random.choice(FOOD_EMOJIS)
                food_pos = [random.randrange(1, (W//20)) * 20, random.randrange(1, (H//20)) * 20]
            else: snake_body.pop()

            draw_text(current_emoji, 25, WHITE, food_pos[0]+10, food_pos[1]+10, is_emoji=True)

            for i, pos in enumerate(snake_body):
                color = WHITE if i == 0 else snake_color
                pygame.draw.rect(SCREEN, color, pygame.Rect(pos[0], pos[1], 18, 18), border_radius=4)
                if i == 0: # Double Eyes
                    eye_col = RED
                    if direction in ['RIGHT', 'LEFT']:
                        pygame.draw.circle(SCREEN, eye_col, (pos[0]+10, pos[1]+5), 3)
                        pygame.draw.circle(SCREEN, eye_col, (pos[0]+10, pos[1]+13), 3)
                    else:
                        pygame.draw.circle(SCREEN, eye_col, (pos[0]+5, pos[1]+10), 3)
                        pygame.draw.circle(SCREEN, eye_col, (pos[0]+13, pos[1]+10), 3)

            if snake_pos[0]<0 or snake_pos[0]>W-20 or snake_pos[1]<0 or snake_pos[1]>H-20: game_over = True
            for block in snake_body[1:]:
                if snake_pos == block: game_over = True
            
            if game_over: save_hs(score)
            draw_text(f'SCORE: {score} | BEST: {load_hs()}', 22, YELLOW, 150, 30)
        else:
            draw_text(f"FINAL SCORE: {score}", 50, RED, W//2, H//3)
            r_btn = pygame.draw.rect(SCREEN, GREEN, (W//2 - 160, H//2 + 40, 150, 50), border_radius=8)
            m_btn = pygame.draw.rect(SCREEN, BLUE, (W//2 + 10, H//2 + 40, 150, 50), border_radius=8)
            draw_text("RESTART(R)", 20, WHITE, W//2 - 85, H//2 + 65)
            draw_text("MENU (Q)", 20, WHITE, W//2 + 85, H//2 + 65)
            if pygame.mouse.get_pressed()[0]:
                m_p = pygame.mouse.get_pos()
                if r_btn.collidepoint(m_p): main_game()
                if m_btn.collidepoint(m_p): return

        pygame.display.update()
        clock.tick(current_speed)

if __name__ == '__main__':
    while True:
        game_menu()
        main_game()
