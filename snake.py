#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Step 5 - 灰色陷阱：避免跟紅/紫重疊 + 完整清理 timer
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

OBSTACLE_COUNT = 2
OBSTACLE_START_EAT = 5

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def your_score(score):
    value = score_font.render("Score: " + str(score), True, YELLOW)
    dis.blit(value, [0, 0])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    text_rect = mesg.get_rect(center=(DIS_WIDTH/2, DIS_HEIGHT/2))
    dis.blit(mesg, text_rect)

def rand_grid_pos():
    x = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
    y = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
    return x, y

def rand_grid_pos_excluding(occupied):
    while True:
        x, y = rand_grid_pos()
        if (x, y) not in occupied:
            return x, y
            
def spawn_obstacles(count, occupied):
    obstacles = set()
    while len(obstacles) < count:
        pos = rand_grid_pos()
        if pos not in occupied:
            obstacles.add(pos)
    return obstacles

def build_occupied_for_obstacles(snake_List, head_pos, food_pos, speed_pos, trap_pos):
    occupied = set((seg[0], seg[1]) for seg in snake_List)
    occupied.add(head_pos)
    occupied.add(food_pos)
    if speed_pos is not None:
        occupied.add(speed_pos)
    if trap_pos is not None:
        occupied.add(trap_pos)
    return occupied

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

    SNAKE_SPEED = BASE_SPEED  # 重新設定初始速度

    obstacles = set()

    # --- 正常食物 ---
    foodx = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
    foody = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0

    # --- 加速果實  ---
    speed_food_x = None  # 紫色食物 X 座標
    speed_food_y = None  # 紫色食物 Y 座標
    speed_food_delay = 10 # 初始出現間隔 (秒)

    # 自訂事件
    SPEED_FOOD_APPEAR = pygame.USEREVENT + 1  # 紫色食物出現事件
    SPEED_FOOD_DISAPPEAR = pygame.USEREVENT + 2  # 紫色食物消失事件
    SPEED_FOOD_BOOST_END = pygame.USEREVENT + 3  # 加速結束事件

    # 設置紫色食物第一次出現的計時器
    pygame.time.set_timer(SPEED_FOOD_APPEAR, speed_food_delay * 1000) 

    is_speed_boosted = False
    boost_duration = 5 # 加速持續時間 (秒)

    def maybe_refresh_obstacles_after_eat():
        nonlocal obstacles

        if total_eaten < OBSTACLE_START_EAT:
            obstacles = set()
            return

        head_pos = (x1, y1)
        food_pos = (foodx, foody)
        speed_pos = (speed_food_x, speed_food_y) if speed_food_x is not None else None
        trap_pos = (trap_food_x, trap_food_y) if trap_food_x is not None else None

        occupied = build_occupied_for_obstacles(
            snake_List=snake_List,
            head_pos=head_pos,
            food_pos=food_pos,
            speed_pos=speed_pos,
            trap_pos=trap_pos
        )
        obstacles = spawn_obstacles(OBSTACLE_COUNT, occupied)

     def refresh_fruits_after_eat():
        nonlocal speed_food_x, speed_food_y, trap_food_x, trap_food_y

        occupied = set((seg[0], seg[1]) for seg in snake_List)
        occupied |= obstacles
        occupied.add((x1, y1))
        occupied.add((foodx, foody))

        # 先生成加速果實
        speed_food_x, speed_food_y = rand_grid_pos_excluding(occupied)
        occupied.add((speed_food_x, speed_food_y))

        # 再生成陷阱食物（避免跟加速果實重疊）
        trap_food_x, trap_food_y = rand_grid_pos_excluding(occupied)
    
    # ===== 灰色陷阱 Step5（最終）=====
    trap_food_x = None
    trap_food_y = None

    TRAP_APPEAR = pygame.USEREVENT + 4
    TRAP_DISAPPEAR = pygame.USEREVENT + 5

    TRAP_SHOW_MS = 2500
    TRAP_NEXT_MIN_MS = 6000
    TRAP_NEXT_MAX_MS = 10000
    TRAP_PENALTY = 5

    pygame.time.set_timer(TRAP_APPEAR, 7000)

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

        # --- 事件處理 ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            # 紫色食物出現
            if event.type == SPEED_FOOD_APPEAR:
                if speed_food_x is None:
                    speed_food_x = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
                    speed_food_y = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
                    # 出現後3秒自動消失
                    pygame.time.set_timer(SPEED_FOOD_DISAPPEAR, 3000)
                # 隨機設定下一次出現間隔 (8~12秒)
                new_delay = random.randint(8, 12)
                pygame.time.set_timer(SPEED_FOOD_APPEAR, new_delay * 1000)

            # 紫色食物消失
            elif event.type == SPEED_FOOD_DISAPPEAR:
                speed_food_x = None
                speed_food_y = None
                pygame.time.set_timer(SPEED_FOOD_DISAPPEAR, 0)

            # 加速結束，恢復原速
            elif event.type == SPEED_FOOD_BOOST_END:
                SNAKE_SPEED = BASE_SPEED
                is_speed_boosted = False
                pygame.time.set_timer(SPEED_FOOD_BOOST_END, 0)

            # ===== 灰色陷阱出現：避免跟紅/紫重疊（新）=====
            elif event.type == TRAP_APPEAR:
                if trap_food_x is None:
                    avoid = {(foodx, foody)}
                    if speed_food_x is not None:
                        avoid.add((speed_food_x, speed_food_y))
                    trap_food_x, trap_food_y = rand_grid_pos_avoid(avoid)
                    pygame.time.set_timer(TRAP_DISAPPEAR, TRAP_SHOW_MS)

                next_delay = random.randint(TRAP_NEXT_MIN_MS, TRAP_NEXT_MAX_MS)
                pygame.time.set_timer(TRAP_APPEAR, next_delay)

            elif event.type == TRAP_DISAPPEAR:
                trap_food_x = None
                trap_food_y = None
                pygame.time.set_timer(TRAP_DISAPPEAR, 0)

            # 按鍵控制
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

        # 畫紫色食物 (如果存在)
        if speed_food_x is not None:
            pygame.draw.rect(dis, PURPLE, [speed_food_x, speed_food_y, SNAKE_BLOCK, SNAKE_BLOCK])

        # 畫灰色陷阱（若存在）
        if trap_food_x is not None:
            pygame.draw.rect(dis, GRAY, [trap_food_x, trap_food_y, SNAKE_BLOCK, SNAKE_BLOCK])

        # 更新蛇的身體
        snake_Head = [x1, y1]
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

        your_score(score)
        pygame.display.update()

        # --- 吃紅色食物判定 ---
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
            foody = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
            Length_of_snake += 1
            score += 1

            # 新正常食物：避開蛇身 + 障礙物 +（若有）加速/陷阱 + 蛇頭
            occupied = set((seg[0], seg[1]) for seg in snake_List) | obstacles | {(x1, y1)}
            if speed_food_x is not None:
                occupied.add((speed_food_x, speed_food_y))
            if trap_food_x is not None:
                occupied.add((trap_food_x, trap_food_y))
            foodx, foody = rand_grid_pos_excluding(occupied)

        # --- 吃紫色食物判定 ---
        if speed_food_x is not None and x1 == speed_food_x and y1 == speed_food_y:
            score += 10
            Length_of_snake += 1
            # 觸發加速
            SNAKE_SPEED = BASE_SPEED + 5
            is_speed_boosted = True
            # 設置5秒後加速結束
            pygame.time.set_timer(SPEED_FOOD_BOOST_END, boost_duration * 1000)
            # 移除紫色食物
            speed_food_x = None
            speed_food_y = None
            pygame.time.set_timer(SPEED_FOOD_DISAPPEAR, 0)

        # ===== 吃灰色陷阱：扣分 + 立刻消失（新）=====
        if trap_food_x is not None and x1 == trap_food_x and y1 == trap_food_y:
            score = max(0, score - TRAP_PENALTY)
            trap_food_x = None
            trap_food_y = None
            pygame.time.set_timer(TRAP_DISAPPEAR, 0)

        if ate_anything:
            total_eaten += 1
            maybe_refresh_obstacles_after_eat()
            refresh_fruits_after_eat()
        
        clock.tick(SNAKE_SPEED)

    # 停止所有計時器
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











