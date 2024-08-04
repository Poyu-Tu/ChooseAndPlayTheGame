import pygame, random
from pygame.locals import * #  導入 Pygame 的所有本地變量

pygame.font.init()

bricks_color = [(3, 68, 166), (3, 122, 186), (75, 196, 251), (37, 227, 233)]

# 設定字型大小
font = pygame.font.SysFont("simsunnsimsun", 18)

# 畫Box
class Box(object):
   def __init__(self, pygame, window, name, rect, color):
        self.pygame = pygame
        self.window = window
        self.name = name
        self.rect = rect
        self.color = color
        self.visivle = True
    
   def update(self):
        if(self.visivle):
            self.pygame.draw.rect(self.window, self.color, self.rect)
# 畫圓
class Circle(object):
    def __init__(self, pygame, window, name, pos, radius, color):
        self.pygame = pygame
        self.window = window
        self.name = name
        self.pos = pos
        self.radius = radius
        self.color = color
        self.visivle = True

    def update(self):
        if(self.visivle):
            self.pygame.draw.circle( self.window, self.color, self.pos , self.radius)

# 定義了一個函數用於在遊戲視窗上顯示文字
def showFont(window, font, text, x, y, color):
    text = font.render(text, True, color)
    window.blit(text, (x,y))

# 定義了一個函數用於判斷物體是否發生碰撞
# boxRect:矩形
def isCollision(x, y, boxRect): 
    if (x >= boxRect[0] and x <= boxRect[0] + boxRect[2] and y >= boxRect[1] and y <= boxRect[1] + boxRect[3]):
        return True;      
    return False;

# 定義了一個函數用於重置遊戲，包括初始化一些變數和磚塊顏色
def resetGame(bricks_list):
    global game_mode, brick_num, cont
    # 生命值
    cont = 3
    # 磚塊部分
    brick_num = len(bricks_list)
    for bricks in bricks_list:
        bricks.color = random.choice(bricks_color) # 隨機選擇一個指定的磚塊顏色       
        bricks.visivle = True           # 開啟磚塊
    game_mode = 0                       # 0:等待開球
    dx =  7                             # 移動速度
    dy = -7
    return dx, dy, brick_num