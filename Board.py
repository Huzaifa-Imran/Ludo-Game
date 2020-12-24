import pygame

whiteColor = (255, 255, 255)
yellowColor = (255, 255, 0)
greenColor = (0, 255, 0)
blueColor = (0, 0, 255)
redColor = (255, 0, 0)
blackColor = (0, 0, 0)
grayColor = (127, 127, 127)

endingPoint = [51, 12, 38, 25]
Tokens = []
# Tokens = [[1,4,8,-1], [37,48,6,18], [-1,-1,-1,-1], [9,50,43,20]]
tokenHoused = [[False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False]]
colours = [blueColor, yellowColor, redColor, greenColor]
playerHasKilled = [False, False, False, False]
blocks = [[], [], [], []]

# location of slots in which tokens cant move until six is rolled
jailSlots = [[(1.5, 1.5), (3.5, 1.5), (1.5, 3.5), (3.5, 3.5)], [(10.5, 1.5), (12.5, 1.5), (10.5, 3.5), (12.5, 3.5)], [(1.5, 10.5), (3.5, 10.5), (1.5, 12.5), (3.5, 12.5)], [(10.5, 10.5), (12.5, 10.5), (10.5, 12.5), (12.5, 12.5)]]
# location of slots which are general and can be moved onto by any token
commonSlots = [(0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 5), (6, 4), (6, 3), (6, 2), (6, 1), (6, 0), (7, 0), (8, 0), (8, 1), (8, 2), (8, 3), (8, 4),
                (8, 5), (9, 6), (10, 6), (11, 6), (12, 6), (13, 6), (14, 6), (14, 7), (14, 8), (13, 8), (12, 8), (11, 8), (10, 8), (9, 8), (8, 9), (8, 10), (8, 11),
                (8, 12), (8, 13), (8, 14), (7, 14), (6, 14), (6, 13), (6, 12), (6, 11), (6, 10), (6, 9), (5, 8), (4, 8), (3, 8), (2, 8), (1, 8), (0, 8), (0, 7)]
# location of slots which are specific to each house
houseSlots = [[(1, 7), (2, 7), (3, 7), (4, 7), (5, 7)], [(7, 1), (7, 2), (7, 3), (7, 4), (7, 5)],
                [(7, 13), (7, 12), (7, 11), (7, 10), (7, 9)],
                [(13, 7), (12, 7), (11, 7), (10, 7), (9, 7)]]
# index of commonSlots on which tokens spawn from jail
spawnPos = [1, 14, 40, 27]

def setWindow():
    global screen, boardX, boardY, smallSquare
    pygame.init()
    width = 1000
    height = 1000
    smallSquare = 60
    boardX = (width - smallSquare * 15) / 2
    boardY = (height - smallSquare * 15) / 2
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Ludo')

def updateScreen():
    screen.fill(whiteColor)
    createBoard(boardX, boardY, smallSquare)
    drawTokens(boardX, boardY, smallSquare)
    pygame.display.flip()
    pygame.display.update()
    pygame.event.clear()

def createBoard(x, y, smallSquare):
    # draw spawn position and houseSlots
    for colour in range(4):
        xAxis, yAxis = commonSlots[spawnPos[colour]]
        pygame.draw.rect(screen, colours[colour], [x + xAxis*smallSquare, y + yAxis*smallSquare, smallSquare, smallSquare], 0)
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
    
    return screen

def drawTokens(x, y, smallSquare):
    for colour in range(4):
        for number in range(4):
            pos = Tokens[colour][number]
            if pos == -2:
                continue
            elif pos == -1:
                i, j = jailSlots[colour][number]
            elif tokenHoused[colour][number]:
                print(tokenHoused)
                print(pos)
                print(colour)
                i, j = houseSlots[colour][pos]
                print(i, j)
            else:
                i, j = commonSlots[pos]
            pygame.draw.circle(screen, colours[colour], (x + (i+0.5)*smallSquare, y + (j+0.5)*smallSquare), smallSquare/2) 
            
    return screen
def moveToken(colour, number, steps):
    pos = Tokens[colour][number]
    if pos == -1:
        tokensClash(colour, number, spawnPos[colour], pos)
        Tokens[colour][number] = spawnPos[colour]
    elif tokenHoused[colour][number] and pos + steps == 5:
        Tokens[colour][number] = -2
    else: 
        if pos <= endingPoint[colour] and pos+steps > endingPoint[colour] and playerHasKilled[colour]:
            newPos = (pos + steps) % (endingPoint[colour] + 1)
            if newPos == 5:  # token has won
                newPos = -2
            tokenHoused[colour][number] = True
        else:
            newPos = (pos + steps) % 52
            tokensClash(colour, number, newPos, pos)
        Tokens[colour][number] = newPos
    for i in range(4):
        if Tokens[colour][number] != -2:  # if all tokens of a colour have not won
            return False  # player has not won
    return True  # player has won

def tokensClash(colour, number, newPos, pos): #check if there is already a token at current or new position
            for i in range(4):
                for j in range(4):
                    if pos != -1 and pos == Tokens[i][j] and number != j: # if old position is not jail and another token exists at old position means it was previously in a block
                        blocks[colour].remove(pos)
                    if newPos == Tokens[i][j]:  # token already exists at new position
                        if colour == i:  # if the token which already exists is of same colour and we have not previously removed a block
                            blocks[colour].append(newPos)
                        else:  # if the token which already exists is an enemy
                            Tokens[i][j] = -1  # put it in jail
                            playerHasKilled[colour] = True
