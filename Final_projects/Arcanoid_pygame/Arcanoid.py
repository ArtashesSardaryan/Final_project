import pygame
from random import randrange as rnd
import sys

WIDTH, HEIGHT = 1200, 800
fps = 60
# paddle settings
paddle_w = 330
paddle_h = 35
paddle_speed = 15
paddle = pygame.Rect(WIDTH // 2 - paddle_w // 2, HEIGHT - paddle_h - 10, paddle_w, paddle_h)
# ball settings
ball_radius = 20
ball_speed = 6
score = 0
lifes = 3
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
dx, dy = 1, -1
# blocks settings
block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(10) for j in range(4)]

pygame.init()
pygame.mixer.init()

sc = pygame.display.set_mode((WIDTH, HEIGHT))
sound = pygame.mixer.Sound('colide.mp3')
game_over_sound_= pygame.mixer.Sound('game_oversound.mp3')
win_sound= pygame.mixer.Sound('win_sound.mp3')
clock = pygame.time.Clock()

font_score = pygame.font.SysFont('Arial',26,bold=True)
font_win = pygame.font.SysFont('Arial',80,bold=True)
font_pause = pygame.font.SysFont('Arial',26,bold=True)

# background image
img = pygame.image.load('1.jpg').convert()
def show_menu():
    menu_background = pygame.image.load("menu.jpg")

def detect_collision(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    sc.blit(img, (0, 0))
    # drawing world
    [pygame.draw.rect(sc, color_list[color], block) for color, block in enumerate(block_list)]
    pygame.draw.rect(sc, pygame.Color('darkorange'), paddle)
    pygame.draw.circle(sc, pygame.Color('white'), ball.center, ball_radius)
    # ball movement
    ball.x += ball_speed * dx
    ball.y += ball_speed * dy
    # collision left right
    if ball.centerx < ball_radius or ball.centerx > WIDTH - ball_radius:
        dx =-dx    
    # collision top
    if ball.centery < ball_radius:
        dy = -dy
    # collision paddle
    if ball.colliderect(paddle) and dy > 0:
        dx, dy = detect_collision(dx, dy, ball, paddle)
        # if dx > 0:
        #     dx, dy = (-dx, -dy) if ball.centerx < paddle.centerx else (dx, -dy)
        # else:
        #     dx, dy = (-dx, -dy) if ball.centerx >= paddle.centerx else (dx, -dy)
    # collision blocks
    hit_index = ball.collidelist(block_list)
    if hit_index != -1:
        hit_rect = block_list.pop(hit_index)
        hit_color = color_list.pop(hit_index)
        dx, dy = detect_collision(dx, dy, ball, hit_rect)
        # special effect
        hit_rect.inflate_ip(ball.width * 3, ball.height * 3)
        pygame.draw.rect(sc, hit_color, hit_rect)
        fps += 2
        score += 1
        sound.play()
    #Score renrede
    render_score = font_score.render(f'SCORE:{score}',1, pygame.Color('orange'))
    sc.blit(render_score,(20,700))
    render_lifes = font_score.render(f'LIVES:{lifes}',1, pygame.Color('orange'))
    sc.blit(render_lifes,(1100,700))
    # win, game over
    if ball.bottom > HEIGHT:
        lifes -= 1
        ball_speed = 6
        ball.x, ball.y = 600, 550
        paddle.x, paddle.y = WIDTH // 2 - paddle_w // 2, HEIGHT - paddle_h - 10
        while True:
            render_pause = font_pause.render("PRESS SPACE", 1 ,pygame.Color('orange'))
            sc.blit(render_pause, (WIDTH//2-80,450))
            pygame.display.flip()
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                break
        if lifes <= 0:
            while True:
                render_win = font_win.render("GAME OVER!", 1 ,pygame.Color('orange'))
                sc.blit(render_win, (WIDTH//2-180,HEIGHT//2-65))
                pygame.display.flip()
                game_over_sound_.play()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()

    elif not len(block_list):
        while True:
            render_win = font_win.render("WINNER!", 1 ,pygame.Color('orange'))
            sc.blit(render_win, (WIDTH//2,HEIGHT//2))
            pygame.display.flip()
            win_sound.play()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
        
    # control
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= paddle_speed
    if key[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.right += paddle_speed
    # update screen
    pygame.display.flip()
    clock.tick(fps)