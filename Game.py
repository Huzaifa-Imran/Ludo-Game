import pygame
import Board
import random

currentColour = 0
currentPlayer = -1
playerNames = []
playerColours = []


def gameSetup():
    global boardX, boardY, smallSquare, playerColours, playerNames, screen, background
    pygame.init()
    smallSquare = 60
    width = 1000
    height = 1000
    screen = pygame.display.set_mode((width, height), 0, 32)
    pygame.display.set_caption('Ludo')
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(Board.whiteColor)
    boardX = (width - smallSquare * 15) / 2
    boardY = (height - smallSquare * 15) / 2
    for i in range(4):
        Board.Tokens.append([])
        for j in range(4):
            Board.Tokens[i].append(-1)  # put all tokens in jail at the beginning i.e -1
    drawGraphics()
    answer = int(input("How many players?(2-4): "))
    if answer >= 2 and answer <= 4:
        players = answer
    else:
        players = int(input("Please enter a number between 2 and 4"))

    print("Enter name of players.\n")
    for i in range(players):
        answer = input(f"Player {i + 1} name: ")
        playerNames.append(answer)

    availableColours = [0, 1, 2, 3]
    print("Choose colours.\nBlue = 0\nYellow = 1\nRed = 2\nGreen = 3")
    for i in range(players):
        answer = int(input(f"Colour for {playerNames[i]}: "))
        if answer in availableColours:
            availableColours.remove(answer)
        else:
            print("That colour is already selected or doesn't exists. Choosing first available colour for you.")
            answer = availableColours.pop(0)
        playerColours.append(answer)

    nextTurn()


def play():
    gameSetup()
    while len(playerColours) >= 2:
        input("Press enter to roll dice.")
        rollDice()
        drawGraphics()


def rollDice():
    roll = random.randint(1, 6)
    print(playerNames[currentPlayer], " rolled ", str(roll))
    moveableTokens(playerColours[currentPlayer], roll)
    nextTurn()


def moveableTokens(colour, roll):
    possibleTokens = []
    for i in range(4):
        if canBeMoved(colour, i, roll):
            possibleTokens.append(i)

    if len(possibleTokens) >= 2:  # if there are atleast 2 moveable tokens
        try:
            answer = int(input(f"Select a token to move: {possibleTokens}"))
        except ValueError:
            answer = 1
            print(f"Wrong token chosen. Moving token {possibleTokens[answer]}")
        won = Board.moveToken(colour, possibleTokens[answer], roll)
        print(playerNames[currentPlayer] + " has moved token " + str(possibleTokens[answer]))
        if won:
            print(playerNames[colour], " has won the game!")  # above loop doesnt returns false
            playerNames.pop(currentPlayer)
            playerColours.pop(currentPlayer)
    elif len(possibleTokens) == 1:
        Board.moveToken(colour, possibleTokens[0], roll)
        print(playerNames[currentPlayer] + " has moved token " + str(possibleTokens[0]))


def canBeMoved(colour, num, roll):
    pos = Board.Tokens[colour][num]
    if pos == -2:  # if token has finished its run
        return False  # cant move
    elif pos == -1:  # if token is in jail
        if roll == 6:
            return True  # can be spawned
        else:
            return False
    elif Board.tokenHoused[colour][num]:  # if token is inside houseSlots
        if pos + roll <= 5:
            return True
        else:
            return False
    else:
        for i in Board.blocks:
            if i == colour:  # colour of block matches with current token
                continue
            for j in i:
                if j <= (pos + roll) % 52:
                    return False  # there is a block in way, cant pass
    return True  # can move in all other scenarios


# checks the next player's turn in clockwise order
def nextTurn():
    global currentPlayer, currentColour
    currentPlayer = -1
    for i in range(len(playerColours)):
        if playerColours[i] == currentColour:
            currentPlayer = i
    currentColour = (currentColour + 1) % 4  # increment currentColour
    if currentPlayer == -1:  # if no player has current colour
        nextTurn()  # recursively call next turn which will incremement currentColour until playerColour matches


def drawGraphics():
    screen.blit(background, (0, 0))
    Board.createBoard(screen, boardX, boardY, smallSquare)
    Board.drawTokens(screen, boardX, boardY, smallSquare)
    pygame.display.flip()
