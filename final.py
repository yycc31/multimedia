import pygame
import random

# --- 初始化 Pygame ---
pygame.init()

# --- 顏色定義 (RGB) ---
bak = (240,240,240)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 50)
BLACK = (0, 0, 0)
RED = (213, 50, 80)       # 正常食物
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
PURPLE = (128, 0, 128)    # 加速果實
GRAY = (120, 120, 120)    # 陷阱食物
OBST = (90, 90, 90)       # 障礙物顏色

# --- 螢幕設定 ---
DIS_WIDTH = 600
DIS_HEIGHT = 400

dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption('Python 貪吃蛇遊戲')

clock = pygame.time.Clock()

# --- 蛇的參數 ---
SNAKE_BLOCK = 10
BASE_SPEED = 15
SNAKE_SPEED = BASE_SPEED

# --- 障礙物參數 ---
OBSTACLE_COUNT = 2        # 每次出現的障礙物數量（可調）
OBSTACLE_START_EAT = 5    # 吃到正常食物第幾次後才開始有障礙物

# --- 字型設定 ---
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def your_score(score):
    value = score_font.render("Score: " + str(score), True, GRAY)
    dis.blit(value, [0, 0])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    text_rect = mesg.get_rect(center=(DIS_WIDTH/2, DIS_HEIGHT/2))
    dis.blit(mesg, text_rect)

def rand_grid_pos():
    """回傳對齊 10 格的隨機座標"""
    x = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
    y = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
    return x, y

def rand_grid_pos_excluding(occupied):
    """回傳對齊 10 格的隨機座標，但要避開 occupied set 內的座標"""
    while True:
        x, y = rand_grid_pos()
        if (x, y) not in occupied:
            return x, y

def spawn_obstacles(count, occupied):
    """生成 count 個障礙物（set of tuples），避開 occupied"""
    obstacles = set()
    while len(obstacles) < count:
        pos = rand_grid_pos()
        if pos not in occupied:
            obstacles.add(pos)
    return obstacles

def build_occupied_for_obstacles(snake_List, head_pos, food_pos, speed_pos, trap_pos):
    """彙整障礙物生成時不能佔用的位置"""
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

    # 用來計算「成功吃到正常食物」次數（你要的那個 5）
    total_eaten = 0

    # 初始速度
    SNAKE_SPEED = BASE_SPEED

    # --- 障礙物：一開始不生成 ---
    obstacles = set()

    # --- 正常食物：一開始就有 ---
    foodx, foody = rand_grid_pos_excluding({(x1, y1)})

    # --- 加速果實 / 陷阱食物：一開始都不生成（你要的）---
    speed_food_x = None
    speed_food_y = None
    trap_food_x = None
    trap_food_y = None

    # --- 加速效果維持（只保留效果計時器，不再用來生成果實）---
    boost_duration = 5
    SPEED_RESET = pygame.USEREVENT + 1
    trap_penalty = 5

    def maybe_refresh_obstacles_after_eat():
        """只要吃到任何東西就換障礙物位置；但前 5 次正常食物前不出障礙物。"""
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
        """
        你要的規則：
        不用定時器亂出現；
        每次「吃到任何東西」後才生成（或換位置）加速果實 + 陷阱食物。
        """
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

    while not game_over:

        # --- 遊戲結束畫面 ---
        while game_close:
            dis.fill(BLACK)
            message("Game Over! Press C-Play Again or Q-Quit", RED)
            your_score(score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        # --- 事件處理 ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            # ===== 加速效果到期：回復速度 =====
            if event.type == SPEED_RESET:
                SNAKE_SPEED = BASE_SPEED
                pygame.time.set_timer(SPEED_RESET, 0)

            # --- 按鍵控制 ---
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

        # --- 撞牆 ---
        if x1 >= DIS_WIDTH or x1 < 0 or y1 >= DIS_HEIGHT or y1 < 0:
            game_close = True

        # --- 移動 ---
        x1 += x1_change
        y1 += y1_change

        # --- 撞到障礙物（若已啟用） ---
        if obstacles and (x1, y1) in obstacles:
            game_close = True

        dis.fill(bak)

        # 畫障礙物
        for (ox, oy) in obstacles:
            pygame.draw.rect(dis, OBST, [ox, oy, SNAKE_BLOCK, SNAKE_BLOCK])

        # 畫正常食物
        pygame.draw.rect(dis, RED, [foodx, foody, SNAKE_BLOCK, SNAKE_BLOCK])

        # 畫加速果實（只有在吃到之後才會生成）
        if speed_food_x is not None:
            pygame.draw.rect(dis, PURPLE, [speed_food_x, speed_food_y, SNAKE_BLOCK, SNAKE_BLOCK])

        # 畫陷阱食物（只有在吃到之後才會生成）
        if trap_food_x is not None:
            pygame.draw.rect(dis, BLUE, [trap_food_x, trap_food_y, SNAKE_BLOCK, SNAKE_BLOCK])

        # --- 更新蛇身 ---
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)

        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # 撞到自己
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        # 畫蛇
        for x in snake_List:
            pygame.draw.rect(dis, GREEN, [x[0], x[1], SNAKE_BLOCK, SNAKE_BLOCK])

        your_score(score)
        pygame.display.update()

        ate_anything = False  # 用來觸發「吃到就刷新障礙物 + 果實」

        # --- 1) 吃正常食物 ---
        if x1 == foodx and y1 == foody:
            Length_of_snake += 1
            score += 1
            ate_anything = True

            # 新正常食物：避開蛇身 + 障礙物 +（若有）加速/陷阱 + 蛇頭
            occupied = set((seg[0], seg[1]) for seg in snake_List) | obstacles | {(x1, y1)}
            if speed_food_x is not None:
                occupied.add((speed_food_x, speed_food_y))
            if trap_food_x is not None:
                occupied.add((trap_food_x, trap_food_y))
            foodx, foody = rand_grid_pos_excluding(occupied)

        # --- 2) 吃加速果實 ---
        if speed_food_x is not None and x1 == speed_food_x and y1 == speed_food_y:
            score += 10
            Length_of_snake += 1
            SNAKE_SPEED = BASE_SPEED + 5
            pygame.time.set_timer(SPEED_RESET, boost_duration * 1000)

            # 吃掉就先消失，等「下一次吃到任何東西」再生成新位置
            speed_food_x = None
            speed_food_y = None

            ate_anything = True

        # --- 3) 吃陷阱食物：扣分、不加長度 ---
        if trap_food_x is not None and x1 == trap_food_x and y1 == trap_food_y:
            score = max(0, score - trap_penalty)

            # 吃掉就先消失，等「下一次吃到任何東西」再生成新位置
            trap_food_x = None
            trap_food_y = None

            ate_anything = True

        # 只要吃到任何東西：刷新障礙物 + 果實位置（你要的「跟障礙物一樣」）
        if ate_anything:
            total_eaten += 1
            maybe_refresh_obstacles_after_eat()
            refresh_fruits_after_eat()

        clock.tick(SNAKE_SPEED)

    # 停止效果計時器（避免重啟遊戲時被影響）
    pygame.time.set_timer(SPEED_RESET, 0)

    pygame.quit()
    quit()

if __name__ == "__main__":
    gameLoop()
