#增加紫色方塊
import pygame
import time
import random

# --- 初始化 Pygame ---
pygame.init()

# --- 顏色定義 (RGB) ---
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
PURPLE = (128, 0, 128)  # 新增紫色食物顏色

# --- 螢幕設定 ---
DIS_WIDTH = 600
DIS_HEIGHT = 400

dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption('Python 貪吃蛇遊戲')

clock = pygame.time.Clock()

# --- 蛇的參數 ---
SNAKE_BLOCK = 10  # 蛇的大小
SNAKE_SPEED = 15  # 蛇的移動速度

# --- 字型設定 ---
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def your_score(score):
    value = score_font.render("Score: " + str(score), True, YELLOW)
    dis.blit(value, [0, 0])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    text_rect = mesg.get_rect(center=(DIS_WIDTH/2, DIS_HEIGHT/2))
    dis.blit(mesg, text_rect)

def gameLoop():
    game_over = False
    game_close = False

    x1 = DIS_WIDTH / 2
    y1 = DIS_HEIGHT / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    # 隨機產生第一個紅色食物位置
    foodx = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
    foody = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0

    # 隨機產生第一個紫色食物位置
    speed_food_x = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
    speed_food_y = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0

    while not game_over:

        while game_close == True:
            dis.fill(BLACK)
            message("Game Over! Press C-Play Again or Q-Quit", RED)
            your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False

        # --- 按鍵控制 ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -SNAKE_BLOCK
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = SNAKE_BLOCK
                    x1_change = 0

        # --- 邊界檢查 (撞牆) ---
        if x1 >= DIS_WIDTH or x1 < 0 or y1 >= DIS_HEIGHT or y1 < 0:
            game_close = True
        
        x1 += x1_change
        y1 += y1_change
        dis.fill(BLACK)
        
        # 畫紅色食物
        pygame.draw.rect(dis, RED, [foodx, foody, SNAKE_BLOCK, SNAKE_BLOCK])
        # 畫紫色食物
        pygame.draw.rect(dis, PURPLE, [speed_food_x, speed_food_y, SNAKE_BLOCK, SNAKE_BLOCK])

        # 更新蛇的身體
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # --- 檢查撞到自己 ---
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        # 畫蛇
        for x in snake_List:
            pygame.draw.rect(dis, GREEN, [x[0], x[1], SNAKE_BLOCK, SNAKE_BLOCK])

        your_score(Length_of_snake - 1)
        pygame.display.update()

        # --- 吃紅色食物判定 ---
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
            foody = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
            Length_of_snake += 1

        # --- 吃紫色食物判定 ---
        if x1 == speed_food_x and y1 == speed_food_y:
            speed_food_x = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
            speed_food_y = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(SNAKE_SPEED)

    pygame.quit()
    quit()

# 啟動遊戲
if __name__ == "__main__":
    gameLoop()
