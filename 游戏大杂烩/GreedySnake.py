 #coding:utf-8
'''
贪吃蛇
author: yoghurt-lee
'''
import random ,pygame,sys
from pygame.locals import *
from sys import exit
import time
image_path = './image/greedy-snake/'
show_picture = './image/greedy-snake/show.png'
background_picture = './image/greedy-snake/background.jpg'

#游戏帧率
FPS = 30
#屏幕长宽
WIDTH = 640
HEIGHT = 480
#块大小
CELLSIZE = 20
CELLWIDTH = int(WIDTH/CELLSIZE)
CELLHEIGHT = int(HEIGHT/CELLSIZE)

# 颜色数组
WHITE = (255, 255, 255)
BLACK = ( 0, 0, 0)
RED = (255, 0, 0)
GREEN = ( 0, 255, 0)
DARKGREEN = ( 0, 155, 0)
DARKGRAY = ( 40, 40, 40)
YELLOW = (255,255,0)
#背景颜色
BGCOLOR = BLACK
#贪吃蛇头部
HEAD = 0
#方向数组
RIGHT = [1,0]
LEFT = [-1,0]
UP = [0,-1]
DOWN = [0,1]
#初始化 ,屏幕,让动画基于时间运作
pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT),0,32)
FPSCLOCK = pygame.time.Clock()
#设置字体以及图片
FONT = pygame.font.Font('./font/FZSTK.TTF',18)
BACKGROUND_PICTURE = pygame.image.load(background_picture).convert()
SHOW_PICTURE = pygame.image.load(show_picture).convert()
def main():
    '''
    运行游戏
    '''
    global MOUSEIMAGE
    #鼠标位置
    MOUSEIMAGE = pygame.image.load(image_path + 'guangbiao.png')
    #设置标题
    pygame.display.set_caption('贪吃蛇')
    #设置图标
    icon = pygame.image.load(image_path + 'icon.png')
    pygame.display.set_icon(icon)

    #显示开始图片
    if showStartScreen():
        return

    while True:
        runGame()
        if gameOver():
            break


def gameOver():
    '''
    游戏结束
    '''
    #设置结束提示以及绘制
    gameoverFont = pygame.font.Font('./font/cabin.ttf', 100)
    gameSurf = gameoverFont.render('Game Over',True,RED)
    gameRect = gameSurf.get_rect()
    gameRect.center = (WIDTH/2,HEIGHT/2)

    FONT1 = pygame.font.Font('./font/FZSTK.TTF', 30)
    pressKeySurf = FONT1.render(u'按ESC结束游戏/按R重新开始', True, WHITE)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.center = (WIDTH /2, HEIGHT - 60)
    #等待时间循环重新开始或者结束游戏
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_r:
                    return 0
                elif event.key == K_ESCAPE:
                    return 1
        SCREEN.blit(BACKGROUND_PICTURE,(0,0))
        SCREEN.blit(gameSurf,gameRect)
        SCREEN.blit(pressKeySurf, pressKeyRect)
        (x,y) = pygame.mouse.get_pos()
        SCREEN.blit(MOUSEIMAGE,(x-MOUSEIMAGE.get_width()/2,y-MOUSEIMAGE.get_height()/2))
        #刷新屏幕
        pygame.display.update()

def runGame():
    #游戏主循环
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5,CELLHEIGHT - 6)
    #最开始蛇长度为 3
    snake = [
        {'x':startx,'y': starty},
        {'x': startx - 1, 'y': starty},
        {'x': startx - 2, 'y': starty}
    ]
    #最开始的方向
    direction = RIGHT
    #生成苹果位置
    apple = appleLocation()
    #循环一次的时间
    TIME = 0.1
    #蛇的长度作为一个标志,如果这个标志变化了,那么TIME也就变化，控制游戏难度
    laststate = len(snake)
    while True:
        SCREEN.blit(BACKGROUND_PICTURE,(0,0))
        #draw_grid()
        #蛇死亡后返回
        if snakeDie(snake):
            return
        lastdirection = direction #记录前一个方向,防止出现BUG
        #事件循环
        for event in pygame.event.get():
            if event.type==QUIT:
                exit()
            elif event.type == KEYDOWN:
                key = event.key
                if lastdirection != RIGHT:
                    if (key ==K_a or key==K_LEFT) and direction!=RIGHT: #往左
                        direction = LEFT
                if lastdirection != LEFT:
                    if (key ==K_d or key==K_RIGHT) and direction!=LEFT: #往右
                        direction = RIGHT
                if lastdirection != DOWN:
                    if (key ==K_a or key==K_UP) and direction!=DOWN: #往上
                        direction = UP
                if lastdirection != UP:
                    if (key ==K_s or key==K_DOWN) and direction!=UP: #往下
                        direction = DOWN
                if key==K_ESCAPE:
                    exit()
        #吃到了苹果，生成新苹果,否则，删除蛇的尾巴
        if snake[HEAD]['x']== apple['x'] and snake[HEAD]['y'] == apple['y']:
            apple = appleLocation()
        else:
            del snake[-1] #删除掉蛇的尾巴
        #新的头
        new_head = {'x':snake[HEAD]['x']+direction[0],'y':snake[HEAD]['y']+direction[1]}
        snake.insert(0,new_head)
        #绘制蛇,苹果，分数
        draw_snake(snake)
        draw_apple(apple)
        draw_score(10*(len(snake)-3))
        #绘制鼠标
        (x,y) = pygame.mouse.get_pos()
        SCREEN.blit(MOUSEIMAGE,(x-MOUSEIMAGE.get_width()/2,y-MOUSEIMAGE.get_height()/2))
        #刷新屏幕
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        #蛇的当前长度为蛇的当前状态
        nowstate = len(snake)
        #状态变化
        if laststate!=nowstate:
            TIME-=0.005
            laststate = nowstate
        #确保循环时间合理性
        if TIME<0: TIME = 0
        time.sleep(TIME)

def draw_score(score):
    '''
    绘制分数
    '''
    Font = pygame.font.Font('./font/cabin.ttf', 30)
    scoreSurf = Font.render('Score: %s' % (score), True, YELLOW)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WIDTH - 200, 10)
    SCREEN.blit(scoreSurf,scoreRect)

def draw_snake(snake):
    '''
    绘制蛇
    '''
    head = True
    for item in snake:
        x = item['x']*CELLSIZE
        y = item['y']*CELLSIZE
        snakeRect = pygame.Rect(x,y,CELLSIZE,CELLSIZE)
        pygame.draw.rect(SCREEN,DARKGREEN,snakeRect)
        if head:
            head = False
            innersankeRect = pygame.Rect(x+2,y+2,CELLSIZE-4,CELLSIZE-4)
            pygame.draw.rect(SCREEN,YELLOW,innersankeRect)
        else:
            innersankeRect = pygame.Rect(x+2,y+2,CELLSIZE-4,CELLSIZE-4)
            pygame.draw.rect(SCREEN,GREEN,innersankeRect)

def draw_apple(apple):
    '''
    绘制苹果
    '''
    x = apple['x']*CELLSIZE
    y = apple['y']*CELLSIZE
    appleRect = pygame.Rect(x,y,CELLSIZE,CELLSIZE)
    pygame.draw.rect(SCREEN,RED,appleRect)

def draw_grid():
    '''
    绘制网格(测试用)
    '''
    color = (40,40,40)
    for x in range(0,WIDTH,CELLSIZE):
        pygame.draw.line(SCREEN,color,(x,0),(x,HEIGHT))
    for y in range(0,HEIGHT,CELLSIZE):
        pygame.draw.line(SCREEN,color,(0,y),(WIDTH,y))

def snakeDie(snake):
    '''
    判定蛇当前是否死亡
    '''
    # 蛇撞墙或者撞到自己就挂了
    if snake[HEAD]['x'] == -1 or snake[HEAD]['x'] == CELLWIDTH or snake[HEAD]['y'] == -1 or snake[HEAD]['y'] == CELLHEIGHT:
        return True
    for item in snake[1:]:
        if snake[HEAD]['x'] == item['x'] and snake[HEAD]['y'] == item['y']:
            return True
    return False

def appleLocation():
    '''
    随机生成苹果的位置
    '''
    return {'x':random.randint(0,CELLWIDTH-1),'y':random.randint(0,CELLHEIGHT-1)}

def showStartScreen():
    '''
    绘制开始屏幕
    '''
    titleFont = pygame.font.Font('./font/cabin.ttf', 55)
    titleSurf = titleFont.render('Greedy Snake!', True, RED)
    #参数一：显示的内容
    #参数二：是否开启抗锯齿，就是说True的话字体会比较平滑，不过相应的速度有一点点影响
    #参数三：字体颜色
    #参数四：字体背景颜色（可选）
    degrees = 0
    while True:
        SCREEN.blit(SHOW_PICTURE,(0,0))
        rotatedSurf = pygame.transform.rotate(titleSurf, degrees)
        rotatedRect = rotatedSurf.get_rect()
        rotatedRect.center = (WIDTH / 2, HEIGHT / 3)
        SCREEN.blit(rotatedSurf, rotatedRect)

        FONT1 = pygame.font.Font('./font/FZSTK.TTF', 30)
        pressKeySurf = FONT1.render(u'请按任意键开始游戏.', True, WHITE)
        pressKeyRect = pressKeySurf.get_rect()
        pressKeyRect.center = (WIDTH /2, HEIGHT - 60)
        SCREEN.blit(pressKeySurf, pressKeyRect)
        flag = checkForKeyPress()
        if flag==1:
            return 1
        elif flag:
            return 0
        #清空事件循环
        pygame.event.get()
        (x,y) = pygame.mouse.get_pos()
        SCREEN.blit(MOUSEIMAGE,(x-MOUSEIMAGE.get_width()/2,y-MOUSEIMAGE.get_height()/2))

        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees += 3 #每次增加的角度


def checkForKeyPress():
    '''
    判定键盘事件
    '''
    if len(pygame.event.get(QUIT)) > 0:
        exit()
    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        return 1
    return 2

if __name__ == '__main__':
    main()
