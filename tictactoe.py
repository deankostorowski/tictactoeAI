import random
import math
import re

#Main game loop which also sets up the board, score and asks user for a game type input
def ticTacToe():
    playing = True
    X = ""
    O = ""
    totalGameMoves = 0
    board = [["_","_","_"],["_","_","_"],["_","_","_"]]
    score = [0,0,0,0,0,0,0,0] #[row1, row2, row3, col1, col2, col3, dig1, dig2]
    scoreDict = {0:[[1,1],[1,2],[1,3]],
                 1:[[2,1],[2,2],[2,3]],
                 2:[[3,1],[3,2],[3,3]],
                 3:[[1,1],[2,1],[3,1]],
                 4:[[1,2],[2,2],[3,2]],
                 5:[[1,3],[2,3],[3,3]],
                 6:[[1,1],[2,2],[3,3]],
                 7:[[3,1],[2,2],[1,3]],}
    X,O = setupGame()
    printBoard(board)
    while(playing):
        if (totalGameMoves % 2 == 0):
            currentMove = X
            currentMarker = "X"
        else:
            currentMove = O
            currentMarker = "O"

        if currentMove == "user":
            score = userMove(board, score, currentMarker)
        elif(currentMove == "easy"):
            print("Making move level " + '"easy"')
            easyMove(board, score, currentMarker)
        elif(currentMove == "medium"):
            print("Making move level " + '"medium"')
            mediumMove(board, score, currentMarker, scoreDict)
        elif (currentMove == "hard"):
            print("Making move level " + '"hard"')
            hardMove(board, score, totalGameMoves, currentMarker)
        printBoard(board)
        totalGameMoves += 1
        if checkWin(score, totalGameMoves):
            playing = False

#Asks the user for the coordinates they would like to place their marker
def userMove(board, score, currentMarker):
    hasMoved = False
    while not hasMoved:
        nextMovePosition = re.sub(' +', ' ', input("Enter the coordinates: ").strip())
        if len(nextMovePosition) != 3:
            print("You should enter numbers!" )
        else:
            try:
                row = int(nextMovePosition.split()[0])
                col = int(nextMovePosition.split()[1])
                if not ((0 < col < 4) and (0 < row < 4)):
                    print("Coordinates should be from 1 to 3!")
                elif not (board[row-1][col-1] == "_"):
                    print("This cell is occupied! Choose another one!")
                else:
                    # currentTurn = currentMarker
                    board[row-1][col-1] = currentMarker
                    hasMoved = True
                    score = updateScore(score, currentMarker, col, row)
                    return score
            except ValueError:
                print("You should enter numbers!")

#Easy AI performs a random move on the board
def easyMove(board, score, currentMarker):
    cpuMoved = False
    while not cpuMoved:
        col = random.randint(1, 3)
        row = random.randint(1, 3)
        if (board[row - 1][col - 1] == "_"):
            board[row - 1][col - 1] = currentMarker
            score = updateScore(score, currentMarker, col, row)
            cpuMoved = True

#Medium AI checks for a winning move or to block a win before moving randomly
def mediumMove(board, score, currentMarker, scoreDict):
    cpuMoved = False
    win = False
    block = False
    while not cpuMoved:
        win = checkPossibleWin(board, score, currentMarker, scoreDict)
        if not win:
            block = checkPossibleBlock(board, score, currentMarker, scoreDict)
        if not block and not win:
            easyMove(board, score, currentMarker)
            cpuMoved = True
        if win or block:
            cpuMoved = True

#Minimax algorithm setup for Hard AI move
def hardMove(board, score, totalGameMoves, currentMarker):
    isMaximizing = True if currentMarker == "X" else False
    if totalGameMoves == 0:
        bestMove = [0, 0]
    elif isMaximizing:
        bestScore = -math.inf
        bestMove = [-1, -1]
        for row, i in enumerate(board):
            for col, j in enumerate(i):
                if board[row][col] == "_":
                    board[row][col] = currentMarker
                    minimaxScore = minimax(board, totalGameMoves+1, False)
                    board[row][col] = "_"
                    if minimaxScore > bestScore:
                        bestScore = minimaxScore
                        bestMove = [row, col]
    else:
        bestScore = math.inf
        for row, i in enumerate(board):
            for col, j in enumerate(i):
                if board[row][col] == "_":
                    board[row][col] = currentMarker
                    minimaxScore = minimax(board, totalGameMoves+1, True)
                    board[row][col] = "_"
                    if minimaxScore < bestScore:
                        bestScore = minimaxScore
                        bestMove = [row, col]
    board[bestMove[0]][bestMove[1]] = currentMarker
    score = updateScore(score, currentMarker, bestMove[1]+1, bestMove[0]+1)

#Minimax algorithm implementation to determind Hard AI move
def minimax(board, totalGameMoves, isMaximizing):
    defaultScores = {"X": 10, "O" : -10, "Tie" : 0}
    result = checkWinMiniMax(board, totalGameMoves)
    if result != "":
        return defaultScores.get(result)
    if isMaximizing:
        bestScore = -math.inf
        for row, i in enumerate(board):
            for col, j in enumerate(i):
                if board[row][col] == "_":
                    board[row][col] = "X"
                    bestScore = max(bestScore, minimax(board, totalGameMoves+1, False))
                    board[row][col] = "_"
        return bestScore
    else:
        bestScore = math.inf
        for row, i in enumerate(board):
            for col, j in enumerate(i):
                if board[row][col] == "_":
                    board[row][col] = "O"
                    bestScore = min(bestScore, minimax(board, totalGameMoves+1, True))
                    board[row][col] = "_"
        return bestScore

#Helper to check if the minimax algorithm has found a winning state of the board
def checkWinMiniMax(board, totalGameMoves):
    #rows
    for row in range(3):
        if len(set([board[row][0], board[row][1], board[row][2]]))==1 and board[row][0] != "_":
            return board[row][0]
    #cols
    for col in range(3):
        if len(set([board[0][col], board[1][col], board[2][col]]))==1 and board[0][col] != "_":
            return board[0][col]
    #diag1
    if len(set([board[0][0], board[1][1], board[2][2]]))==1 and board[0][0] != "_":
        return board[0][0]

    #diag2
    if len(set([board[2][0], board[1][1], board[0][2]]))==1 and board[2][0] != "_":
        return board[2][0]

    if totalGameMoves == 9:
        return "Tie"
    else:
        return ""

#Checks if the Medium AI has a winning move
def checkPossibleWin(board, score, currentMarker, scoreDict):
    if currentMarker == "X":
        scoreToLookFor = 2
    else:
        scoreToLookFor = -2
    for scoreIndex, v in enumerate(score):
        if v == scoreToLookFor:
            boardSpotsToCheck = scoreDict.get(scoreIndex)
            for s in boardSpotsToCheck:
                row = s[0]
                col = s[1]
                if board[row-1][col-1] == "_":
                    board[row-1][col-1] = currentMarker
                    score = updateScore(score, currentMarker, col, row)
                    return True
    return False

#Checks if the Medium AI can block the opponent from winning
def checkPossibleBlock(board, score, currentMarker, scoreDict):
    if currentMarker == "X":
        scoreToLookFor = -2
    else:
        scoreToLookFor = 2
    for scoreIndex, v in enumerate(score):
        if v == scoreToLookFor:
            boardSpotsToCheck = scoreDict.get(scoreIndex)
            for s in boardSpotsToCheck:
                row = s[0]
                col = s[1]
                if board[row-1][col-1] == "_":
                    board[row-1][col-1] = currentMarker
                    score = updateScore(score, currentMarker, col, row)
                    return True
    return False

#Helper to update the score
def updateScore(score, currentMarker, col, row):
    modifier = 0
    if (currentMarker == "X"):
        modifier = 1
    if (currentMarker == "O"):
        modifier = -1
    score[row-1] += modifier
    score[3+(col-1)] += modifier
    if col == row:
        score[6] += modifier
    if (col == 3 and row == 1) or (col == 1 and row == 3) or (col == 2 and row == 2):
        score[7] += modifier
    return score

#Checks the score to see if X or O has won the game
def checkWin(score, totalGameMoves):
    if 3 in score:
        print ("X wins")
        return True
    elif -3 in score:
        print ("O wins")
        return True
    elif totalGameMoves == 9:
        print("Draw")
        return True
    else:
        return False

#Inital setup from the user to determine which Tic Tac Toe game they would like to play
def setupGame():
    settingUpGame = True
    validCommands = ["start", "exit", "easy", "medium", "hard", "user"]
    while(settingUpGame):
        startCommand = input("Input command: ").strip().lower()
        #startCommand = "start hard user"
        invalidCommand = False
        startList = startCommand.split()
        if startList[0] == "exit":
            exit()
        if len(startList) != 3 or startList[0] != "start":
            print("Bad parameters!")
            invalidCommand = True
            continue
        for i in startList:
            if i not in validCommands:
                print("Bad parameters")
                invalidCommand = True
        if(not invalidCommand):
            X = startList[1]
            O = startList[2]
            return X, O

#Helper function to print entire board in proper formatting
def printBoard(board):
    print("---------")
    for r in (board):
        print("|" + " " + r[0] + " " + r[1] + " " + r[2] + " " + "|")
    print("---------")

ticTacToe()
