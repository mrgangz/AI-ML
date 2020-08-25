### COPYRIGHT MITUL @ 2020 MAY 12###
# This code will take in a oska board in the format of "[www], [--], [-], [-b], [bb-]" where w represents
# player white, and b represents player black. Any size board may be used, so long as the board maintains 2n -1 rows, 
# where n is the number of slots of the biggest rows, which must be the top and bottom rows.
import copy


### class to keep track of boards parents
class OskaBoard:
    def __init__(self, b):
        self.b = b
        self.score = boardEvaluator(b)



### top function to call in arguments from terminal
def oskaplayer(list, player, numberOfMoves):
    board = makeBoard(list)     # create board representation

    if numberOfMoves < 1:
        printBoard(board)

    if player == 'w':
        move = minimax(OskaBoard(board), numberOfMoves, True)     # call minimax starting with max
        printBoard(move.b)  # print out best move
    if player == 'b':
        move = minimax(OskaBoard(board), numberOfMoves, False)    # call minimax starting with min
        printBoard(move.b)  # print out best move




### function for minimax algorithm, takes board Object, max depth, isMax? bool. Max is white, Min is black
def minimax(boardObj, maxDepth, isMax):

    if maxDepth == 0 or gameWon(boardObj.b):  # if this is the last board state possible or game won:
        return boardObj    # base case, return evaluated score

    if isMax:   # if whites level turn, generate all white moves and rank them
        #maxScore = -1000
        maxBoard = boardObj
        boardObj.score = -100   # worst case score for starting board
        for i in movegen(boardObj.b, 'w'):
            for j in i:
                eBoard = minimax(OskaBoard(j), maxDepth - 1, not isMax) # send the child of j to recurse w/ one less depth and change player
                #maxScore = max(eval, maxScore)
                if eBoard.score > maxBoard.score:
                    maxBoard = eBoard
        #printBoard(maxBoard.b)
        return maxBoard

    else:       # black turn, find minimum for this level of black moves generated
        #minScore = 1000
        minBoard = boardObj
        boardObj.score = 100    # worst case for starting board
        for i in movegen(boardObj.b, 'b'):
            for j in i:
                eBoard = minimax(OskaBoard(j), maxDepth - 1, not isMax)
                #minScore = min(eval, minScore)
                if eBoard.score < minBoard.score:
                    minBoard = eBoard
        return minBoard




### function to determine closeness to end state for a board and player
def boardEvaluator(board):
    # if the game is a winning state, return 100 or -100 depending on who won
    if gameWon(board) != 0:
        return gameWon(board)

    score = 0

    # num of white pieces - num of black pieces
    score = score + (countPiece(board, 'w') - countPiece(board, 'b'))

    lastRow = board[len(board) - 1]
    firstRow = board[0]

    # reward the player for having pieces at the opposing players starting row
    # num of white pieces at bottom row
    for i in lastRow:
        if i == 'w':
            score = score + 1
    # num of black pieces in the top row
    for i in firstRow:
        if i == 'b':
            score = score - 1

    return score    # return evaluated board



### function to count the number of pieces in board
def countPiece(board, player):
    count = 0

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == player:
                count = count + 1

    return count


### function to check if a board state is a winning board
def gameWon(board):
    # different win states: no more black, no more white, all white on bottom row, all black on top row
    checkWhite = checkBlack = firstRowBlack = lastRowWhite = True

    # go through board to see if the board is a winning state
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 'w':
                checkWhite = False  # if we find a white piece, game not done yet
            if board[i][j] =='b':
                checkBlack = False  # if we find a black piece, game not won yet

            if i == len(board) - 1:  # Check if last row white
                if board[i][j] != 'w':
                    lastRowWhite = False
            if i == 0:              # check if first row is now black
                if board[i][j] != 'b':
                    firstRowBlack = False

    # check if black won
    if checkWhite or firstRowBlack:
        return -10000   # -10 indicates black winning
    # check if white won
    elif checkBlack or lastRowWhite:
        return 10000    # 10 indicates white winning
    else:
        return 0    # no winner



### function to represent board as a 2d matrix
def makeBoard(rows):
    board = []  # final product
    for i in range(len(rows)):
        row = []    # contents in one row
        for j in rows[i]:
            if j == "-" or j == 'w' or j == 'b':    # check if j is not apostrophe from string
                row.append(j)
        board.append(row)   # add row to the final board

    return board    # return board



### function to make board printed out like in specification
def printBoard(board):
    numRows = len(board)

    print("[", end="")
    for row in range(numRows):
        print("'", end="")
        for element in board[row]:
            print(element, end="")
        print("'", end="")
        if row != numRows - 1:
            print(", ", end="")

    print("]")  # final closing bracket



### function that takes the board and current player and generates new moves
def movegen(rows, player):
    #length = len(rows)  # get length of list so we can seperate strings into 2x2 matrix
    board = makeBoard(rows)


    possibleMoves = []  # empty array to store possible moves in
    if player == 'w':
        possibleMoves = generateWhiteMoves(board)
        return possibleMoves
    elif player == 'b':
        possibleMoves = generateBlackMoves(board)
        return possibleMoves
    else:
        print("invalid player selection try again")
        return -1

    return possibleMoves


### function to generate moves possible if current turn is player white
def generateWhiteMoves(board):
    possibleMoves = []

    numRows = len(board) # number of rows in board
    for i in range(numRows):
        rowLen = len(board[i])  # length of specific row in board
        for j in range(rowLen):
            if board[i][j] == 'w':  # if element is white player piece we generate possible moves for that piece
                possibleMoves.append(moveWhitePiece(board, (i,j)))

    return possibleMoves



### function that generates possible move of specific white piece
def moveWhitePiece(board, coordinate):
    i = coordinate[0]   # i from matrix to index
    j = coordinate[1]   # j from matrix to index
    moves = []
    numRows = len(board)    # number of rows in board

    # make sure that there is another row to the bottom
    if i + 1 < numRows:
        if len(board[i]) > len(board[i + 1]):
            # first check if diagonal down-left is possible
            if j > 0:
                if board[i + 1][j - 1]  == '-':     # if one row down one to the left is open
                    newBoard = copy.deepcopy(board) # proceed to change board
                    newBoard[i + 1][j - 1] = 'w'
                    newBoard[i][j] = '-'
                    moves.append(newBoard)
                elif board[i + 1][j - 1] == 'b':    # if left-down is a black piece, check if we can skip over it
                    if i + 2 < numRows and j - 1 > 0:
                        if len(board[i + 1]) > len(board[i + 2]):
                            if board[i + 2][j - 2] == '-':  # check if space to skip over black is there or not
                                newBoard = copy.deepcopy(board)
                                newBoard[i + 2][j - 2] = 'w'
                                newBoard[i + 1][j - 1] = '-'
                                newBoard[i][j] = '-'
                                moves.append(newBoard)
                        else:
                            if board[i + 2][j - 1] == '-':  # check if space to skip over black is there or not
                                newBoard = copy.deepcopy(board)
                                newBoard[i + 2][j - 1] = 'w'
                                newBoard[i + 1][j - 1] = '-'
                                newBoard[i][j] = '-'
                                moves.append(newBoard)

            # next check if diagonal down-right is possible
            if j < len(board[i + 1]):
                if board[i + 1][j] == '-':
                    newBoard = copy.deepcopy(board)
                    newBoard[i + 1][j] = 'w'
                    newBoard[i][j] = '-'
                    moves.append(newBoard)
                elif board[i + 1][j] == 'b':
                    if i + 2 < numRows:
                        if len(board[i + 1]) > len(board[i + 2]):
                            if j < len(board[i + 2]):
                                if board[i + 2][j] == '-':
                                    newBoard = copy.deepcopy(board)
                                    newBoard[i + 2][j] = 'w'
                                    newBoard[i + 1][j] = '-'
                                    newBoard[i][j] = '-'
                                    moves.append(newBoard)
                        else:
                            if board[i + 2][j + 1] == '-':
                                newBoard = copy.deepcopy(board)
                                newBoard[i + 2][j + 1] = 'w'
                                newBoard[i + 1][j] = '-'
                                newBoard[i][j] = '-'
                                moves.append(newBoard)

        else:
            if board[i + 1][j] == '-':  # if one row down one to the left is open
                newBoard = copy.deepcopy(board)  # proceed to change board
                newBoard[i + 1][j] = 'w'
                newBoard[i][j] = '-'
                moves.append(newBoard)
            elif board[i + 1][j] == 'b':  # if left-down is a black piece, check if we can skip over it
                if i + 2 < numRows:
                    if board[i + 2][j] == '-':  # check if space to skip over black is there or not
                        newBoard = copy.deepcopy(board)
                        newBoard[i + 2][j] = 'w'
                        newBoard[i + 1][j] = '-'
                        newBoard[i][j] = '-'
                        moves.append(newBoard)

            if board[i + 1][j + 1] == '-':
                newBoard = copy.deepcopy(board)
                newBoard[i + 1][j + 1] = 'w'
                newBoard[i][j] = '-'
                moves.append(newBoard)
            elif board[i + 1][j + 1] == 'b':
                if i + 2 < numRows:
                    if board[i + 2][j + 2] == '-':
                        newBoard = copy.deepcopy(board)
                        newBoard[i + 2][j + 2] = 'w'
                        newBoard[i + 1][j + 1] = '-'
                        newBoard[i][j] = '-'
                        moves.append(newBoard)
    return moves



### function to generate moves possible if current turn is player black
def generateBlackMoves(board):
    possibleMoves = []

    numRows = len(board)  # number of rows in board
    for i in range(numRows):
        rowLen = len(board[i])  # length of specific row in board
        for j in range(rowLen):
            if board[i][j] == 'b':  # if element is white player piece we generate possible moves for that piece
                possibleMoves.append(moveBlackPiece(board, (i, j)))

    return possibleMoves



### function that generates the possible moves for a black piece
def moveBlackPiece(board, coordinate):
    i = coordinate[0]  # i from matrix to index
    j = coordinate[1]  # j from matrix to index
    moves = []
    numRows = len(board)  # number of rows in board

    # check if there is a row above the current black piece
    if i > 0:
        if len(board[i]) > len(board[i - 1]):
            # check if top left is possible
            if j > 0:
                if board[i - 1][j - 1] == '-':  # check top left if empty
                    newBoard = copy.deepcopy(board)
                    newBoard[i][j] = '-'
                    newBoard[i - 1][j - 1] = 'b'
                    moves.append(newBoard)
                elif board[i - 1][j - 1] == 'w':    # if opposing white then see if skip over
                    if i - 1 > 0: # check top left
                        if len(board[i - 1]) > len(board[i - 2]) and j - 1 > 0:
                            if board[i - 2][j - 2] == '-':
                                newBoard = copy.deepcopy(board)
                                newBoard[i][j] = '-'
                                newBoard[i - 1][j - 1] = '-'
                                newBoard[i - 2][j - 2] = 'b'
                                moves.append(newBoard)
                        else:
                            if j != 0:
                                if board[i - 2][j - 1] == '-':
                                    newBoard = copy.deepcopy(board)
                                    newBoard[i][j] = '-'
                                    newBoard[i - 1][j - 1] = '-'
                                    newBoard[i - 2][j - 1] = 'b'
                                    moves.append(newBoard)


            # next check if top right is possible
            if j < len(board[i - 1]):
                if board[i - 1][j] == '-':  # if top right is empty
                    newBoard = copy.deepcopy(board)
                    newBoard[i][j] = '-'
                    newBoard[i - 1][j] = 'b'
                    moves.append(newBoard)
                elif board[i - 1][j] == 'w':    # if top right is a white piece
                    if i - 1 > 0:
                        if len(board[i - 1]) > len(board[i - 2]) and j < len(board[i - 2]):
                            if board[i - 2][j] == '-':  # check if space diagonal over white is available
                                newBoard = copy.deepcopy(board)
                                newBoard[i][j] = '-'
                                newBoard[i - 1][j] = '-'
                                newBoard[i - 2][j] = 'b'
                                moves.append(newBoard)
                        elif j < len(board[i - 2]):
                            if board[i - 2][j + 1] == '-':  # check if space diagonal over white is available
                                newBoard = copy.deepcopy(board)
                                newBoard[i][j] = '-'
                                newBoard[i - 1][j] = '-'
                                newBoard[i - 2][j + 1] = 'b'
                                moves.append(newBoard)
        else:
            if board[i - 1][j] == '-':  # check top left if empty
                newBoard = copy.deepcopy(board)
                newBoard[i][j] = '-'
                newBoard[i - 1][j] = 'b'
                moves.append(newBoard)
            elif board[i - 1][j] == 'w':  # if opposing white then see if skip over
                if i - 1 > 0:
                    if board[i - 2][j] == '-':
                        newBoard = copy.deepcopy(board)
                        newBoard[i][j] = '-'
                        newBoard[i - 1][j] = '-'
                        newBoard[i - 2][j] = 'b'
                        moves.append(newBoard)

            if board[i - 1][j + 1] == '-':  # if top right is empty
                newBoard = copy.deepcopy(board)
                newBoard[i][j] = '-'
                newBoard[i - 1][j + 1] = 'b'
                moves.append(newBoard)
            elif board[i - 1][j + 1] == 'w':  # if top right is a white piece
                if i - 1 > 0:
                    if board[i - 2][j + 2] == '-':  # check if space diagonal over white is available
                        newBoard = copy.deepcopy(board)
                        newBoard[i][j] = '-'
                        newBoard[i - 1][j + 1] = '-'
                        newBoard[i - 2][j + 2] = 'b'
                        moves.append(newBoard)

    return moves    # return possible moves for this black piece

'''
max1 = copy.deepcopy(isMax)    # make sure not to change original

    stateTree = []
    parentStates = []   #   list of parents to generate moves from
    levelList = []   # list of lists for each level in minimax tree,
    parentStates.append(board)      # starting state goes in first as the parent of tree

    if maxDepth == 0:
        return board
    
    # evaluate all moves possible till max depth
    for i in range(maxDepth):
        #print("loop iter: " + str(i))

        length = len(parentStates)
        for x in range(length):
            b = parentStates[0]
            if max1:    # if it is whites turn
                for j in movegen(b, 'w'):   # generate all moves of white for this board
                    for n in j:
                        parentStates.append(n)
                        levelList.append(OskaBoard(n, b))   # append new board state as an object

            else:
                for j in movegen(b, 'b'):   # generate all possible moves for black
                    for n in j:
                        parentStates.append(n)  # add new moves to parents to check
                        levelList.append(OskaBoard(n, b))   # append new board state as an object

            parentStates.pop(0) # delete explored from parent states list

        l = copy.deepcopy(levelList)
        max1 = not max1   # give turn to next player
        stateTree.append(l)  # add the level to the state Tree
        levelList.clear()   # clear list for next parent state

    # now that we have all the possible states in a tree, we can select the outcomes by traversing the tree
    finalMoves = []
    max2 = copy.deepcopy(isMax)  # make sure not to change original
    for i in list(reversed(stateTree)):   # go from bottom up in state tree
        finalBoard = i[0]
        min = 0
        max = 0
        for j in i: # get board objects from bottom row to top row

            if len(finalMoves) == 0:    # if this is the bottom most element we can choose the best option
                if max2:
                    if max < j.score:
                        finalBoard = j
                else:
                    if min > j.score:
                        finalBoard = j
            else:
                if max < j.score:
                    finalBoard = j
                else:
                    if min > j.score:
                        finalBoard = j

        max2 = not max2
        finalMoves.append(finalBoard)

 
'''
