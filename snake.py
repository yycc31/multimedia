#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Step 3 - 灰色陷阱：隨機出現時間 + 固定消失
import pygame
import time
import random

pygame.init()

WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
PURPLE = (128, 0, 128)
GRAY = (120, 120, 120)

DIS_WIDTH = 600
DIS_HEIGHT = 400
dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption('Python 貪吃蛇遊戲')

clock = pygame.time.Clock()

SNAKE_BLOCK = 10
BASE_SPEED = 15
SNAKE_SPEED = BASE_SPEED

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
    global SNAKE_SPEED

    game_over = False
    game_close = False

    x1 = DIS_WIDTH / 2
    y1 = DIS_HEIGHT / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1
    score = 0

    SNAKE_SPEED = BASE_SPEED

    foodx = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
    foody = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0

    # --- 加速果實  ---
    speed_food_x = None
    speed_food_y = None
    speed_food_delay = 10

    SPEED_FOOD_APPEAR = pygame.USEREVENT + 1
    SPEED_FOOD_DISAPPEAR = pygame.USEREVENT + 2
    SPEED_FOOD_BOOST_END = pygame.USEREVENT + 3

    pygame.time.set_timer(SPEED_FOOD_APPEAR, speed_food_delay * 1000) 

    is_speed_boosted = False
    boost_duration = 5

    # ===== 灰色陷阱 Step3：隨機出現（新）=====
    trap_food_x = None
    trap_food_y = None

    TRAP_APPEAR = pygame.USEREVENT + 4
    TRAP_DISAPPEAR = pygame.USEREVENT + 5

    TRAP_SHOW_MS = 2500
    TRAP_NEXT_MIN_MS = 6000
    TRAP_NEXT_MAX_MS = 10000

    pygame.time.set_timer(TRAP_APPEAR, 7000)  # 第一次 7 秒後出現

    while not game_over:

        while game_close == True:
            dis.fill(BLACK)
            message("Game Over! Press C-Play Again or Q-Quit", RED)
            your_score(score)
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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == SPEED_FOOD_APPEAR:
                if speed_food_x is None:
                    speed_food_x = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
                    speed_food_y = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
                    pygame.time.set_timer(SPEED_FOOD_DISAPPEAR, 3000)
                new_delay = random.randint(8, 12)
                pygame.time.set_timer(SPEED_FOOD_APPEAR, new_delay * 1000)

            elif event.type == SPEED_FOOD_DISAPPEAR:
                speed_food_x = None
                speed_food_y = None
                pygame.time.set_timer(SPEED_FOOD_DISAPPEAR, 0)

            elif event.type == SPEED_FOOD_BOOST_END:
                SNAKE_SPEED = BASE_SPEED
                is_speed_boosted = False
                pygame.time.set_timer(SPEED_FOOD_BOOST_END, 0)

            # ===== 灰色陷阱出現（隨機下次出現時間）=====
            elif event.type == TRAP_APPEAR:
                if trap_food_x is None:
                    trap_food_x = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
                    trap_food_y = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
                    pygame.time.set_timer(TRAP_DISAPPEAR, TRAP_SHOW_MS)

                next_delay = random.randint(TRAP_NEXT_MIN_MS, TRAP_NEXT_MAX_MS)
                pygame.time.set_timer(TRAP_APPEAR, next_delay)

            elif event.type == TRAP_DISAPPEAR:
                trap_food_x = None
                trap_food_y = None
                pygame.time.set_timer(TRAP_DISAPPEAR, 0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -SNAKE_BLOCK; y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = SNAKE_BLOCK; y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -SNAKE_BLOCK; x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = SNAKE_BLOCK; x1_change = 0

        if x1 >= DIS_WIDTH or x1 < 0 or y1 >= DIS_HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(BLACK)

        pygame.draw.rect(dis, RED, [foodx, foody, SNAKE_BLOCK, SNAKE_BLOCK])

        if speed_food_x is not None:
            pygame.draw.rect(dis, PURPLE, [speed_food_x, speed_food_y, SNAKE_BLOCK, SNAKE_BLOCK])

        if trap_food_x is not None:
            pygame.draw.rect(dis, GRAY, [trap_food_x, trap_food_y, SNAKE_BLOCK, SNAKE_BLOCK])

        snake_Head = [x1, y1]
        snake_List.append(snake_Head)

        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        for x in snake_List:
            pygame.draw.rect(dis, GREEN, [x[0], x[1], SNAKE_BLOCK, SNAKE_BLOCK])

        your_score(score)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
            foody = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
            Length_of_snake += 1
            score += 1

        if speed_food_x is not None and x1 == speed_food_x and y1 == speed_food_y:
            score += 10
            Length_of_snake += 1
            SNAKE_SPEED = BASE_SPEED + 5
            is_speed_boosted = True
            pygame.time.set_timer(SPEED_FOOD_BOOST_END, boost_duration * 1000)
            speed_food_x = None
            speed_food_y = None
            pygame.time.set_timer(SPEED_FOOD_DISAPPEAR, 0)

        clock.tick(SNAKE_SPEED)

    pygame.time.set_timer(SPEED_FOOD_APPEAR, 0)
    pygame.time.set_timer(SPEED_FOOD_DISAPPEAR, 0)
    pygame.time.set_timer(SPEED_FOOD_BOOST_END, 0)
    pygame.time.set_timer(TRAP_APPEAR, 0)
    pygame.time.set_timer(TRAP_DISAPPEAR, 0)

    pygame.quit()
    quit()

if __name__ == "__main__":
    gameLoop()


# In[ ]:




