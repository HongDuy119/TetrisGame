import pygame # import pygame
from copy import deepcopy # -1 điểm không biết là gì
from random import choice, randrange  
import time

W, H = 10, 20 # width = 10, height = 20
TILE = 35 # size of cell
GAME_RES = W * TILE, H * TILE # size of window game
RES = 700, 700 # size of window
FPS = 45

file = 'B.mp3' # music 
pygame.init() 
pygame.mixer.init() # -1 điểm vì không biết là gì
pygame.mixer.music.load(file)
pygame.mixer.music.play()
pygame.event.wait()

# pygame.init()  -1 điểm vì khai báo đéo để làm gì
sc = pygame.display.set_mode(RES) # init window
game_sc = pygame.Surface(GAME_RES) # window play
clock = pygame.time.Clock() # time

grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)] # draw rectangle

figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)], # init point of rectangle
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]] 

figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos] # tạo viên gạch rơi trên xuống (array)
figure_rect = pygame.Rect(0, 0, TILE - 1, TILE - 1 ) # size mỗi ô vuông trong viên gạch -1 điểm vì trả lời sai 
field = [[0 for i in range(W)] for j in range(H)] 

pausing = False
#over 
def game_over():
    gfont = pygame.font.SysFont('cosolas',40)
    gsurf = gfont.render('Game over!',True, pygame.Color(255,0,0))
    grect = gsurf.get_rect()
    grect.midtop = (500,150)
    sc.blit(gsurf,grect)
    pygame.display.flip()
    time.sleep(10 )
    # pygame.quit()

anim_count, anim_speed, anim_limit = 0, 60, 3000
# anim_acount = ?
# anim_speed = speed 
# anima_limit = time delay start game ( 3000 = 3s )
bg = pygame.image.load('img/bg.jpg').convert() # load ảnh
game_bg = pygame.image.load('img/bg2.jpg').convert() # load ảnh


main_font = pygame.font.Font('font/font.ttf', 65) # load font 
font = pygame.font.Font('font/font.ttf', 45) # load font

title_tetris = main_font.render('TETRIS', True, pygame.Color('darkorange')) # init text
title_score = font.render('score:', True, pygame.Color('green')) # init text 
title_record = font.render('record:', True, pygame.Color('purple')) # init text

get_color = lambda : (randrange(1, 256), randrange(1, 200), randrange(1, 250)) # function random color brick

figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))  
color, next_color = get_color(), get_color() 

score, lines = 0, 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}


def check_borders():
    if figure[i].x < 0 or figure[i].x > W - 1:
        return False
    elif figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
        return False
    return True


def get_record(): # lấy score từ file
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')


def set_record(record, score): # viết score vào file
    rec = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(rec))

while True:
    record = get_record() # lấy score từ file
    dx, rotate = 0, False
    # draw background
    sc.blit(bg, (350, 0))
    sc.blit(game_sc, (0, 0))
    game_sc.blit(game_bg, (0, 0))
    # delay for full lines
    for i in range(lines):
        pygame.time.wait(200)
    # control
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -1
            elif event.key == pygame.K_RIGHT:
                dx = 1
            elif event.key == pygame.K_DOWN:
                anim_limit = 100
            elif event.key == pygame.K_SPACE:
                rotate = True
            elif event.key == pygame.K_p:
                pygame.K_PAUSE
            
                
    # move x
    figure_old = deepcopy(figure)
    for i in range(4):
        figure[i].x += dx
        if not check_borders():
            figure = deepcopy(figure_old)
            break
    # move y
    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not check_borders():
                for i in range(4):
                    field[figure_old[i].y][figure_old[i].x] = color
                figure, color = next_figure, next_color
                next_figure, next_color = deepcopy(choice(figures)), get_color()
                anim_limit = 2000
                break
    # rotate
    center = figure[0]
    figure_old = deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not check_borders():
                figure = deepcopy(figure_old)
                break
    # check lines
    line, lines = H - 1, 0
    for row in range(H - 1, -1, -1):
        count = 0
        for i in range(W):
            if field[row][i]:
                count += 1
            field[line][i] = field[row][i]
        if count < W:
            line -= 1
        else:
            anim_speed += 3
            lines += 1
    # compute score
    score += scores[lines]
    # draw grid
    [pygame.draw.rect(game_sc, (40, 40, 40), i_rect, 1) for i_rect in grid]
    # draw figure
    for i in range(4):
        figure_rect.x = figure[i].x * TILE
        figure_rect.y = figure[i].y * TILE
        pygame.draw.rect(game_sc, color, figure_rect)
    # draw field
    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = x * TILE, y * TILE
                pygame.draw.rect(game_sc, col, figure_rect)
    # draw next figure
    for i in range(4):
        figure_rect.x = next_figure[i].x * TILE + 340
        figure_rect.y = next_figure[i].y * TILE + 185
        pygame.draw.rect(sc, next_color, figure_rect)
    # draw titles
    sc.blit(title_tetris, (390, 20))
    sc.blit(title_score, (450, 490))
    sc.blit(font.render(str(score), True, pygame.Color('white')), (505, 570))
    sc.blit(title_record, (440, 320))
    sc.blit(font.render(record, True, pygame.Color('gold')), (465, 400))
    # game over
    for i in range(W):
        if field[0][i]:
            game_over()
            set_record(record, score)
            field = [[0 for i in range(W)] for i in range(H)]
            anim_count, anim_speed, anim_limit = 0, 60, 2000
            score = 0
            for i_rect in grid:
                pygame.draw.rect(game_sc, get_color(), i_rect)
                sc.blit(game_sc, (0, 0))
                pygame.display.flip()
                clock.tick(200)
    pygame.display.flip()
    clock.tick(FPS) 