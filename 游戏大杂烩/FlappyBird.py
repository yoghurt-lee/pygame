from pygame.locals import *
import pygame,random,time,sys

bgm_path = "./bgm/flappy-bird/"
image_path = "./image/flappy-bird/"
font_path = "./font/"
FPS = 30
PIPETIME = 2 #s
BIRDFLYTIME = 1 #s
BirdFlySpeed = [0,15] #px/s
BirdFallSpeed = [0,15] #px/s
PipeMoveSpeed = [-200,0]
WINDOWWIDTH = 284 * 2
WINDOWHEIGHT = 512
PASSHEIGHT = 130
TEXTCOLOR = (255, 255, 255)
TEXTSHADOWCOLOR = (185, 185, 185)

def makeTextObjs(text, font, color):
  surf = font.render(text, True, color)
  return surf, surf.get_rect()

def terminate():
  pygame.quit()
  sys.exit()

def checkForKeyPress():
  # Go through event queue looking for a KEYUP event.
  # Grab KEYDOWN events to remove them from the event queue.
  for event in pygame.event.get(): # get all the QUIT events
    if event.type == QUIT :
        pygame.quit()
        sys.exit()
    if event.type == KEYDOWN:
        return event.key
  return None


def showTextScreen(text):
    titleShadowSurf, titleShadowRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
    titleShadowRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) - 100)

    # Draw the text
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 103)

    # Draw the additional "Press a key to play." text.
    pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play.', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) )

    while True:
        DISPLAYSURF.blit(BACKGROUND,(0,0))
        DISPLAYSURF.blit(BACKGROUND,(284,0))
        DISPLAYSURF.blit(titleShadowSurf, titleShadowRect)
        DISPLAYSURF.blit(titleSurf, titleRect)
        DISPLAYSURF.blit(pressKeySurf, pressKeyRect)
        (x,y) = pygame.mouse.get_pos()
        DISPLAYSURF.blit(MOUSEIMAGE,(x-MOUSEIMAGE.get_width()/2,y-MOUSEIMAGE.get_height()/2))
        press = checkForKeyPress()
        if press == K_ESCAPE:
            return False
        elif press != None:
            return True
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def check_in_pipe(bird,pipe):
    if bird.x+bird.images[0].get_width()/2 < pipe.x - pipe.images[0].get_width()/2:
        return False
    if bird.x-bird.images[0].get_width()/2 > pipe.x + pipe.images[0].get_width()/2:
        return False
    return True

def isValidPosition(pipes,bird):
    x=bird.x
    y=bird.y
    if(y-bird.images[0].get_height()/2 < 0 or y+bird.images[0].get_height()/2 > WINDOWHEIGHT):
        return False
    for pipe in pipes:
        if check_in_pipe(bird,pipe):
            if y-bird.images[0].get_height()/2 < pipe.topy + pipe.images[0].get_height()/2:
                return False
            elif y + bird.images[0].get_height()/2 > pipe.bottomy - pipe.images[0].get_height()/2:
                return False
    return True


class Bird(object):
    def __init__(self,x,y,speed,bird_images):
        self.x = x
        self.y = y
        self.images = bird_images #wing up and wing down
        self.fall_speed = speed
        self.destination = [self.x,self.y] #press space will be set a destination

class Pipe(object):
    def __init__(self,pipe_x,toppipe_mid_y,pipe_image):
        #middle coordinate
        self.x = pipe_x
        self.topy = toppipe_mid_y
        self.bottomy = toppipe_mid_y + pipe_image[0].get_height() + PASSHEIGHT
        self.images = pipe_image

def DrawTheWorld(bird,pipes,score):
    DISPLAYSURF.blit(BACKGROUND,(0,0))
    DISPLAYSURF.blit(BACKGROUND,(284,0))
    DISPLAYSURF.blit(bird.images[random.randint(0,1)],(bird.x - bird.images[0].get_width()/2,bird.y - bird.images[0].get_height()/2))
    for pipe in pipes:
        DISPLAYSURF.blit(pipe.images[0],(pipe.x - pipe.images[0].get_width()/2,pipe.topy - pipe.images[0].get_height()/2))
        DISPLAYSURF.blit(pipe.images[1],(pipe.x - pipe.images[0].get_width()/2,pipe.bottomy - pipe.images[0].get_height()/2))
    scoreSurf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.center = (WINDOWWIDTH/2, 20)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

def runGame():
    bird_wing_up_image = pygame.image.load(image_path + 'bird_wing_up.png')
    bird_wing_down_image = pygame.image.load(image_path + 'bird_wing_down.png')
    bird = Bird(50,WINDOWHEIGHT/2,BirdFallSpeed,[bird_wing_up_image,bird_wing_down_image])
    top_pipe_image = pygame.image.load(image_path + 'toppipe.png')
    down_pipe_image = pygame.image.load(image_path + 'downpipe.png')
    LastPipeTime = time.time()
    LastPipeMoveTime = time.time()
    LastBirdFlyTime = time.time()
    LastBirdDwonTime = time.time()
    pipes = []
    score = 0
    IsInPipe = False
    NowInPipe = None
    IsBirdFly = False
    while True: #game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
                elif event.key == K_r:
                    return score
                elif event.key == K_p:
                    #Pausing the game
                    showTextScreen('Paused')
                    LastPipeTime = time.time()
                    LastBirdFlyTime = time.time()
                    LastBirdDwonTime = time.time()
                    LastPipeMoveTime = time.time()

            if event.type == MOUSEBUTTONDOWN or (event.type
            == KEYDOWN and event.key in (K_SPACE,K_UP,K_RETURN)):
                    IsBirdFly = True
                    LastBirdFlyTime = time.time()
                    bird.destination = [bird.x,bird.y-80.0]
        #bird moving
        if IsBirdFly:
            if bird.y <= bird.destination[1]+1.0:
                IsBirdFly = False
                LastBirdDwonTime = time.time()
            else:
                direction = [bird.destination[0] - bird.x,bird.destination[1] - bird.y]
                bird.x += (time.time() - LastBirdFlyTime) * direction[0] * BirdFlySpeed[0]
                bird.y += (time.time() - LastBirdFlyTime) * direction[1] * BirdFlySpeed[1]
                LastBirdFlyTime = time.time()

        else:
            bird.x += (time.time() - LastBirdDwonTime) * bird.fall_speed[0]
            bird.y += (time.time() - LastBirdDwonTime) * bird.fall_speed[1]
        #pipe moving
        for pipe in pipes:
            pipe.x += (time.time() - LastPipeMoveTime) * PipeMoveSpeed[0]
        LastPipeMoveTime = time.time()
        #check position
        if time.time() - LastPipeTime > PIPETIME:
            pipe = Pipe(WINDOWWIDTH + top_pipe_image.get_width()/2, random.randint(-200,200),[top_pipe_image,down_pipe_image])
            pipes.append(pipe)
            LastPipeTime = time.time()

        if len(pipes) > 0 and pipes[0].x + pipe.images[0].get_width()/2 < 0:
            del pipes[0]

        if not isValidPosition(pipes,bird):
            return score

        if not IsInPipe:
            for pipe in pipes:
                if check_in_pipe(bird,pipe):
                    IsInPipe = True
                    NowInPipe = pipe
                    break

        if IsInPipe and not check_in_pipe(bird,NowInPipe):
            IsInPipe = False
            score +=1
            NowInPipe = None
        #draw the world
        DrawTheWorld(bird,pipes,score)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def main():
    global FPSCLOCK,DISPLAYSURF,BACKGROUND,GAMEBACKGROUND,BASICFONT,BIGFONT,MOUSEIMAGE
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    BACKGROUND = pygame.image.load(image_path + 'background.png')
    MOUSEIMAGE = pygame.image.load(image_path + 'guangbiao.png')
    icon = pygame.image.load(image_path + 'icon.png')
    pygame.display.set_icon(icon)

    BASICFONT = pygame.font.Font(font_path + 'FreeSansBold.ttf', 18)
    BIGFONT = pygame.font.Font(font_path + 'FreeSansBold.ttf', 50)
    pygame.display.set_caption('Flappy Bird')
    if showTextScreen('Flappy Bird') == False:
        return
    while True:
        GAMEBACKGROUND = pygame.image.load(image_path + 'background.png')
        score = runGame()
        if score == False:
            return
        if showTextScreen('Game Over!Score: %i' % score) == False:
            return

if __name__ == '__main__':
    main()
