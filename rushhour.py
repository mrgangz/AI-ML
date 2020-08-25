# COPYRIGHT Mitul Ganger @2020

import sys
import copy

select = sys.argv[1]    # either 0 or 1 for heuristic value
length = len(sys.argv[2])   # get length of list so we can seperate strings into 2x2 matrix
arg = sys.argv[2][1:length - 1]
rows = arg.split(',')    # list of strings

### function to make the strings list into a 2d matrix
def makeGrid(rows):
    newGrid = [[0] * 6 for i in range(6)]
    for i in range(6):
        for j in range(6):
            newGrid[i][j] = rows[i][j]
    return newGrid


grid = makeGrid(rows)   # make the string list into a 2d matrix with all chars


### Class to make listing out cars in the grid easier
class Car :
    def __init__(self, letter, startPosition, orientation, length, endPosition):
        self.letter = letter
        self.startPosition = startPosition
        self.orientation = orientation  # 'h' for horizontal, 'v' for vertical
        self.length = length
        self.endPosition = endPosition
    # function for debugging
    def printCar(self):
        print("Car Letter: " + self.letter + "\nsP: {0}".format(self.startPosition) + "\norien: " + self.orientation
              + "\nlen: " + str(self.length) + "\neP: {0}\n".format(self.endPosition))



### function to get the list of cars in object form
def getCars(grid):
    carsArray = []  # array to record the car objects
    discovered = []  # array to make sure car isn't counted twice

    # go through entire 6x6 grid from top left
    for i in range(6):
        for j in range(6):
            # if the element is a letter
            if grid[i][j] != '-':
                # if statement to check if right element is the same letter. if it is then
                # we know that the car is horizontal and we will log it
                if j < 5:
                    # make sure that the element horizontal and not a different letter
                    if grid[i][j] == grid[i][j + 1] :
                        l = 0   # length for car obj
                        letter = grid[i][j]     # letter of car on grid
                        startPosition = (i, j)
                        while j < 6:
                            if grid[i][j] != letter:
                                break
                            else:
                                l = l + 1   # add to length of car
                                j = j + 1   # iterate again one more to the right
                        car = Car(letter, startPosition, 'h', l, (i, j - 1))   # create car object
                        j = j - 1
                        carsArray.append(car)       # append car to the final list

                if i < 5:
                    # make sure the element is vertical and is not already stored in the list
                    if grid[i][j] == grid[i + 1][j] and discovered.count(grid[i][j]) == 0 and grid[i][j] != '-':
                        l = 0
                        startPosition = (i, j)
                        letter = grid[i][j]  # letter of car on grid
                        x = i
                        # go down rows until out of bounds or car stops
                        while x < 6:
                            if grid[x][j] != letter:
                                break
                            else:
                                l = l + 1
                                x = x + 1
                        car = Car(letter, startPosition, 'v', l, (x - 1, j) )
                        carsArray.append(car)  # append car to the final list
                        discovered.append(letter)   # add letter to discovered list

    return carsArray

def printBoard(grid):
    for i in range(6):
        for j in range(6):
            print(str(grid[i][j]), end="")
        print("")
    print("\n")

### function to see if said grid is the solution to the problem
def isSolution(grid):
    # see if the X car made it to the end
    if grid[2][5] == 'X':
        return True
    else:
        return False


### Heuristic to see how many spaces to the right of XX are blocked
def blockHeuristic(grid):
    # if done, return 0
    if isSolution(grid):
        return 0

    row = grid[2]   # access row 3 where XX is
    x = 1
    for i in range(6):
        if row[5 - i] == "X":
            break
        elif row[5 - i] != '-':
            x = x + 1
    return x    # return the heuristic block number


### custom heuristic that sees which state has best path free of cars
def customHeuristic(grid):
    # if done, return 0
    if isSolution(grid):
        return 0

    row = grid[2]  # access row 3 where XX is
    x = 1
    for i in range(6):
        if row[5 - i] == "X":
            break
        elif row[5 - i] == '-':
            x = x + 1
        # heigher weight for cars blocking the path than empty
        else:
            x = x + 3
    return x  # return the heuristic block number


### function to move car up and return new grid
def moveUp(car, grid):
    if grid[car.startPosition[0] - 1][car.startPosition[1]] == '-':
        newGrid = copy.deepcopy(grid)
        newGrid[car.startPosition[0] - 1][car.startPosition[1]] = car.letter
        newGrid[car.endPosition[0]][car.endPosition[1]] = '-'
        return newGrid
    else:
        return []

### function to move car down and return new grid
def moveDown(car, grid):
    newGrid = copy.deepcopy(grid)
    if grid[car.endPosition[0] + 1][car.endPosition[1]] == '-':
        newGrid[car.endPosition[0] + 1][car.endPosition[1]] = car.letter
        newGrid[car.startPosition[0]][car.startPosition[1]] = '-'
        return newGrid
    else:
        return []

### function to move car right and return new grid
def moveRight(car, grid):
    newGrid = copy.deepcopy(grid)
    if grid[car.endPosition[0]][car.endPosition[1] + 1] == '-':
        newGrid[car.endPosition[0]][car.endPosition[1] + 1] = car.letter
        newGrid[car.startPosition[0]][car.startPosition[1]] = '-'
        return newGrid
    else:
        return []

### function to move car left and return new grid
def moveLeft(car, grid):
    newGrid = copy.deepcopy(grid)
    if grid[car.startPosition[0]][car.startPosition[1] - 1] == '-':
        newGrid[car.startPosition[0]][car.startPosition[1] - 1] = car.letter
        newGrid[car.endPosition[0]][car.endPosition[1]] = '-'
        return newGrid
    else:
        return []


### function to get horizontal moves for
def generateVertMoves(car, grid):
    moves = []  # array to store the different vertical moves possible for this car

    # see if space to move up
    if car.startPosition[0] > 0:
        moves.append(moveUp(car, grid))
    # see if space to move down
    if car.endPosition[0] < 5:
        moves.append(moveDown(car, grid))

    return moves    # return the possible vertical moves for this car


### function to get horizontal moves for a horiz car
def generateHorizMoves(car, grid):
    moves = []  # array to store different horizontal moves possible for this car

    # see if space to move left
    if car.startPosition[1] > 0:
        moves.append(moveLeft(car, grid))
    # see if space to move right
    if car.endPosition[1] < 5:
        moves.append(moveRight(car, grid))

    return moves    # return possible moves


### function that calls appropriate generating new move states
def getCarStates(carObj, grid):
    if carObj.orientation == 'v':
        return generateVertMoves(carObj, grid)
    elif carObj.orientation == 'h':
        return generateHorizMoves(carObj, grid)
    else:
        return


### Function that generates all possible moves of all cars
def generateStates(grid):
    carList = getCars(grid) # function to get the list of car objects
    states = []         # generate all states into list
    finalstates = []    # seperate into a list of all future states

    for x in carList:
        states.append(getCarStates(x, grid))
    for i in states:
        for j in i:
            finalstates.append(j)   # final states contains all possible car moves now
            #printBoard(j)

    return finalstates


### class to keep track of all nodes and their parents/path length
class Board :
    # initiate state in board
    def __init__(self, board, parent=None):
        self.parent = parent
        self.pathLength = 0     # distance from start
        self.board = board
        self.f = 0



### function that runs A* algorithm
def aStar(grid):

    # set start node as current board
    startNode = Board(grid)
    startNode.f = startNode.pathLength = 0

    open = [startNode]                  # list for all nodes that need to be processed starting with first node
    checked = []                           # nodes that have had their successors generated

    statesExplored = 0          # keep track of the states we process

    # while loop to keep going until all nodes explored
    # i have a bug in here and have not been able to fix it
    while len(open) > 0:

        cur_node = open[0]
        index = 0
        # find node with smallest f
        for n in open:
            if n.f < cur_node.f:
                cur_node = n
                index = open.index(n)

        open.pop(index)
        checked.append(cur_node)

        ### check if we raeched a solution with the current node
        if isSolution(cur_node.board):
            path = []
            pl = cur_node.pathLength
            while cur_node.parent != None:
                path.append(cur_node.board)
                cur_node = cur_node.parent
            path.reverse()      # reverse the path up from children to parents
            for i in path:
                printBoard(i)
            print("number of moves: " + str(pl))
            print(" states explored: " + str(statesExplored))
            break

        newStates = generateStates(cur_node.board)  # keep children here
        for state in newStates:
            if state:

                newB = Board(state)     # make neww obj
                newB.parent = cur_node
                newB.pathLength = cur_node.pathLength + 1
                if select == 0:
                    newB.f = newB.pathLength + blockHeuristic(newB.board)   # calculate the f value
                else:
                    newB.f = newB.pathLength + customHeuristic(newB.board)   # calculate the f value

                for o in open:
                    if o == newB:
                        continue

                for seen in checked:
                    if seen.board == state:
                        continue

                open.append(newB)

        statesExplored = statesExplored + 1


aStar(grid)     # call a star function on input grid

