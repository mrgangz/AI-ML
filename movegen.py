### COPYRIGHT MITUL @ 2020 MAY 12###

import sys
import copy


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

    print("]")  # creates 2 new lines after finishing



### function that takes the board and current player and generates new moves
def movegen(rows, player):
    length = len(rows)  # get length of list so we can seperate strings into 2x2 matrix
    board = makeBoard(rows)


    possibleMoves = []  # empty array to store possible moves in
    if player == 'w':
        possibleMoves = generateWhiteMoves(board)
    elif player == 'b':
        possibleMoves = generateBlackMoves(board)
    else:
        print("invalid player selection try again")
        return -1

    for i in possibleMoves: # print board in specified format
        for j in i:
            printBoard(j)



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
                        if len(board[i - 1]) > len(board[i - 2]):
                            if board[i - 2][j] == '-':  # check if space diagonal over white is available
                                newBoard = copy.deepcopy(board)
                                newBoard[i][j] = '-'
                                newBoard[i - 1][j] = '-'
                                newBoard[i - 2][j] = 'b'
                                moves.append(newBoard)
                        else:
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

#movegen(sys.argv[1], sys.argv[2])