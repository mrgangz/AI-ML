### tilepuzzle.py
# MITUL GANGER

import sys
import copy
import ast

#helper function to find index of the empty tile
def findZeroIndex(tile):
    for i in range(3):
        for j in range(3):
            if tile[i][j] == 0:
                pos = (i, j)
                return pos


def tilepuzzle(start, goal):
    return statesearch([start], goal, [])

def statesearch(unexplored,goal,path):
    if unexplored == []:
        return []
    elif goal == head(unexplored):
        print(reverse(cons(goal, path)))
    else:
        if len(path) > 20:
            return statesearch([], goal, [])
        result = statesearch(generateNewStates(head(unexplored)), goal, cons(head(unexplored), path))
        if result != []:
            return result
        else:
            return statesearch(tail(unexplored), goal, path)


def generateNewUp(currState):
    newState = copy.deepcopy(currState)
    zeroIndex = findZeroIndex(newState)
    if zeroIndex[0] != 0:
        switch = newState[zeroIndex[0] - 1][zeroIndex[1]]
        newState[zeroIndex[0] - 1][zeroIndex[1]] = 0
        newState[zeroIndex[0]][zeroIndex[1]] = switch
        return newState
    else:
        return currState


def generateNewRight(currState):
    newState = copy.deepcopy(currState)
    zeroIndex = findZeroIndex(newState)
    if zeroIndex[1] != 2:
        switch = newState[zeroIndex[0]][zeroIndex[1] + 1]
        newState[zeroIndex[0]][zeroIndex[1] + 1] = 0
        newState[zeroIndex[0]][zeroIndex[1]] = switch
        return newState
    else:
        return currState

def generateNewDown(currState):
    newState = copy.deepcopy(currState)
    zeroIndex = findZeroIndex(currState)
    if zeroIndex[0] != 2:
        switch = newState[zeroIndex[0] + 1][zeroIndex[1]]
        newState[zeroIndex[0] + 1][zeroIndex[1]] = 0
        newState[zeroIndex[0]][zeroIndex[1]] = switch
        return newState
    else:
        return currState

def generateNewLeft(currState):
    newState = copy.deepcopy(currState)
    zeroIndex = findZeroIndex(currState)
    if zeroIndex[1] > 0:
        switch = newState[zeroIndex[0]][zeroIndex[1] - 1]
        newState[zeroIndex[0]][zeroIndex[1] - 1] = 0
        newState[zeroIndex[0]][zeroIndex[1]] = switch
        return newState
    else:
        return currState


def reverse(st):
    return st[::-1]
    
def head(lst):
    return lst[0]

def tail(lst):
    return lst[1:]

def take(n,lst):
    return lst[0:n]

def drop(n,lst):
    return lst[n:]

def cons(item,lst):
    return [item] + lst


def generateNewStates(currState):
    return [generateNewLeft(currState), generateNewDown(currState), generateNewRight(currState), generateNewUp(currState)]


#start = [[2,8,3],[1,4,0],[7,6,5]]
#goal = [[1,2,3],[8,0,4],[7,6,5]]

arg1 = sys.argv[1]
start = ast.literal_eval(arg1)

arg2 = sys.argv[2]
goal = ast.literal_eval(arg2)

tilepuzzle(start, goal)

