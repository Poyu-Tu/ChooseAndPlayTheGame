import pygame, os, threading, random

# *從 snakeGame_function 檔案中引入這些函數
from snakeGame_function import *

# *設置工作目錄為當前文件所在目錄
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# *初始化
pygame.init()   # pygame.init()：初始化所有的 Pygame 模組
pygame.font.init()  # pygame.font.init()：初始化 Pygame 的字體模組
pygame.mixer.init() # 初始化混音器模組

# *載入音效和背景音樂
pygame.mixer.music.load('background_music.mp3') # 載入背景音樂
eat_sound = pygame.mixer.Sound('eat.mp3')
collision_sound = pygame.mixer.Sound('died.mp3')
lose_sound = pygame.mixer.Sound('lose.mp3')
bye_sound = pygame.mixer.Sound('bye.mp3')
bonus_sound = pygame.mixer.Sound('restart.mp3')

# *設置音效和背景音樂音量
pygame.mixer.music.set_volume(0.3)
eat_sound.set_volume(1.0)
collision_sound.set_volume(1.0)
lose_sound.set_volume(1.0)
bye_sound.set_volume(1.0)
bonus_sound.set_volume(1.0)

# *定義遊戲中使用的顏色。這些顏色用 RGB 值來表示
background_color = (40, 38, 36)
snake_color = (249, 67, 143)
message_color = (255, 255, 255)
border_color = (128, 128, 128)
info_color = (255, 255, 255)
food_colors = [(246, 237, 223), (206, 232, 227), (207, 233, 206), (228, 189, 185), (207, 216, 231)]
bonus_color = (255, 255, 26)

# *創建顯示視窗
window_width, window_height = 900, 600  # 設定固定大小的視窗以兼容瀏覽器
window = pygame.display.set_mode((window_width, window_height))

# *設定視窗標題
pygame.display.set_caption('Hungry Snake 🐍')

# *創建一個 Clock 對象來幫助控制遊戲的幀率
clock = pygame.time.Clock()

# *設置蛇的大小和速度
snake_block = 15    # 定義蛇每一節的大小
snake_speed = 15    #  義蛇的移動速度

# *初始化 bonus 食物計時器
bonus_food_timer = random.randint(10000, 20000)  # 隨機生成 10 到 20 秒的計時器
bonus_food_start_time = pygame.time.get_ticks()  # 記錄開始時間
        
# !定義遊戲主循環函數
def gameLoop():

    global bonus_food, bonus_food_timer, bonus_food_start_time

    # *循環播放背景音樂
    pygame.mixer.music.play(-1)

    game_over = False   # 控制遊戲是否繼續 
    game_close = False  # 控制遊戲是否關閉
    score_shown = False # 顯示分數

    # *設定蛇的初始位置在視窗的中心
    init_loc_x = window_width / 2
    init_loc_y = window_height / 2

    # *設定蛇的初始移動方向
    init_move_x = 0
    init_move_y = 0

    # *蛇的初始身體設定
    init_snake = [] # 用於儲存蛇身每一節的位置
    init_snake_length = 1   # 設定蛇的初始長度為 1 節

    # *隨機生成食物位置
    food_random_x, food_random_y, food_color = generate_food(window_width, window_height, snake_block, init_snake)

    # *計算目前吃掉多少食物
    food_counter = 0
    
    # *初始分數
    score = 0

    # *初始化 bonus 食物
    bonus_food = None

    # *記錄遊戲開始時間
    start_time = pygame.time.get_ticks()

    # *在背景執行緒中生成 bonus 食物
    threading.Thread(target=generate_bonus_food, args=(window_width, window_height, snake_block, init_snake, [(food_random_x, food_random_y, food_color)])).start()

    # *當 game_over 為 False 時，執行遊戲循環
    while not game_over:
        # 檢查按鍵event
        for event in pygame.event.get():    # 迴圈獲取所有 Pygame 的事件
            # *如果按下 叉叉 鍵，顯示退出訊息並結束遊戲
            if event.type == pygame.QUIT:
                pygame.mixer.Sound.play(bye_sound)
                # 等待音樂播放完畢
                while pygame.mixer.get_busy():
                    pass
                game_over = True
            
            if event.type == pygame.KEYDOWN:    # 如果按下某個鍵...
                # *檢查具體的按鍵並改變蛇的移動方向
                if event.key == pygame.K_j:
                    init_move_x = -snake_block
                    init_move_y = 0
                elif event.key == pygame.K_l:
                    init_move_x = snake_block
                    init_move_y = 0
                elif event.key == pygame.K_i:
                    init_move_y = -snake_block
                    init_move_x = 0
                elif event.key == pygame.K_k:
                    init_move_y = snake_block
                    init_move_x = 0
                # *如果按下 ESC 鍵，顯示退出訊息並結束遊戲
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.Sound.play(bye_sound)
                    # 等待音樂播放完畢
                    while pygame.mixer.get_busy():
                        pass
                    game_over = True
 
        # *碰撞邊界判斷
        if ((init_loc_x >= window_width - 15) or (init_loc_x <= 0) or 
            (init_loc_y >= window_height - 15) or (init_loc_y <= 0) or
            # 以上檢查是否有碰撞到視窗邊界
            # window_width - 15 可以根據網格 確保碰撞視窗邊界時 蛇不會跑出畫面外面 而是在切齊畫面處發生事件
            (init_loc_x <= 165) and (init_loc_y <= 135)):   # (init_loc_x < 165 and init_loc_y < 135)：檢查是否碰撞到資訊框
            
            if not game_close:  # 確保僅在 game_close 為 False 時執行碰撞處理
                pygame.mixer.Sound.play(collision_sound)
                collision_effect(window, border_color, snake_color, snake_block, init_snake)
                pygame.time.wait(1000)   # 等待 1000 毫秒
                game_close = True   # 遊戲關閉
        
        # *控制蛇的移動位置變化
        if not game_close:  # 如果遊戲沒有結束...
            init_loc_x += init_move_x   # 持續更新蛇的橫向移動
            init_loc_y += init_move_y   # 持續更新蛇的縱向移動

        # *填充背景
        window.fill(background_color)

        # *畫食物
        '''
        pygame.draw.rect(surface, color, rect, width=0)：用於在指定的 Surface（畫布）上畫一個矩形
            surface: 要在哪個畫布上繪製這個矩形
            color: 矩形的顏色
            rect: 定義矩形的位置和大小。這是一個列表或元組，格式為 [x, y, width, height]
                x: 矩形的左上角的 x 座標
                y: 矩形的左上角的 y 座標
                width: 矩形的寬度
                height: 矩形的高度
            width（可選）：邊框的寬度。默認為 0，表示填充整個矩形。如果設置為其他值，則僅繪製邊框，內部為透明
        '''
        # [food_random_x, food_random_y, snake_block, snake_block]:
        #     food_random_x: 矩形左上角的 x 座標，表示食物在視窗中的橫向位置
        #     food_random_y: 矩形左上角的 y 座標，表示食物在視窗中的縱向位置
        #     snake_block: 矩形的寬度，這裡與蛇的方塊大小相同
        #     snake_block: 矩形的高度，同樣與蛇的方塊大小相同
        pygame.draw.rect(window, food_color, [food_random_x, food_random_y, snake_block, snake_block])

        # *畫獎勵食物
        if bonus_food:
            bonus_random_food_x, bonus_random_food_y, bonus_color = bonus_food
            pygame.draw.rect(window, bonus_color, [bonus_random_food_x, bonus_random_food_y, snake_block, snake_block])
            # 檢查獎勵食物是否超過 5 秒
            if pygame.time.get_ticks() - bonus_food_start_time > 5000:
                bonus_food = None

        # *更新蛇的身體位置，並保持蛇的長度不變
        snake_update = [init_loc_x, init_loc_y] # snake_update: 這是一個清單（list），包含了蛇頭目前的位置 [init_loc_x, init_loc_y]
        init_snake.append(snake_update) # 將 snake_update 這個包含了蛇頭新位置的清單，添加到 init_snake 這個蛇身體的位置清單中
        if len(init_snake) > init_snake_length: # 如果 init_snake 清單的長度（即蛇身的節數）超過了 init_snake_length，則刪除最早的一節，這是為了控制蛇身體的長度，保持其不變，除非吃到食物
            del init_snake[0]   # 刪除 init_snake 清單中的第一個元素，即最早加入的那節。這樣蛇看起來就像是在前進，因為新的節會在蛇頭增加，而舊的節會從蛇尾刪除

        # *判斷蛇是否咬到自己
        for i in init_snake[:-1]:   # [:-1] 表示從列表的開始到最後一個元素的前一個元素（不包括最後一個元素），目的是排除蛇頭的當前位置，只檢查蛇身體的其他部分，以防止自我咬傷的判斷出錯
            # 這行程式碼檢查當前的蛇身位置 i 是否等於蛇頭的當前位置 snake_update
            if i == snake_update:   # 如果 i 和 snake_update 相等，這意味著蛇頭的位置與蛇身的某個位置重疊了，這就是蛇咬到了自己
                pygame.mixer.Sound.play(collision_sound)
                collision_effect(window, border_color, snake_color, snake_block, init_snake)
                game_close = True   # 遊戲關閉

        # *畫蛇
        draw_snake(window, border_color, snake_color, snake_block, init_snake)

        # *顯示遊戲資訊
        # 獲取當前遊戲的每秒幀數（Frames Per Second，簡稱 FPS），然後將其轉換為整數(因為 clock.get_fps() 可能返回一個浮點數)，有助於監控遊戲的流暢度
        fps = int(clock.get_fps())
        show_info(window, info_color=info_color, snake_length=init_snake_length, fps=fps, start_time=start_time, score=score)

        # *更新顯示
        pygame.display.update() # 主要作用是將你在程式中對視窗內容的所有更改（例如畫蛇、畫食物、填充背景等）應用到實際的視窗中，使得使用者能夠看到這些變化

        # *每吃到10的倍數數量的食物，會存到food_num裡
        food_num = int(food_counter // 10)

        # *檢查是否吃到普通食物，包含計分
        if (init_loc_x == food_random_x) and (init_loc_y == food_random_y):
            pygame.mixer.Sound.play(eat_sound)
            eatFood_effect(window, food_random_x, food_random_y, snake_block)
            # 根據當前食物是否為bonus food而判斷是否會增加長度，True = +2，False = +1
            food_random_x, food_random_y, food_color = generate_food(window_width, window_height, snake_block, init_snake)
            score += int(200 * (1 + (0.1 * food_num)))    # 普通food 一個200分
            init_snake_length += 1
            food_counter += 1   # 吃到食物 +1 次

        # *檢查是否吃到獎勵食物，包含計分
        if bonus_food and init_loc_x == bonus_food[0] and init_loc_y == bonus_food[1]:
            pygame.mixer.Sound.play(bonus_sound)
            eatFood_effect(window, bonus_food[0], bonus_food[1], snake_block)
            eatBonus_effect(window, border_color, snake_color, snake_block, init_snake)
            bonus_food = None
            score += int(500 * (1 + (0.1 * food_num)))
            init_snake_length += 2

        # *隨機生成獎勵食物
        if not bonus_food and pygame.time.get_ticks() - bonus_food_start_time > bonus_food_timer:
            bonus_food = generate_bonus_food(window_width, window_height, snake_block, init_snake, [(food_random_x, food_random_y, food_color)])
            bonus_food_start_time = pygame.time.get_ticks()
            bonus_food_timer = random.randint(10000, 20000)

        # *設定遊戲速度
        clock.tick(snake_speed)

        # !game over後的 loop
        while game_close:
            pygame.mixer.music.stop()   # 背景音樂停止
            if not score_shown:
                pygame.mixer.Sound.play(lose_sound)
                length_score = init_snake_length * 0.01
                show_score_popup(score, length_score)
                score_shown = True  # 表示分數已經顯示過了，可以確保分數彈出視窗只顯示一次

                pygame.mixer.Sound.play(bye_sound)
                # 等待音樂播放完畢
                while pygame.mixer.get_busy():
                    pass
                game_over = True
                return
    
    pygame.quit()
    quit()

# 開始遊戲
gameLoop()