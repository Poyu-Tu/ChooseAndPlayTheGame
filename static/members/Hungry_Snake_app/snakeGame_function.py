import pygame, random, tkinter as tk
from tkinter import messagebox

pygame.font.init()

# *設定顏色（RGB）
background_color = (40, 38, 36)
border_color = (128, 128, 128)
food_colors = [(255, 226, 184), (184, 255, 241), (186, 255, 184)]
bonus_color = (255, 255, 26)

# *設定字體樣式
font_style = pygame.font.SysFont('bahnschrift', 25)
info_font = pygame.font.SysFont('comicsansms', 15)
hint_font = pygame.font.SysFont('bahnschrift', 10)

# *定義蛇的繪製函數
def draw_snake(window, border_color, snake_color, snake_block, snake_list):
    for i in snake_list:    # 對snake_list 中的每一個元素做迴圈，snake_list 中的每一個元素都是蛇身體的一節位置，位置用一個包含 x 和 y 座標的列表表示，例如 [x, y]
        # 這個矩形代表蛇的一節，為邊框的部分
        pygame.draw.rect(window, border_color, [i[0], i[1], snake_block, snake_block])  # i[0] 和 i[1] 分別是矩形的左上角 x 和 y 座標
        # 用於填充蛇的內部顏色，尺寸略小於蛇的一節
        '''
        Surface():
        用於創建和操作繪圖表面
            創建空白表面：創建一個指定尺寸的空白表面，然後在其上繪製圖像或文字
            繪製圖像：將圖像文件加載到表面上
            繪製形狀：在表面上繪製各種形狀，如矩形、圓形、線條等
            顯示文字：在表面上顯示文字
        '''
        snake_surface = pygame.Surface((snake_block - 1.5, snake_block - 1.5))
        snake_surface.fill(snake_color) # 蛇的內部顏色(粉紅)
        '''
        blit(source, dest):
        用於將一個表面對象繪製到另一個表面上的 Pygame 方法，通常會將文字或圖像表面繪製到遊戲窗口的主表面上
            source：要繪製的來源表面對象
                例如，我們用 render() 方法創建的文字表面。
            dest：目標位置
                可以是一個 (x, y) 坐標元組或一個 Rect 對象，指示在目標表面上繪製的位置
        '''
        window.blit(snake_surface, (i[0] + 1 , i[1] + 1))   # 位置是 i[0] + 1 和 i[1] + 1，這樣可以讓內部顏色略微縮小並居中於蛇的邊界內

# *定義遊戲資訊顯示函數
def show_info(window, info_color, snake_length, fps, start_time, score):
    # 計算遊戲時間
    '''
    pygame.time.get_ticks()：獲取遊戲運行的總時間（毫秒）
    減去 start_time 以獲得遊戲開始後的經過時間：才會重新開始計算時間
    
    '''
    current_time = pygame.time.get_ticks() - start_time

    '''
    render(text, antialias, color, background=None) :
    用於創建文字表面的 Pygame 方法，屬於 Pygame 的字體對象
        text：要渲染的文字字符串
        antialias：布林值，指示是否啟用抗鋸齒
            如果為 True，文字將顯得更平滑
        color：文字顏色
        background（可選）：文字的背景顏色，如果為 None，背景將透明
    '''
    time_text = info_font.render(f"Time: {current_time // 1000}s", True, info_color)    # f"Time: {current_time // 1000}s"：將時間從毫秒轉換為秒並顯示
    fps_text = info_font.render(f"FPS: {fps}", True, info_color)
    length_text = info_font.render(f"Snake Length: {snake_length}", True, info_color)
    score_text = info_font.render(f"Score: {score}", True, info_color)
    hint_text = hint_font.render("**Press 'ESC / X' to force quit**", True, info_color)

    # 畫資訊框
    info_box = pygame.Rect(0, 0, 165, 135)  # 設定一個長方形
    pygame.draw.rect(window, background_color, info_box)    # 畫長方形內
    pygame.draw.rect(window, border_color, info_box, 2) # 畫長方形的外框

    window.blit(time_text, [10, 5])
    window.blit(fps_text, [10, 30])
    window.blit(length_text, [10, 55])
    window.blit(score_text, [10, 80])
    window.blit(hint_text, [10, 110])

# *顯示成績的彈出視窗
def show_score_popup(final_score, length_score):
    root = tk.Tk()  # 這是 tkinter 庫用來生成 GUI 視窗的根物件
    root.withdraw() # 隱藏根視窗，也就是說不會顯示 root 視窗本身
    root.geometry("750x400")    # 設定了視窗的大小為 750 像素寬，400 像素高，這裡設置的大小實際上不會影響彈出訊息框的大小
    root.option_add("*Font", "Helvetica 30")    # 設置了 tkinter 視窗內所有字體的樣式和大小
    final_length_score = final_score * length_score
    messagebox.showwarning("Game Over !", f"Your total score: {int(final_score + final_length_score)}\nIncluding the score for the total length of the snake >> {final_length_score} ")
    root.destroy()  # 會銷毀根視窗物件，這樣做是為了確保 root 物件被正確釋放，避免佔用不必要的資源

# *隨機生成食物位置，確保不會與資訊框重疊
def generate_food(window_width, window_height, snake_block, snake_list):
    while True: # 開始一個無限迴圈，這個迴圈會一直運行直到生成一個合法的食物位置
        '''
        random.randrange(2 * snake_block, window_width - 2 * snake_block): 
        生成一個從 2 * snake_block 到 window_width - 2 * snake_block 之間的隨機整數，這保證了食物不會生成在視窗的邊界之外，也不會在邊界上生成

        round(... / 15.0) * 15.0: 
        將這個隨機整數除以 15.0，並將結果四捨五入(round())到最接近的整數，然後再乘以 15.0，確保了生成的隨機位置是 15 的倍數，這與蛇的大小（snake_block）一致，從而保證蛇和食物都對齊在相同的網格上。
        '''
        food_random_x = round(random.randrange(2 * snake_block, window_width - 2 * snake_block) / 15.0) * 15.0
        food_random_y = round(random.randrange(2 * snake_block, window_height - 2 * snake_block) / 15.0) * 15.0
        if ((food_random_x >= 180 or food_random_y >= 150) and   # 確保食物不與資訊框、蛇身或 bonus 食物重疊，資訊框的大小是 165x135，只要 food_random_x 大於等於 180 或 food_random_y 大於等於 150，就意味著食物不在資訊框內及上
            (food_random_x, food_random_y) not in snake_list):
            
            food_color = random.choice(food_colors)
            return food_random_x, food_random_y, food_color # 一旦找到一個合法的食物位置，就返回這個位置，結束迴圈
        
# *隨機生成獎勵食物位置，確保不會與資訊框重疊
def generate_bonus_food(window_width, window_height, snake_block, snake_list, normal_food):
    while True:
        bonus_food_random_x = round(random.randrange(2 * snake_block, window_width - 2 * snake_block) / 15.0) * 15.0
        bonus_food_random_y = round(random.randrange(2 * snake_block, window_height - 2 * snake_block) / 15.0) * 15.0
        if ((bonus_food_random_x >= 180 or bonus_food_random_y >= 150) and
            (bonus_food_random_x, bonus_food_random_y) not in snake_list and
            (bonus_food_random_x, bonus_food_random_y) not in normal_food):
            return bonus_food_random_x, bonus_food_random_y, bonus_color
            
# *當貪食蛇吃掉普通食物時，顯示一個閃爍的特效        
def eatFood_effect(window, food_random_x, food_random_y, snake_block):
    for i in range(5):
        # 畫食物
        pygame.draw.rect(window, (255, 255, 255), [food_random_x, food_random_y, snake_block, snake_block])
        pygame.display.update()
        pygame.time.wait(20)    # 使程式暫停 20 毫秒，可以讓食物的顏色顯示一段時間
        # 清除食物
        pygame.draw.rect(window, background_color, [food_random_x, food_random_y, snake_block, snake_block])
        pygame.display.update()
        pygame.time.wait(20)

# *當蛇碰撞時，實現了整條蛇閃爍的特效
def collision_effect(window, border_color, snake_color, snake_block, snake_list):
    for i in range(15):
        if i % 2 == 0:  # 判斷目前迴圈的次數是否為偶數，根據判斷結果，執行不同的動作
            draw_snake(window, border_color, snake_color, snake_block, snake_list)  # 背景色為蛇顏色，顯示蛇
        else:
            draw_snake(window, background_color, background_color, snake_block, snake_list) # 背景色為背景色，隱藏蛇
        pygame.display.update()
        pygame.time.wait(100)

# *當貪食蛇吃掉獎勵食物時，實現了整條蛇閃爍的特效
def eatBonus_effect(window, border_color, snake_color, snake_block, snake_list):
    for i in range(10):
        if i % 2 == 0:  # 判斷目前迴圈的次數是否為偶數，根據判斷結果，執行不同的動作
            draw_snake(window, border_color, (255, 0, 0), snake_block, snake_list)  # 背景色為蛇顏色，顯示蛇
        else:
            draw_snake(window, border_color, snake_color, snake_block, snake_list) # 背景色為背景色，隱藏蛇
        pygame.display.update()
        pygame.time.wait(10)