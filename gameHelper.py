from random import randint, shuffle
import time

level = [0, 1, 2, 3]

numberList = [i for i in range(1, 10)]

#return a new grid, size 9x9
def initGrid():
    grid = []
    for i in range(0, 9):
        grid.append([])
        for j in range(0, 9):
            grid[i].append(0)
    return grid

#print the board string
def getBoardString(matrix):
    boardString = ""
    for row in range(9):
        for col in range(9):
            boardString += str(matrix[row][col]) + " "
            if (col + 1) % 3 == 0 and (col+1) != 9:
                boardString += "| "
            if col == 8:
                boardString += "\n"
                if (row + 1) % 3 == 0 and (row+1) != 9:
                    boardString += "- - - - - - - - - - - \n"
    return boardString

#check if the grid is full of answer
def finishGenerating(matrix):
    for i in range(0, 9):
        for j in range(0, 9):
            if matrix[i][j] == 0:
                return False
    return True

#check if a 'num' can be placed in [row, col]
def isSafe(matrix, row, col, num):
    return not num in matrix[row] and not num in [matrix[i][col] for i in range(9)] and not num in [matrix[row - row%3 + i][col - col%3 + j] for i in range(3) for j in range(3)]


def solver(matrix):
    global counter #counter for the number of solutions
    for row in range(0, 9):
        for col in range(0, 9):
            if matrix[row][col] == 0:
                for num in range(1, 10):
                    if isSafe(matrix, row, col, num):
                        matrix[row][col] = num
                        if finishGenerating(matrix):
                            counter += 1
                            break
                        else:
                            if solver(matrix):
                                return True
                        matrix[row][col] = 0
                return False
    return False

#generate a new puzzle:
def generateSudokuBoard(matrix):
    for row in range(0, 9):
        for col in range(0, 9):
            if matrix[row][col] == 0:
                shuffle(numberList)
                for number in numberList:
                    if isSafe(matrix, row, col, number):
                        matrix[row][col] = number
                        if finishGenerating(matrix):
                            return True
                        else:
                            if generateSudokuBoard(matrix):
                                return True
                        matrix[row][col] = 0
                return False
    return False

def createPuzzle(matrix, difficulty):
    global counter
    global attempts
    if difficulty == level[0]:
        attempts = 2
    elif difficulty == level[1]:
        attempts = 3
    elif difficulty == level[2]:
        attempts = 4
    elif difficulty == level[3]:
        attempts = 5

    while attempts > 0:
        row = randint(0, 8)
        col = randint(0, 8)
        while (matrix[row][col] == 0):
            row = randint(0, 8)
            col = randint(0, 8)
        backup = matrix[row][col]
        matrix[row][col] = 0

        copyGrid = []
        for r in range(0, 9):
            copyGrid.append([])
            for c in range(0, 9):
                copyGrid[r].append(matrix[r][c])

        counter = 0
        solver(copyGrid)

        if counter != 1:
            matrix[row][col] = backup
            attempts -= 1
    
def getEditableCells(matrix):
    editableCells = []
    for row in range(0, 9):
        for col in range(0, 9):
            if matrix[row][col] == 0:
                editableCells.append((row, col))
    return editableCells

#check unique value in row, col, and 3x3 grid

def checkRowValue(matrix, row, value):
    collision = []
    for i in range(0, 9):
        if matrix[row][i] == value:
            collision.append((row,i))
    if len(collision) > 1:
        return collision
    else:
        return [] 

def checkColValue(matrix, col, value):
    collision = []
    for i in range(0, 9):
        if matrix[i][col] == value:
            collision.append((i,col))
    if len(collision) > 1:
        return collision
    else:
        return []

def check3x3Value(matrix, row, col, value):
    collision = []
    for i in range(row - row % 3, row - row % 3 + 3):
        for j in range(col - col % 3, col - col % 3 + 3):
            if matrix[i][j] == value:
                collision.append((i,j))
    if len(collision) > 1:
        return collision
    else:
        return []

def getAllCollision(matrix):
    collision = set()
    for val in range(1, 10):
        for i in range(0, 9):
            rowCollision = checkRowValue(matrix, i, val)
            colCollision = checkColValue(matrix, i, val)
            collision = collision.union(collision, set(rowCollision + colCollision))
        rows = [0, 3, 6]
        cols = [0, 3, 6]
        for row in rows:
            for col in cols:
                boxCollision = check3x3Value(matrix, row, col, val)
                collision = collision.union(collision, set(boxCollision))
    if len(collision) > 0:
        return collision
    else:
        return []