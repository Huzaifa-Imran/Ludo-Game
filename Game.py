import Board
import random
import copy as cp

currentColour = 0
playerNames = []
playerColours = []
colourOrder = ['blue', 'yellow', 'green', 'red']
sixesRolled = 0

def gameSetup():
    Board.setWindow()
    for i in range(4):
        Board.Tokens.append([])
        for j in range(4):
            Board.Tokens[i].append(-1)  # put all tokens in jail at the beginning i.e -1
    Board.updateScreen()
    answer = int(input("How many players?(2-4): "))
    while(True):
        if answer >= 2 and answer <= 4:
            players = answer
            break
        else:
            answer = int(input("Please enter a number between 2 and 4"))

    print("Enter name of players.\n")
    for i in range(players):
        answer = input(f"Player {i + 1} name: ")
        playerNames.append(answer)

    availableColours = [0, 1, 2, 3]
    answer = input("Do you want to choose colours yourself?('yes' or 'no'): ")
    if answer == "yes":
        print("Blue = 0\nYellow = 1\nGreen = 2\nRed = 3")
        for i in range(players):
            if len(availableColours) > 1:
                answer = int(input(f"Colour for {playerNames[i]}{availableColours}: "))
                if answer in availableColours:
                    availableColours.remove(answer)
                else:
                    answer = availableColours.pop(0)
                    print(f"That colour is already selected or doesn't exists. Assigning you colour {colourOrder[answer]}")
            else:
                answer = availableColours[0]
            playerColours.append(answer)
    else:
        random.shuffle(availableColours)
        for i in range(players):
            playerColours.append(availableColours[i])
    nextTurn()


def play():
    gameSetup()
    while len(playerColours) >= 2:
        input(f"\nCurrent Turn: {playerNames[currentPlayer]}({colourOrder[currentPlayer]}) Press enter to roll dice.")
        rollDice()
        Board.updateScreen()


def rollDice():
    global sixesRolled, tempState
    roll = random.randint(1, 6)
    print(f"{playerNames[currentPlayer]} rolled {roll}")
    if roll == 6:
        sixesRolled += 1
        if sixesRolled != 3:
            if sixesRolled == 1:
                tempState = (cp.copy(Board.Tokens), cp.copy(Board.playerHasKilled[currentPlayer]), cp.copy(Board.tokenHoused[currentPlayer]), cp.copy(Board.blocks[currentPlayer]))
            moveableTokens(playerColours[currentPlayer], roll)
        else:
            Board.Tokens, Board.playerHasKilled[currentPlayer], Board.tokenHoused[currentPlayer], Board.blocks[currentPlayer] = tempState
            print(f"{playerNames[currentPlayer]} rolled three cosecutive sixes! Cancelling previous moves.")
            sixesRolled = 0
            
    else:
        sixesRolled = 0
        moveableTokens(playerColours[currentPlayer], roll)

    if sixesRolled == 0:
        nextTurn()

def moveableTokens(colour, roll):
    possibleTokens = []
    for i in range(4):
        if canBeMoved(colour, i, roll):
            possibleTokens.append(i)

    if len(possibleTokens) >= 1:  # if there are atleast 2 moveable tokens
        if len(possibleTokens) >= 2:
            while(True):
                try:
                    answer = int(input(f"Select a token to move{possibleTokens}: "))
                    if answer in possibleTokens:
                        break
                    else:
                        print("That token is not available")
                except ValueError:
                    print(f"Invalid input.")
        else:
            answer = 0
            won = Board.moveToken(colour, possibleTokens[0], roll)
        won = Board.moveToken(colour, possibleTokens[answer], roll)
        print(f"{playerNames[currentPlayer]} has moved token {possibleTokens[answer]}")
        if won:
            print(f"{playerNames[colour]} has won the game!")  # above loop doesnt returns false
            playerNames.pop(currentPlayer)
            playerColours.pop(currentPlayer)


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

