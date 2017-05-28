#coding:utf-8
'''
贪吃蛇
author: yoghurt-lee
'''
import pygame,random,sys
from sys import exit
from pygame.locals import *
path = sys.argv[0]
#图片路径
image_path = './image/2048/'
background_picture = './image/2048/background.jpg'
#游戏初始化
pygame.init()

#屏幕长宽
WIDTH = 480
HEIGHT = 580
#分数区域的高度
SCORE_HIGHT = HEIGHT-WIDTH
#块大小
CELLSIZE = 120
#每行以及每列的块数
SIZE = 4
#屏幕初始化
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
#背景图对象
BACKGROND_PICTURE = pygame.image.load(background_picture).convert()
#数字数组
array = [[0 for i in range(SIZE)] for i in range(SIZE)]
#16个方块的Surface对象
BLOCK = [pygame.Surface((CELLSIZE, CELLSIZE)) for i in range(15)]
#Ｒ　Ｇ　Ｂ颜色待选数组
color = [
    (192,192,192),
    (211,211,211),
    (0,255,0),
    (255,105,180),
    (0,0,255),
    (255,255,0),
    (0,0,139),
    (119,136,153),
    (0,206,209),
    (0,128,128),
    (173,255,47),
    (255,250,205),
    (255,215,0),
    (255,250,240),
    (255,239,205)
]
for i in range(15):
    BLOCK[i].fill(color[i])
TIMES = SIZE*SIZE #还有多少个空地方 最开始有16个空
#总分数
SCORE = 0
def main():
    '''
    开始游戏
    '''
    while True:
        if runGame()==1:
            return
        if GAMEOVER():
            return

def runGame():
    '''
    游戏主循环
    '''
    global array,TIMES,SCORE,SCREEN,MOUSEIMAGE
    # 屏幕
    SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
    # 设置标题
    pygame.display.set_caption('2048')
    # 鼠标指针图片
    MOUSEIMAGE = pygame.image.load(image_path + 'guangbiao.png')
    # 游戏图标以及设置
    icon = pygame.image.load(image_path + 'icon.jpg')
    pygame.display.set_icon(icon)
    # 初始化数组
    array = [[0 for i in range(SIZE)] for i in range(SIZE)]
    TIMES = SIZE*SIZE #还有多少个空地方 最开始有16个空
    SCORE = 0
    # 初始化两个数字方块
    create()
    create()
    # 显示游戏面板
    showPanel()
    while True:
        # 绘制背景图
        SCREEN.blit(BACKGROND_PICTURE,(0,0))
        if gameOver():
            return
        # 时间循环
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return 1
                else:
                    moveKey(event)
        showPanel()

def GAMEOVER():
    '''
    游戏结束页面
    '''
    global SCORE
    # 设置字体以及显示字体
    gameoverFont = pygame.font.Font('./font/cabin.ttf', 100)
    gameSurf = gameoverFont.render('Game Over',True,(255,0,0))
    gameRect = gameSurf.get_rect() #获取当前字体所在矩形的长宽
    gameRect.center = (WIDTH/2,HEIGHT/2) #设置矩形中心

    Margin = pygame.Surface((WIDTH, CELLSIZE))
    Margin.fill((255,255,255))
    FONT1 = pygame.font.Font('./font/FZSTK.TTF', 30)
    pressKeySurf = FONT1.render(u'按ESC结束游戏/按R重新开始', True, (0,0,0))
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.center = (WIDTH /2, HEIGHT - 60)

    while True:
        # 设置背景图
        SCREEN.blit(BACKGROND_PICTURE,(0,0))
        SCREEN.blit(gameSurf,gameRect)
        SCREEN.blit(Margin,(0, HEIGHT-CELLSIZE))
        SCREEN.blit(pressKeySurf, pressKeyRect)
        # 获取鼠标位置
        (x,y) = pygame.mouse.get_pos()
        SCREEN.blit(MOUSEIMAGE,(x-MOUSEIMAGE.get_width()/2,y-MOUSEIMAGE.get_height()/2))
        #时间循环
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_r:
                    return 0
                elif event.key == K_ESCAPE:
                    return 1
        #刷新
        pygame.display.update()

def moveKey(e):
    '''
    判定键盘事件
    '''
    global SCORE,TIMES #引用全局变量,如果要修改全局变量的值必须这么弄,不然SCORE会被认为是局部变量
    flag = False #标志整个图是否发生了变化,如果发生了变化就调用 create()
    # 触发了向上的操作
    if e.key == K_UP or e.key == K_w:
        for y in range(1,SIZE):
            for x in range(0,SIZE):
                if array[x][y] == 0: continue
                dispos = -1 # 标记位置 ,如果这个dispos一直为-1 ,那么证明y以上的所有位置都不会被y代替的位置,否则y1的位置将被y位置的元素代替
                for y1 in range(y-1,-1,-1):
                    if array[x][y1]!=0:
                        if array[x][y] == array[x][y1]:
                            flag = True
                            dispos = -1
                            SCORE += 2*array[x][y1]
                            array[x][y1]*=2
                            array[x][y] = 0
                            TIMES+=1 #空位增加了
                        break #直接退出循环,该层已经不可能再往上走了
                    else:
                        dispos = y1
                #不为-1的情况
                if dispos is not -1:
                    flag = True
                    array[x][dispos] = array[x][y]
                    array[x][y] = 0
    #触发了向下的操作
    if e.key == K_DOWN or e.key == K_s:
        for y in range(SIZE-1,-1,-1):
            for x in range(0,4):
                if array[x][y] == 0: continue
                dispos = -1
                for y1 in range(y+1,SIZE):
                    if array[x][y1]!=0:
                        if array[x][y] == array[x][y1]:
                            flag = True
                            dispos = -1
                            SCORE += 2*array[x][y1]
                            array[x][y1]*=2
                            array[x][y] = 0
                            TIMES+=1 #空位增加了
                        break #直接退出循环,该层已经不可能再往上走了
                    else:
                        dispos = y1
                if dispos is not -1:
                    flag = True
                    array[x][dispos] = array[x][y]
                    array[x][y] = 0
    #触发了向左的操作
    if e.key == K_a or e.key == K_LEFT:
        for y in range(0,SIZE):
            for x in range(1,SIZE):
                if array[x][y] == 0:continue
                dispos = -1
                for x1 in range(x-1,-1,-1):
                    if array[x1][y] !=0:
                        if array[x1][y]== array[x][y]:
                            flag = True
                            dispos = -1
                            SCORE += 2*array[x1][y]
                            array[x1][y]*=2
                            array[x][y] = 0
                            TIMES+=1
                        break
                    else:
                        dispos = x1
                if dispos is not -1:
                    flag = True
                    array[dispos][y] = array[x][y]
                    array[x][y] = 0
    #触发了向右的操作
    if e.key == K_d or e.key == K_RIGHT:
        for y in range(0,SIZE):
            for x in range(SIZE-1,-1,-1):
                if array[x][y] == 0:continue
                dispos = -1
                for x1 in range(x+1,SIZE):
                    if array[x1][y] !=0:
                        if array[x1][y]== array[x][y]:
                            flag = True
                            dispos = -1
                            SCORE += 2*array[x1][y]
                            array[x1][y]*=2
                            array[x][y] = 0
                            TIMES+=1
                        break
                    else:
                        dispos = x1
                if dispos is not -1:
                    flag = True
                    array[dispos][y] = array[x][y]
                    array[x][y] = 0
    if flag:
        #创造新数字方块
        create()
def create():
    '''
    在空方块处产生新的数字
    '''
    flag = False # 直到某个空位置产生一个新的数 flag 才变成 0
    if TIMES>0:
        while not flag:
            x = random.randint(0,3)
            y = random.randint(0,3)
            #print x,y
            if array[x][y] == 0:
                if random.randint(0,3) == 0: #1/4的几率生成 4
                    array[x][y] = 4
                else:
                    array[x][y] = 2
                flag = True

def gameOver():
        '''
        判定游戏的结束状态
        '''
        for r in range(SIZE):
            for c in range(SIZE):
                if array[r][c] == 0:
                    return False
        for r in range(SIZE):
            for c in range(SIZE-1):
                if array[r][c] == array[r][c + 1]:
                    return False
        for r in range(SIZE-1):
            for c in range(SIZE):
                if array[r][c] == array[r + 1][c]:
                    return False
        return True

def showPanel():
    '''
    显示游戏面板
    '''
    for i in range(SIZE):
        for j in range(SIZE):
            WHITE=(255,255,255)
            # 画矩形
            outerRect = pygame.Rect(CELLSIZE * i,CELLSIZE * j+100,CELLSIZE,CELLSIZE)
            pygame.draw.rect(SCREEN,WHITE,outerRect)
            innerRect = pygame.Rect(CELLSIZE * i+5,CELLSIZE * j+100+5,CELLSIZE-10,CELLSIZE-10)
            if array[i][j] != 0:
                t = array[i][j]
                num=0
                while t!=1:
                    num+=1
                    t/=2
                '''
                SCREEN.blit(BLOCK[num%14],(CELLSIZE * i, CELLSIZE * j+100))
                '''
                # 绘制方块颜色
                pygame.draw.rect(SCREEN,color[num%14],innerRect)
                Font = pygame.font.Font('./font/cabin.ttf', 80)
                map_text = Font.render(str(array[i][j]), True, (106, 90, 205))
                text_rect = map_text.get_rect()
                text_rect.center = (CELLSIZE * i + CELLSIZE / 2, CELLSIZE * j + CELLSIZE / 2+100)
                SCREEN.blit(map_text, text_rect)
            else:
                '''
                SCREEN.blit(BLOCK[0],(CELLSIZE * i, CELLSIZE * j+100))
                '''
                pygame.draw.rect(SCREEN,color[0],innerRect)
    # 绘制分数
    Font = pygame.font.Font('./font/cabin.ttf', 45)
    score_text = Font.render("Score: %s"%str(SCORE),True,(255,255,0))
    text_rect = map_text.get_rect()
    text_rect.center = (250, 70)
    SCREEN.blit(score_text, text_rect)
    #绘制鼠标
    (x,y) = pygame.mouse.get_pos()
    SCREEN.blit(MOUSEIMAGE,(x-MOUSEIMAGE.get_width()/2,y-MOUSEIMAGE.get_height()/2))
    #刷新屏幕
    pygame.display.update()

if __name__ == '__main__':
    main()
