from gameHelper import *
import copy
import os
import pickle   

class Board:
    def __init__(self, difficulty):
        #create a temp board
        grid = initGrid()
        #make a new sudoku board
        generateSudokuBoard(grid)
        #make a solved board
        self.solvedBoard = copy.deepcopy(grid)
        self.difficulty = difficulty
        #make a unsolved board
        createPuzzle(grid, difficulty)
        self.unsolvedBoard = copy.deepcopy(grid)
        #get editable cells from unsolved board
        self.editableCells = getEditableCells(self.unsolvedBoard)
        #initiate for the undo stack
        self.undoStack = []
        del grid
    
    #private functions
    def __isEditable(self, cell):
        if cell in self.editableCells:
            return True
        else:
            return False

    #public functions
    def isSolved(self):
        return self.unsolvedBoard == self.solvedBoard

    def getCurrentBoard(self):
        return self.unsolvedBoard
    
    def getEditableCells(self):
        return self.editableCells
    
    def makeAMove(self, x, y, value):
        cell = (x, y)
        #receive a cell in form of (x, y) and the value want to edit
        if self.__isEditable(cell):
            #add the move to the undo stack
            self.undoStack.append((cell, self.unsolvedBoard[cell[0]][cell[1]]))
            #edit the board
            self.unsolvedBoard[cell[0]][cell[1]] = value
            return True
        return False
    
    def deleteAMove(self, x, y):
        cell = (x, y)
        if self.__isEditable(cell):
            #add the move to the undo stack
            self.undoStack.append((cell, self.unsolvedBoard[cell[0]][cell[1]]))
            #edit the board
            self.unsolvedBoard[cell[0]][cell[1]] = 0
            return True
        return False
    
    def undoAMove(self):
        if len(self.undoStack) > 0:
            cell, value = self.undoStack.pop()
            self.unsolvedBoard[cell[0]][cell[1]] = value
            return True
        return False
    
    def hint(self, x, y):
        cell = (x, y)
        if self.__isEditable(cell):
            self.unsolvedBoard[cell[0]][cell[1]] = self.solvedBoard[cell[0]][cell[1]]
            self.editableCells.remove(cell)
            return True
        return False

    def solve(self):
        self.unsolvedBoard = copy.deepcopy(self.solvedBoard)
        return True
    
    def getTile(self, i, j):
        return self.unsolvedBoard[i][j]
    
    def checkEditable(self, x, y):
        if (x, y) in self.editableCells:
            return True
        else:
            return False

def saveCurrentGame(board):
    #save the current game
    with open('currentGame.pickle', 'wb') as f:
        pickle.dump(board, f)

def loadSavedGame():
    #load the saved game
    with open('currentGame.pickle', 'rb') as f:
        return pickle.load(f)

def init():
    try:
        board = loadSavedGame()
    except:
        board = Board(0)

    return board