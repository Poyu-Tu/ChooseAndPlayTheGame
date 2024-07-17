import pygame, random, os
from pygame.locals import * #  導入 Pygame 的所有本地變量
from hitbricks_function import *
from tkinter import messagebox as showMsg1, messagebox as showMsg2

# 設置工作目錄為當前文件所在目錄
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 初始化
pygame.init()
pygame.font.init()
pygame.mixer.init()

# 載入音效和背景音樂
pygame.mixer.music.load('background.mp3') # 載入背景音樂
win_sound = pygame.mixer.Sound('win.mp3')
lose_sound = pygame.mixer.Sound('lose.mp3')
catch_sound = pygame.mixer.Sound('catch.mp3')
notCatch_sound = pygame.mixer.Sound('notCatch.mp3')
clean_sound = pygame.mixer.Sound('clean.mp3')
bye_sound = pygame.mixer.Sound('bye.mp3')

# 設置音效和背景音樂音量
pygame.mixer.music.set_volume(0.5)
win_sound.set_volume(1.0)
lose_sound.set_volume(1.0)
catch_sound.set_volume(0.2)
notCatch_sound.set_volume(0.3)
clean_sound.set_volume(0.2)
bye_sound.set_volume(1.0)

 # 顏色(R,G,B值)
bricks_color = [(3, 68, 166), (3, 122, 186), (75, 196, 251), (37, 227, 233)]
background_color = (34, 42, 52)
board_color = (168, 190, 205)
ball_color = (207, 225, 236)
info_color = (240, 255, 255)

# 遊戲視窗的寬度和高度
window_width, window_height = 730, 700

# 設置遊戲視窗大小
window = pygame.display.set_mode((window_width, window_height)) 

# 顯示Title
pygame.display.set_caption("Hit Bricks 🧱") 

# 創建一個對象來幫助跟蹤時間
clock = pygame.time.Clock() 

# 磚塊數量串列
bricks_list = []

# 0:等待開球 1:遊戲進行中
game_mode = 0

# 生命值
cont = 3

# 初始分數
score = 0

# 每個磚塊基礎分數
brick_base_score = 200

# *底板設定
# 定義底板的初始位置
board_x = 0
board_y = (window_height - 48)

#創建一個 Box 類對象來表示底板
board = Box(pygame, window, "board", [board_x, board_y, 100, 17], board_color) #底板長寬

# *球設定
# 定義球的初始位置
ball_x = board_x
ball_y = board_y

# 創建一個 Circle 類對象來表示球
ball = Circle(pygame, window, "ball", [ball_x, ball_x], 9, ball_color)

# *建立磚塊
# 定義磚塊的初始位置
brick_x = 25.5
brick_y = 60

# 初始化磚塊位置變量
brick_w = 0
brick_h = 0
for i in range( 0, 99): # 創建 99 個磚塊
    if i % 11 == 0: # 每 11 個磚塊換一行
        brick_w = 0
        brick_h += 22   # 每個磚塊之間的直向間隔
    bricks_list.append(Box(pygame, window, f"brick_{str(i)}", [brick_w + brick_x, brick_h + brick_y, 60, 20], random.choice(bricks_color)))
    brick_w += 62   # 每個磚塊之間的橫向間隔
    
# 紀錄遊戲開始時間 
start_ticks = pygame.time.get_ticks() 

# 初始遊戲，重置所有變量
dx, dy, brick_num = resetGame(bricks_list)

# 初始化磚塊變化值，也就是磚塊最低的分數
brick_score = 10

# *主迴圈開始
running = True

# 循環播放背景音樂
pygame.mixer.music.play(-1)

while running:

    # 計算遊戲進行的秒數
    seconds = (pygame.time.get_ticks() - start_ticks) / 1000

    for event in pygame.event.get(): # 從佇列中獲取事件
        if event.type == pygame.QUIT:
            pygame.mixer.Sound.play(bye_sound)
            # 等待音樂播放完畢
            while pygame.mixer.get_busy():
                pass
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.mixer.Sound.play(bye_sound)
                # 等待音樂播放完畢
                while pygame.mixer.get_busy():
                    pass
                running = False       
        
        if event.type == pygame.MOUSEMOTION:
            # pygame.mouse.get_pos()：這是一個 Pygame 的函數，用於獲取滑鼠當前的位置。它返回一個包含滑鼠 x 和 y 座標的元組 (x, y)
            # pygame.mouse.get_pos()[0]：這個部分取的是滑鼠 x 座標，即 pygame.mouse.get_pos() 返回的元組中的第一個值
            # - 50：這個部分是從滑鼠 x 座標中減去 50，用於調整底板的 x 座標，使得底板的中心對齊滑鼠的位置
            board_x = pygame.mouse.get_pos()[0] - (board.rect[2] // 2)    # 因底板的寬度是 100 像素，要取中間直可以寫 -(底板寬度 // 2)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if(game_mode == 0):
                game_mode = 1

    # 用背景顏色填充整個視窗
    window.fill(background_color)

    # 磚塊
    for bricks in bricks_list:
        # 球碰磚塊
        if isCollision(ball.pos[0], ball.pos[1], bricks.rect): 
            if bricks.visivle:  # 如果磚塊可見
                # 扣除磚塊
                brick_num -= 1
                # 得分計算
                time_interval = int(seconds // 7)   # 時間每經過7秒進行得分調整
                if brick_score >= 10:
                    brick_score = brick_base_score * (1 - (0.025 * time_interval))  # 每經過7秒 會扣除打掉一塊brick 2.5%的分數
                print(brick_score)
                score += max(brick_score, 0)    # 累加分數並確保得分不為負
                pygame.mixer.Sound.play(clean_sound)
                # 結束遊戲 win
                if brick_num == 0:
                    pygame.mixer.Sound.play(win_sound)
                    # 根據剩餘生命值調整總分
                    if cont == 3:
                        score *= 1.5
                        mb1 = showMsg1.showinfo("GAME OVER", f"恭喜清除所有磚塊\n總分 : {int(score)}分\n包含生命獎勵>>分數 x 1.5")
                    elif cont == 2:
                        score *= 1.25
                        mb1 = showMsg1.showinfo("GAME OVER", f"恭喜清除所有磚塊\n總分 : {int(score)}分\n包含生命獎勵>>分數 x 1.25")
                    else:
                        mb1 = showMsg1.showinfo("GAME OVER", f"恭喜清除所有磚塊\n總分 : {int(score)}分")
                    pygame.quit()
                    break 
                # 球反彈
                dy = -dy;
            # 關閉磚塊
            bricks.visivle = False
        # 更新磚塊
        bricks.update() 

    #  顯示剩餘磚塊數量 
    showFont(window, font, f"Bricks : {brick_num}", 10, 18, info_color)
    
    # 為了避免底板移動超出遊戲視窗
    if board_x < 0: # 如果底板超出左邊界，設置為 0
        board_x = 0
    if board_x > window_width - board.rect[2]:  # 如果底板超出右邊界，設置為視窗寬度減去底板寬度
        board_x = window_width - board.rect[2]
    
    # 秀底板
    board.rect[0] = board_x # 更新底板位置
    board.update()

    # 碰撞判斷=球碰底板
    if isCollision(ball.pos[0], ball.pos[1], board.rect):
        pygame.mixer.Sound.play(catch_sound) 
        # 球反彈
        dy = -dy

    # 0:等待開球   
    if game_mode == 0:
        # ball.pos[0] 是球的位置元組中的 x 座標部分
        # 通過 ball_x = ...，ball_x 被設置為計算出的 x 座標
        # 通過 ball.pos[0] = ball_x，球的 x 座標被設置為 ball_x 的值
        # board.rect[0] 是底板的左上角 x 座標
        # board.rect[2] 是底板的寬度
        # ((board.rect[2] - ball.radius) // 2) 首先計算出底板寬度減去球的半徑，然後將結果除以 2，即將結果減半
        # 這個計算的目的是將球放在底板的中心，減去球的半徑是因為球的位置是基於其中心點，而不是其左上角
        ball.pos[0] = ball_x = board.rect[0] + ((board.rect[2] - ball.radius) // 2) # 將球放在底板中間
        ball.pos[1] = ball_y = board.rect[1] - ball.radius  # 將球放在底板上方

    # 1:遊戲進行中
    elif game_mode == 1:
        # 更新球的位置
        ball_x += dx
        ball_y += dy
        # 判斷死亡遊戲結束
        if (ball_y + dy) > (window_height - ball.radius): # 如果球超出底邊界
            channel = pygame.mixer.Sound.play(notCatch_sound)
            cont -= 1
            while channel.get_busy(): # 等待音樂播放完畢
                pygame.time.delay(50)
            game_mode = 0 

        if cont == 0:
            pygame.mixer.Sound.play(lose_sound)
            mb2 = showMsg2.showinfo("GAME OVER", f"遊戲結束\n本次得分 : {int(score)}")
            pygame.quit()
            running = False

        # 如果球碰到左右邊界，改變水平速度方向
        if ball_x + dx > window_width - ball.radius or ball_x + dx < ball.radius: # 右牆或左牆碰撞.
            dx = -dx
        # 如果球碰到上下邊界，改變垂直速度方向
        if ball_y + dy > window_height - ball.radius or ball_y + dy < ball.radius: # 下牆或上牆碰撞       
            dy = -dy
        # 更新球的位置
        ball.pos[0] = ball_x
        ball.pos[1] = ball_y
    ball.update() # 更新球
    # 顯示字
    showFont(window, font, f"FPS : {int(clock.get_fps())}", 10, 2, info_color)
    showFont(window, font, f"Your Life : {int(cont)}", 10, 34, info_color)
    showFont(window, font, f"Game Time : {int(seconds)}/s", 10, 50, info_color)
    showFont(window, font, f"Score : {int(score)}", 10, 66, info_color)
    # 更新畫面
    pygame.display.update() # 更新顯示
    clock.tick(70)

# 離開遊戲
pygame.quit() 
quit()