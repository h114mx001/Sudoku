import model, view, constants
import pygame
import os
import tkinter as tk

#sudoku GUI
pygame.init()

mainWindow = pygame.display.set_mode((800, 560))
mainWindow.fill((255, 255, 255))
board = model.init()
difficulty = board.difficulty
newBoard = view.Board(mainWindow, constants.difficulties[difficulty], board.getCurrentBoard())
newBoard.setEditableCells(board.getEditableCells())

class Button(object):
    def __init__(self, image, position, size, callback = None):
        self.image = image
        self.rect = pygame.Rect(position, size)
        self.callback = callback
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def eventHandler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.callback:
                    self.callback()
    
pause = False
gameFinished = False

def pausing():
    global pause
    img = pygame.image.load(os.path.join("resource", "resume.png"))
    img = pygame.transform.scale(img, (300, 100))
    button = Button(img, (270, 220), (300, 100), unpause)
    while pause:
        mainWindow.fill(constants.white)
        button.draw(mainWindow)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            button.eventHandler(event)      

def unpause():
    global pause
    pause = False

def newGame():
    global board, newBoard
    def generateNewGame(difficulty):
        global board, newBoard
        gameFinished = True
        board = model.Board(difficulty)
        # newBoard.setEditableCells(board.getEditableCells())
        # newBoard.drawBoard()
        difficulty = board.difficulty
        newBoard = view.Board(mainWindow, constants.difficulties[difficulty], board.getCurrentBoard())
        newBoard.setEditableCells(board.getEditableCells())
        print(board.getCurrentBoard())
        root.destroy()
        return

    root = tk.Tk()
    root.geometry("300x200")
    label = tk.Label(root, text="Choose difficulty:")
    btnEasy = tk.Button(root, text = "Easy", command = lambda: generateNewGame(0))
    btnMedium = tk.Button(root, text = "Medium", command = lambda: generateNewGame(1))
    btnHard = tk.Button(root, text = "Hard", command = lambda: generateNewGame(2))
    btnExpert = tk.Button(root, text = "Expert", command = lambda: generateNewGame(3))
    btnFrame = tk.Frame(root)

    label.grid(row = 0, column = 0, sticky=tk.W+tk.E)
    btnEasy.grid(row = 1, column = 0, sticky=tk.W+tk.E)
    btnMedium.grid(row = 2, column = 0, sticky=tk.W+tk.E)
    btnHard.grid(row = 3, column = 0, sticky=tk.W+tk.E)
    btnExpert.grid(row = 4, column = 0, sticky=tk.W+tk.E)
    root.mainloop()


def commandReceiver(buttonMessage, indexMessage):
    if indexMessage != (None, None) and buttonMessage != None:
        if buttonMessage in "123456789":
            board.makeAMove(indexMessage[0], indexMessage[1], int(buttonMessage))
            newBoard.board[indexMessage[0]][indexMessage[1]] = int(buttonMessage)
            newBoard.tiles[indexMessage[0]][indexMessage[1]].value = int(buttonMessage)

        if buttonMessage == "erase":
            board.deleteAMove(indexMessage[0], indexMessage[1])
            newBoard.board[indexMessage[0]][indexMessage[1]] = 0
            newBoard.tiles[indexMessage[0]][indexMessage[1]].value = 0 
            
        if buttonMessage == "hint":
            board.hint(indexMessage[0], indexMessage[1])
            newBoard.setEditableCells(board.getEditableCells())

    if buttonMessage == "undo":
        board.undoAMove()

    if buttonMessage == "newGame":
        newGame()

def main():
    global pause
    clock = pygame.time.Clock()
    startTime = pygame.time.get_ticks()
    isExited = False

    pygame.display.set_caption("Sudoku Classic")
    
    buttons = view.Buttons()
    pauseImg = pygame.image.load(os.path.join("resource", "pause.png"))
    pauseImg = pygame.transform.scale(pauseImg, (25, 25))
    pauseButton = Button(pauseImg, (750, 15), (25, 25), pausing)

    # number1 = numberButton(mainWindow, 1)
    newBoard.drawBoard()
    while gameFinished == False:
        mainWindow.fill(constants.white)
        buttons.display(mainWindow)
        pauseButton.draw(mainWindow)
        for event in pygame.event.get():
  
            if event.type == pygame.QUIT:
                model.saveCurrentGame(board)
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if pauseButton.rect.collidepoint(mouse):
                    pause = True
                    pausing()

            buttonCmd = buttons.eventHandler(event)
            currentCell = newBoard.messageAnnouncer(event)
            if buttonCmd != None:
                currentCell = newBoard.messageAnnouncer(event)
                print(buttonCmd, currentCell)
                commandReceiver(buttonCmd, currentCell)

        newBoard.redraw(board.getCurrentBoard())
        pygame.display.update()
    
main()