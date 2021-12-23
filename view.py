import pygame
import time
import model, constants
import os

class Button(object):
    def __init__(self, image, position, size, value):
        self.image = image
        self.rect = pygame.Rect(position, size)
        self.value = value

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def printValue(self):
        print(self.value)

    def eventHandler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return self.value

class Buttons:
    def __init__(self):
        buttonValue = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "erase", "hint", "note", "undo","newGame"] 
        self.buttonHolder = []
        #numberButton
        buttonX = 510
        buttonY = 250
        buttonSize = (70, 70)
        for i in range(1, 10):
            img = pygame.image.load(os.path.join("resource", buttonValue[i-1] + ".png"))
            img = pygame.transform.scale(img, buttonSize)
            self.buttonHolder.append(Button(img, (buttonX, buttonY), buttonSize, buttonValue[i-1]))
            buttonX += 100
            if i % 3 == 0:
                buttonX = 510
                buttonY += 80
        buttonSize = (55, 55)
        #functionButton
        buttonX = 510
        buttonY = 150
        for i in range(10, 14):
            img = pygame.image.load(os.path.join("resource", buttonValue[i-1] + ".png"))
            img = pygame.transform.scale(img, buttonSize)
            self.buttonHolder.append(Button(img, (buttonX, buttonY), buttonSize, buttonValue[i-1]))
            buttonX += 70
        #newGameButton
        buttonSize = (260, 65)
        img = pygame.image.load(os.path.join("resource", buttonValue[-1] + ".png"))
        img = pygame.transform.scale(img, buttonSize)
        self.buttonHolder.append(Button(img, (515, 75), buttonSize, buttonValue[-1]))

    def display(self, screen):
        for i in range(len(self.buttonHolder)):
            self.buttonHolder[i].draw(screen)

        label1 = pygame.font.SysFont('roboto', 15).render('Erase', True, constants.darkBlue)
        screen.blit(label1, (520, 210))
        label2 = pygame.font.SysFont('roboto', 15).render('Hint', True, constants.darkBlue)
        screen.blit(label2, (590, 210))
        label3 = pygame.font.SysFont('roboto', 15).render('Notes', True, constants.darkBlue)
        screen.blit(label3, (660, 210))
        label4 = pygame.font.SysFont('roboto', 15).render('Undo', True, constants.darkBlue)
        screen.blit(label4, (725, 210))

    def eventHandler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(self.buttonHolder)):
                if self.buttonHolder[i].rect.collidepoint(event.pos):
                    print(self.buttonHolder[i].value)
                    return self.buttonHolder[i].value
        else:
            return None

class Board:
    def __init__(self, window, difficulty, board):
        self.window = window
        self.board = board
        self.difficulty = difficulty
        self.tiles = []
        self.currentCell = (None, None)
        
        # self.tiles = [[Tile(window, constants.startX+i*constants.cellSize, startY+j*constants.cellSize, self.board[i][j]) for i in range(9)] for j in range(9)]
        for i in range(9):
            self.tiles.append([])
            for j in range(9):
                self.tiles[i].append(Tile(window, constants.startX+j*constants.cellSize, constants.startY+i*constants.cellSize, self.board[i][j]))
                if self.board[i][j] == 0:
                    self.tiles[i][j].textColor = constants.darkBlue
                self.tiles[i][j].setID((i, j))
                
    def setEditableCells(self, editableCells):
        self.editableCells = editableCells
    
    def isEditable(self, x, y):
        if (x, y) in self.editableCells:
            return True
        else:
            return False

    def drawBoard(self):
        for i in range(9):
            for j in range(9):
                self.tiles[i][j].draw(1)
                if self.board[i][j] != 0:
                    self.tiles[i][j].display(self.board[i][j], (constants.startX+j*constants.cellSize+15, constants.startY+i*constants.cellSize+6))
        pygame.draw.line(self.window, constants.black, (constants.startX, constants.startY), (constants.startX+9*constants.cellSize, constants.startY), 3)
        pygame.draw.line(self.window, constants.black, (constants.startX, constants.startY+9*constants.cellSize), (constants.startX+9*constants.cellSize, constants.startY+9*constants.cellSize), 3)
        for i in range(9):
            for j in range(9):
                #horizontal lines
                if i % 3 == 0 and i != 0:
                    pygame.draw.line(self.window, constants.black, (constants.startX, constants.startY+i*constants.cellSize), (constants.startX+9*constants.cellSize, constants.startY+i*constants.cellSize), 3)
                #vertical lines
                if j % 3 == 0 and j != 0:
                    pygame.draw.line(self.window, constants.black, (constants.startX+j*constants.cellSize, constants.startY), (constants.startX+j*constants.cellSize, constants.startY+9*constants.cellSize), 3)
                
        pygame.draw.line(self.window, constants.black, (constants.startX, constants.startY), (constants.startX, constants.startY+9*constants.cellSize), 3)
        pygame.draw.line(self.window, constants.black, (constants.startX+9*constants.cellSize, constants.startY), (constants.startX+9*constants.cellSize, constants.startY+9*constants.cellSize), 3)
        self.textLabel(self.difficulty, 50, 20, constants.black) #difficulty
        self.textLabel("01:34", 700, 20, constants.black) #timer

    def changeState(self, clickedTile):
        for i in range(9):
            for j in range(9):
                if self.tiles[i][j] != clickedTile:
                    self.tiles[i][j].selected = False
                else:
                    self.tiles[i][j].selected = True
                    currentVal = self.tiles[i][j].value
                    for tmpI in range(9):
                        for tmpJ in range(9):
                            if currentVal != 0 and (tmpI, tmpJ) != (i, j):
                                if currentVal == self.tiles[tmpI][tmpJ].value:
                                    self.tiles[tmpI][tmpJ].sameValue = True
                                else: 
                                    self.tiles[tmpI][tmpJ].sameValue = False
                            elif currentVal == 0:
                                self.tiles[tmpI][tmpJ].sameValue = False
                            if ((i // 3 == tmpI//3 and j//3 == tmpJ//3) or (i == tmpI) or (j == tmpJ)) and (tmpI, tmpJ) != (i, j):
                                self.tiles[tmpI][tmpJ].sameRowColBox = True
                            else:
                                self.tiles[tmpI][tmpJ].sameRowColBox = False

        # self.getState()

    def findViolated(self):
        for i in range(1, 10):
            for row in range(0, 9):
                pass


    def getState(self):
        for i in range(9):
            for j in range(9):
                if self.tiles[i][j].sameRowColBox:
                    print(1, end = " ")
                else: 
                    print(0, end = " ")
            print()
    
    def messageAnnouncer(self, event):
        mousePos = pygame.mouse.get_pos()
        for j in range(9):
            for i in range(9):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.tiles[i][j].rect.collidepoint(mousePos):
                        self.changeState(self.tiles[i][j])
                        self.currentCell = (i, j)
        return self.currentCell
    
    def getCurrentState(self):
        print(self.board)

    def textLabel(self, text, x, y, color):
        label = pygame.font.SysFont('roboto bold', 25).render(text, True, color)
        self.window.blit(label, (x, y))

    def redraw(self, updatedBoard):
        self.board = updatedBoard
        for i in range(9):
            for j in range(9):
                self.tiles[i][j].renewAttribute(self.isEditable(i, j))
        self.drawBoard()
        
        

class Tile: 
    def __init__(self, window, x, y, value):
        self.value = value
        self.window = window 
        self.rect = pygame.Rect(x, y, constants.cellSize, constants.cellSize)
        self.selected = False
        self.correct = False
        self.violated = False
        self.sameValue = False
        self.sameRowColBox = False
        self.id = (None, None)
        self.textColor = constants.black
        self.bgColor = constants.white
        
    def draw(self, thickness):
        pygame.draw.rect(self.window, self.bgColor, self.rect)
        pygame.draw.rect(self.window, constants.black, self.rect, thickness)

    def display(self, value, position):
        '''Displays a number on that tile'''
        font = pygame.font.SysFont('roboto', 35)
        text = font.render(str(value), True, self.textColor)
        self.window.blit(text, position)

    def clicked(self, mousePos):
        '''Checks if a tile has been clicked'''
        if self.rect.collidepoint(mousePos): #checks if a point is inside a rect
            self.selected = True
        return self.selected
    
    def setID(self, id):
        self.id = id
    
    def getID(self):
        return self.id

    def renewAttribute(self, editable):
        # if self.selected == True:
        #     self.textColor = constants.darkBlue
        # else:
        #     if self.violated
        if editable:
            self.textColor = constants.darkBlue
        else:
            self.textColor = constants.black
        self.bgColor = constants.white
        if self.selected == True:
            self.textColor = constants.lightBlue
            self.bgColor = constants.darkBlue
        if self.sameRowColBox == True:
            self.bgColor = constants.lightWhite
        if self.sameValue == True:
            self.bgColor = constants.lightBlue    
        if self.violated == True:
            self.bgColor = constants.red