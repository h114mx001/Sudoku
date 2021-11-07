from random import randint, shuffle

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

def checkBlock(block):
    return set(block) == set(range(1, 10))

def checkRow(matrix, row):
    return checkBlock(matrix[row])

def checkCol(matrix, col):
    return checkBlock([matrix[row][col] for row in range(9)])

def checkBox3x3(matrix, row, col):
    return checkBlock([matrix[row + i][col + j] for i in range(3) for j in range(3)])

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
                            return True
                        else:
                            if solver(matrix):
                                return True
                return False
    return False

def createPuzzle(matrix, difficulty):
    global counter
    global attempts 
    if difficulty == "easy":
        attempts = 2
    elif difficulty == "medium":
        attempts = 3
    elif difficulty == "hard":
        attempts = 4
    elif difficulty == "expert":
        attempts = 5
    counter = 1

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

def testCode():
    grid = initGrid()
    generateSudokuBoard(grid)
    print(getBoardString(grid))
    createPuzzle(grid, "expert")


if __name__ == "__main__":
    testCode()