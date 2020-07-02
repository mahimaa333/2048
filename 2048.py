import pygame,sys,random,time
from pygame.locals import *

BOARDWIDTH = 4
BOARDHEIGHT = 4
TILESIZE = 80
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FPS = 40
BLANK = None
SCORE = 0

XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH-1))) / 2)
YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT-1))) / 2)

UP = 'up'
DOWN = 'down'
RIGHT = 'right'
LEFT = 'left'

pygame.init()

WHITE = (255,255,255)
TEXTCOLOR = WHITE
GRID_COLOR = (64,58,54)
TILECOLOR = GRID_COLOR
EMPTY_CELL_COLOR = (76,70,66)
SCORE_LABEL_FONT = pygame.font.Font('freesansbold.ttf', 20)
SCORE_FONT = pygame.font.Font('freesansbold.ttf', 20)
GAME_OVER_FONT = pygame.font.Font('freesansbold.ttf', 30)
GAME_OVER_FONT_COLOR = (238, 228, 218, 0.73)
# WINNER_BG = "#ffcc00"
GAME_OVER = (64,58,54)
CELL_COLORS = {
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}
BGCOLOR = "#eee4da"

CELL_NUMBER_COLORS = {
    2: (41,36,34),
    4: (41,36,34),
    8: (100,100,100),
    16: (100,100,100),
    32: (100,100,100),
    64: (100,100,100),
    128: (100,100,100),
    256: (100,100,100),
    512: (100,100,100),
    1024: (100,100,100),
    2048: (100,100,100)
}

CELL_NUMBER_FONTS = {
    2: pygame.font.Font('freesansbold.ttf', 55),
    4: pygame.font.Font('freesansbold.ttf', 55),
    8: pygame.font.Font('freesansbold.ttf', 55),
    16: pygame.font.Font('freesansbold.ttf', 55),
    32: pygame.font.Font('freesansbold.ttf', 55),
    64: pygame.font.Font('freesansbold.ttf', 55),
    128: pygame.font.Font('freesansbold.ttf', 50),
    256: pygame.font.Font('freesansbold.ttf', 50),
    512: pygame.font.Font('freesansbold.ttf', 50),
    1024: pygame.font.Font('freesansbold.ttf', 45),
    2048: pygame.font.Font('freesansbold.ttf', 45)
}

def main():
    global FPSCLOCK,BASICFONT, DISPLAYSURF, NEW_SURF, NEW_RECT,SCORE

    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    pygame.display.set_caption('2048')
    FPSCLOCK = pygame.time.Clock()
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    NEW_SURF, NEW_RECT = makeText('New Game',TEXTCOLOR,TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 60)
    mainBoard = getNewBoard()

    while True:
        slideTo = None
        msg = 'Press the arrow keys to slide'
        drawBoard(mainBoard,msg)
        checkForQuit()
        
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                spotx, spoty = getSpotClicked(mainBoard, event.pos[0], event.pos[1])
                if (spotx, spoty) == (None, None):
                    if NEW_RECT.collidepoint(event.pos):
                        SCORE = 0
                        mainBoard = getNewBoard()
            
            if isValidMove(mainBoard):
                if event.type == KEYUP:
                    if event.key == K_n:
                        SCORE = 0
                        mainBoard = getNewBoard()
                    if event.key in (K_LEFT, K_a):
                        for i in range(0,1):
                            move(mainBoard)
                        if isPossible(mainBoard) :
                            makeMove(mainBoard)
                            mergeTiles(mainBoard)
                            placeRandomly(mainBoard)
                        for j in range(0,3%4):
                            move(mainBoard)
                            
                    elif event.key in (K_RIGHT, K_d):
                        for i in range(0,3):
                            move(mainBoard)
                        if isPossible(mainBoard) :
                            makeMove(mainBoard)
                            mergeTiles(mainBoard)
                            placeRandomly(mainBoard)
                        for j in range(0,1%4):
                            move(mainBoard)
                            
                    elif event.key in (K_UP, K_w):
                        for i in range(0,0):
                            move(mainBoard)
                        if isPossible(mainBoard) :
                            makeMove(mainBoard)
                            mergeTiles(mainBoard)
                            placeRandomly(mainBoard)
                        for j in range(0,4%4):
                            move(mainBoard)
                            
                    elif event.key in (K_DOWN, K_s):
                        for i in range(0,2):
                            move(mainBoard)
                        if isPossible(mainBoard) :
                            makeMove(mainBoard)
                            mergeTiles(mainBoard)
                            placeRandomly(mainBoard)
                        for j in range(0,2%4):
                            move(mainBoard)
                    
        pygame.display.update()

def terminate():
    pygame.quit()
    sys.exit()

def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)

def placeRandomly(board):
    list = []
    for i in range(BOARDWIDTH):
        for j in range(BOARDHEIGHT):
            if board[i][j] == 0:
                list.append([i,j])
    number = getRandomNumber()
    pos = random.choice(list)
    board[pos[0]][pos[1]] = number

def getRandomNumber():
    list = [2,4]
    num = random.choice(list)
    return num

def getStartingBoard():
    board = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    placeRandomly(board)
    placeRandomly(board)
    return board

def getNewBoard():
    board = getStartingBoard()
    drawBoard(board,'')
    pygame.display.update()
    return board

def mergeTiles(board):
    global SCORE
    for i in range(BOARDWIDTH):
        for j in range(BOARDHEIGHT-1):
            if board[i][j] == board[i][j+1] and board[i][j] != 0:
                board[i][j] = board[i][j]*2
                board[i][j+1] = 0
                SCORE += board[i][j]
                makeMove(board)

def makeMove(board):
    for i in range(BOARDWIDTH):
        for j in range(BOARDHEIGHT-1):
            while board[i][j] == 0 and sum(board[i][j:]) > 0:
                for k in range(j,BOARDHEIGHT-1):
                    board[i][k] = board[i][k+1]
                board[i][BOARDHEIGHT-1] = 0

def isPossible(board):
    for i in range(BOARDWIDTH):
        for j in range(1,BOARDHEIGHT):
            if board[i][j-1] == 0 and board[i][j] > 0:
                return True 
            elif (board[i][j-1] == board[i][j]) and board[i][j-1] != 0:
                return True
    return False

def isValidMove(board):
    for i in range(BOARDWIDTH):
        for j in range(BOARDHEIGHT):
            if board[i][j] == 0:
                return True
    
    for i in range(BOARDWIDTH):
        for j in range(BOARDHEIGHT-1):
            if board[i][j] == board[i][j+1]:
                return True
            elif board[j][i] == board[j+1][i]:
                return True
    return False 

def move(board):
    for i in range(0,int(BOARDWIDTH /2)):
        for j in range(i,BOARDWIDTH - i- 1):
            temp1 = board[i][j]
            temp2 = board[BOARDWIDTH - 1 - j][i]
            temp3 = board[BOARDWIDTH - 1 - i][BOARDWIDTH - 1 - j]
            temp4 = board[j][BOARDWIDTH - 1 - i]

            board[BOARDWIDTH - 1 - j][i] = temp1
            board[BOARDWIDTH - 1 - i][BOARDWIDTH - 1 - j] = temp2
            board[j][BOARDWIDTH - 1 - i] = temp3
            board[i][j] = temp4

def getLeftTopOfTile(tileX, tileY):
    left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
    top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
    return (left, top)

def getSpotClicked(board, x, y):
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tileRect.collidepoint(x, y):
                return (tileX, tileY)
    return (None, None)

def drawTile(tileX,tileY,color,numberColor,font,number,adjx=0,adjy=0):
    left,top = getLeftTopOfTile(tileX,tileY)
    pygame.draw.rect(DISPLAYSURF,color,(left + adjx, top + adjy, TILESIZE, TILESIZE))
    textSurf = font.render(str(number),True,numberColor)
    textRect = textSurf.get_rect()
    textRect.center = left + int(TILESIZE/2) + adjx, top + int(TILESIZE/2) + adjy
    DISPLAYSURF.blit(textSurf,textRect)

def makeText(text,color,bgcolor,top,left):
    textSurf = BASICFONT.render(text,True,color,bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top,left)
    return (textSurf,textRect)

def drawBoard(board,message):
    DISPLAYSURF.fill((255,255,255))
    if message:
        textSurf,textRect = makeText(message,(0,0,0),CELL_COLORS[2],5,5)
        DISPLAYSURF.blit(textSurf,textRect)

    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            num = board[tileX][tileY]
            if num!=0:
                drawTile(tileX,tileY,CELL_COLORS[num],CELL_NUMBER_COLORS[num],CELL_NUMBER_FONTS[num],num,0,0)
            else:
                drawTile(tileX,tileY,EMPTY_CELL_COLOR ,EMPTY_CELL_COLOR,SCORE_FONT,num,0,0)
                

    left,top = getLeftTopOfTile(0,0)
    width = BOARDWIDTH*TILESIZE
    height = BOARDHEIGHT*TILESIZE
    pygame.draw.rect(DISPLAYSURF,GRID_COLOR,(left-5,top-5,width+11,height+11),4)

    DISPLAYSURF.blit(NEW_SURF,NEW_RECT)
    drawScore(SCORE)
    if not isValidMove(board):
        gameOver()

def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, EMPTY_CELL_COLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)
    
def gameOver():
    DISPLAYSURF.fill(GAME_OVER)
    surf1 = GAME_OVER_FONT.render("GameOver!",1,GAME_OVER_FONT_COLOR)
    surf2 = GAME_OVER_FONT.render("Score : "+str(SCORE),1,GAME_OVER_FONT_COLOR)
    surf3 = GAME_OVER_FONT.render("Press 'New Game' to play again!! ",1,GAME_OVER_FONT_COLOR)
    DISPLAYSURF.blit(NEW_SURF,NEW_RECT)
    
    DISPLAYSURF.blit(surf1,(50,100))
    DISPLAYSURF.blit(surf2,(50,200))
    DISPLAYSURF.blit(surf3,(50,300))

if __name__ == '__main__':
    main()
