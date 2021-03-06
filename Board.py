import pygame
import pygame.freetype
import random

whiteColor = (255, 255, 255)
yellowColor = (255, 255, 0)
greenColor = (102, 255, 51)
blueColor = (0, 153, 255)
redColor = (255, 51, 51)
blackColor = (0, 0, 0)
grayColor = (127, 127, 127)

Tokens = []
tokenHoused = [[False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False]]
colours = [blueColor, yellowColor, greenColor, redColor]
tokenColours = [(0, 0, 204), (255, 204, 0), (0, 179, 0), (204, 0, 0)]
playerHasKilled = [False, False, False, False]
blocks = [[], [], [], []]

# location of slots in which tokens cant move until six is rolled
jailSlots = [[(1.5, 1.5), (3.5, 1.5), (1.5, 3.5), (3.5, 3.5)], [(10.5, 1.5), (12.5, 1.5), (10.5, 3.5), (12.5, 3.5)],
             [(10.5, 10.5), (12.5, 10.5), (10.5, 12.5), (12.5, 12.5)], [(1.5, 10.5), (3.5, 10.5), (1.5, 12.5), (3.5, 12.5)]]
# location of slots which are general and can be moved onto by any token
commonSlots = [(0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 5), (6, 4), (6, 3), (6, 2), (6, 1), (6, 0), (7, 0), (8, 0), (8, 1), (8, 2), (8, 3), (8, 4),
                (8, 5), (9, 6), (10, 6), (11, 6), (12, 6), (13, 6), (14, 6), (14, 7), (14, 8), (13, 8), (12, 8), (11, 8), (10, 8), (9, 8), (8, 9), (8, 10), (8, 11),
                (8, 12), (8, 13), (8, 14), (7, 14), (6, 14), (6, 13), (6, 12), (6, 11), (6, 10), (6, 9), (5, 8), (4, 8), (3, 8), (2, 8), (1, 8), (0, 8), (0, 7)]
# location of slots which are specific to each house
houseSlots = [[(1, 7), (2, 7), (3, 7), (4, 7), (5, 7)], [(7, 1), (7, 2), (7, 3), (7, 4), (7, 5)],
                [(13, 7), (12, 7), (11, 7), (10, 7), (9, 7)], [(7, 13), (7, 12), (7, 11), (7, 10), (7, 9)]]
# index of commonSlots on which tokens spawn from jail
spawnPos = [1, 14, 27, 40]
# index of common slots on which tokens end their route and move inside houseSlots
endingSlots = [51, 12, 25, 38]


def setWindow():
    global screen, boardX, boardY, smallSquare, rollButtonSurface
    pygame.init()
    smallSquare = 60
    width = smallSquare*15+100
    height = smallSquare*15+100
    boardX = (width - smallSquare * 15) / 2
    boardY = (height - smallSquare * 15) / 2
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Ludo')
    # myFont = pygame.font.SysFont('',96)
    # rollButtonSurface = myFont.render('Roll Dice', False, blackColor)

def updateScreen():
    pygame.event.clear()
    screen.fill(whiteColor)
    createBoard(boardX, boardY, smallSquare)
    drawTokens(boardX, boardY, smallSquare)
    pygame.display.update()
    pygame.event.clear()

def createBoard(x, y, smallSquare):
    # draw spawn position and houseSlots
    for colour in range(4):
        xAxis, yAxis = commonSlots[spawnPos[colour]]
        pygame.draw.rect(screen, colours[colour], [x + xAxis*smallSquare, y + yAxis*smallSquare, smallSquare, smallSquare], 0)
        xAxis, yAxis = commonSlots[endingSlots[colour]-3]
        pygame.draw.rect(screen, grayColor, [x + xAxis*smallSquare, y + yAxis*smallSquare, smallSquare, smallSquare], 0)
        if not playerHasKilled[colour]:
            houseSlotColor = grayColor
        else:
            houseSlotColor = colours[colour]
        for number in range(5):
            xAxis, yAxis = houseSlots[colour][number]
            pygame.draw.rect(screen, houseSlotColor, [x + xAxis*smallSquare, y + yAxis*smallSquare, smallSquare, smallSquare], 0)
            pygame.draw.rect(screen, blackColor, [x + xAxis*smallSquare, y + yAxis*smallSquare, smallSquare, smallSquare], 1)

    # draw common slots
    for i in range(52):
        xAxis, yAxis = commonSlots[i]   
        pygame.draw.rect(screen, blackColor, [x + xAxis*smallSquare, y + yAxis*smallSquare, smallSquare, smallSquare], 1)

    #draw starting squares and triangles
    pygame.draw.rect(screen, blueColor, [x, y, smallSquare*6, smallSquare*6], 0)
    pygame.draw.polygon(screen, blueColor, [[x + smallSquare*6, y + smallSquare*9], [x + smallSquare*6, y + smallSquare*6], [x + smallSquare*7.5, y + smallSquare*7.5]], 0)
    pygame.draw.rect(screen, whiteColor, [x + smallSquare, y + smallSquare, smallSquare*4, smallSquare*4], 0)

    # Next colour

    pygame.draw.rect(screen, yellowColor, [x + smallSquare*9, y, smallSquare*6, smallSquare*6], 0)
    pygame.draw.polygon(screen, yellowColor, [[x + smallSquare*6, y + smallSquare*6], [x + smallSquare*9, y + smallSquare*6], [x + smallSquare*7.5, y + smallSquare*7.5]], 0)
    pygame.draw.rect(screen, whiteColor, [x + smallSquare*10, y + smallSquare, smallSquare*4, smallSquare*4], 0)
    
    # Next colour

    pygame.draw.rect(screen, redColor, [x, y + smallSquare*9, smallSquare*6, smallSquare*6], 0)
    pygame.draw.polygon(screen, redColor, [[x + smallSquare*9, y + smallSquare*9], [x + smallSquare*6, y + smallSquare*9], [x + smallSquare*7.5, y + smallSquare*7.5]], 0)
    pygame.draw.rect(screen, whiteColor, [x + smallSquare, y + smallSquare*10, smallSquare*4, smallSquare*4], 0)

    # Next colour
    
    pygame.draw.rect(screen, greenColor, [x + smallSquare*9, y + smallSquare*9, smallSquare*6, smallSquare*6], 0)
    pygame.draw.polygon(screen, greenColor, [[x + smallSquare*9, y + smallSquare*6], [x + smallSquare*9, y + smallSquare*9], [x + smallSquare*7.5, y + smallSquare*7.5]], 0)
    pygame.draw.rect(screen, whiteColor, [x + smallSquare*10, y + smallSquare*10, smallSquare*4, smallSquare*4], 0)

    # draw roll dice button

    # pygame.draw.rect(screen, grayColor, [x + smallSquare*5, y - 125, smallSquare*5, 100], 0)
    # screen.blit(rollButtonSurface, (x + smallSquare*5+5, y - 105))
    # pygame.display.flip()

def drawTokens(x, y, smallSquare):
    for colour in range(4):
        for number in range(4):
            pos = Tokens[colour][number]
            if pos == -2: # if token has won
                continue
            elif pos == -1: # if token is in jail
                i, j = jailSlots[colour][number]
            elif tokenHoused[colour][number]: # if token is in house slots
                i, j = houseSlots[colour][pos]
            else: # if token is in common slots
                i, j = commonSlots[pos]
            pygame.draw.circle(screen, tokenColours[colour], (x + (i+0.5)*smallSquare, y + (j+0.5)*smallSquare), smallSquare/3) # draw a small circle at position of token

    for colour in range(4):
        for pos in blocks[colour]: # if a block exists
            i, j = commonSlots[pos]
            blockCount = blocks[colour].count(pos)
            pygame.draw.circle(screen, tokenColours[colour], (x + (i+0.5)*smallSquare, y + (j+0.5)*smallSquare), smallSquare/2) # draw a big circle at position of block

def canBeMoved(colour, num, roll):
    pos = Tokens[colour][num]
    if pos == -2:  # if token has finished its run
        return False  # cant move
    elif pos == -1:  # if token is in jail
        if roll == 6:
            return True  # can be spawned
        else:
            return False
    elif tokenHoused[colour][num]:  # if token is inside houseSlots
        if pos + roll <= 5:
            return True
        else:
            return False
    else:
        for steps in range(1, roll+1):
            for col in range(4):
                if col != colour and (pos + steps) % 52 in blocks[col]:
                    return False
    return True  # can move in all other scenarios

def moveToken(colour, number, steps):
    pos = Tokens[colour][number]
    if pos == -1:
        tokensClash(colour, number, spawnPos[colour], pos)
        Tokens[colour][number] = spawnPos[colour]
    elif tokenHoused[colour][number] and pos + steps == 5:
        Tokens[colour][number] = -2
    else:
        if pos <= endingSlots[colour] and pos+steps > endingSlots[colour] and playerHasKilled[colour]:
            newPos = (pos + steps) % (endingSlots[colour] + 1)
            tokenHoused[colour][number] = True
            if newPos == 5:  # token has won
                newPos = -2
        else:
            newPos = (pos + steps) % 52
            tokensClash(colour, number, newPos, pos)
        Tokens[colour][number] = newPos
    for i in range(4):
        if Tokens[colour][i] != -2:  # if all tokens of a colour have not won
            return False  # player has not won
    return True  # player has won

def tokensClash(colour, number, newPos, pos): #check if there is already a token at current or new position
    if not tokenHoused[colour][number]:
        if pos in blocks[colour]:
            blocks[colour].remove(pos)
            print(blocks)
        for i in range(4):
            for j in range(4):
                if newPos == Tokens[i][j] and not tokenHoused[i][j]:  # token already exists at new position
                    if colour == i:
                        blocks[colour].append(newPos)
                        print(blocks)
                        return
                    else:
                        Tokens[i][j] = -1  # put it in jail
                        playerHasKilled[colour] = True


def drawDice():
    size = smallSquare*2            # Size of window/dice
    spsz = size/10                  # size of spots
    mx = boardX + smallSquare*7.5             # mid-point of dice (or die?)
    my = boardY + smallSquare*7.5
    l = boardX + smallSquare*7
    t = boardY + smallSquare*7             # location of left and top spots
    r = boardX + smallSquare*8
    b = boardY + smallSquare*8              # location of right and bottom spots
    rolling = 12                    # times that dice rolls before stopping
    n = int()
    for i in range(rolling):        # roll the die...
        n=random.randint(1,6)       # random number between 1 &amp;amp; 6
        pygame.draw.rect(screen, whiteColor, [boardX + smallSquare*6.5, boardY + smallSquare*6.5, size, size], 0)
        if n % 2 == 1:
            pygame.draw.circle(screen,blackColor,(mx,my),spsz)  # middle spot
        if n==2 or n==3 or n==4 or n==5 or n==6:
            pygame.draw.circle(screen,blackColor,(l,b),spsz)  # left bottom
            pygame.draw.circle(screen,blackColor,(r,t),spsz)  # right top
        if n==4 or n==5 or n==6:
            pygame.draw.circle(screen,blackColor,(l,t),spsz)  # left top
            pygame.draw.circle(screen,blackColor,(r,b),spsz)  # right bottom
        if n==6:
            pygame.draw.circle(screen,blackColor,(mx,b),spsz)  # middle bottom
            pygame.draw.circle(screen,blackColor,(mx,t),spsz)  # middle top
    
        pygame.display.update()
        pygame.time.delay(400)
    return n