import copy

from gameHelper import *

# grid = initGrid()
# generateSudokuBoard(grid)
# solvedBoard = copy.deepcopy(grid)
# print(getBoardString(solvedBoard))
# createPuzzle(grid, "easy")
# unsolvedBoard = copy.deepcopy(grid)
# del grid
# print(getBoardString(unsolvedBoard))

class SudokuBoard:

    def __init__(self, difficulty):
        grid = initGrid()
        generateSudokuBoard(grid)
        self.solvedBoard = copy.deepcopy(grid)
        createPuzzle(grid, difficulty)
        self.unsolvedBoard = copy.deepcopy(grid)
        del grid
    
    def getBoardString(self, board):
        return getBoardString(board)

class SudokuGame:

    def __init__(self, difficulty):
        mainGame = SudokuBoard(difficulty)

class HandleGame:

    def __init__(self):
        self.gameStarted = False
        self.gameIsFinished = False

    def startGame(self):
        welcomeMessage = '''Welcome to Terminal 9x9 Sudoku!\nPress 'start' to start the game. Press 'help' to see the commands. GLHF!'''
        print(welcomeMessage)
        self.commandLine()
    
    def gameLoop(self):
        while True and not self.gameIsFinished:
            self.commandLine()

    def help(self):
        helpMessage = '''Commands:
    + new - starts new game
    + help - shows this message
    + exit - exits the game
        '''
        print(helpMessage)

    def newGame(self):
        self.difficulty = input("Choose difficulty: easy, medium, hard, or expert: ")
        if self.difficulty not in ["easy", "medium", "hard", "expert"]:
            print("Invalid difficulty. Please try again.")
            self.newGame()
        else:
            if self.difficulty == "easy":
                self.board = SudokuBoard("easy")
            elif self.difficulty == "medium":
                self.board = SudokuBoard("medium")
            elif self.difficulty == "hard":
                self.board = SudokuBoard("hard")
            elif self.difficulty == "expert":
                self.board = SudokuBoard("expert")
            self.gameStarted = True
            print("Game created successfully! Enjoy!") 
            print(getBoardString(self.board.unsolvedBoard))
            self.gameLoop()
    
    def commandLine(self):
        command = input(">> ")
        command = command.split()
        if command[0] == "help":
            self.help()
        if command[0] == "new":
            self.newGame()
        else:
            print("Invalid command!")
            self.commandLine()
    
if __name__ == "__main__":
    game = HandleGame()
    game.startGame()

