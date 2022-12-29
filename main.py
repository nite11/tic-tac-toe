## took this code from
## http://programarcadegames.com/index.php?lang=en&chapter=array_backed_grids
## as a starting point to build the tic-tac-toe game
import copy
import pygame
import random
from pygame import mixer
import tkinter

top = tkinter.Tk()
top.geometry("300x300")
playerMode='vAI'

def vsHuman():
    global playerMode
    playerMode='vHuman'
    top.destroy()
Human = tkinter.Button(top, text ="vs Human", command = vsHuman)

def vsAI():
    top.destroy()
AI = tkinter.Button(top, text ="vs AI", command = vsAI)

def vsRandAI():
    global playerMode
    playerMode = 'vRandAI'
    top.destroy()
RandAI = tkinter.Button(top, text ="vs Random AI", command = vsRandAI)

Human.pack()
AI.pack()
RandAI.pack()
top.mainloop()
#print(playerMode)

# initializing pygame
pygame.init()

font = pygame.font.Font('freesansbold.ttf', 50)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


X = font.render("X", True, BLACK) #to paste an X
O = font.render("O", True, BLACK)  #to paste an O
restart = font.render("Restart", True, BLACK)  #font of the Restart button


# took some help from this code from
# https://stackoverflow.com/questions/33963361/how-to-make-a-grid-in-pygame

BOARD_SIZE = 300
blockSize = int(BOARD_SIZE/3) #Set the size of the grid block

player=''  #to determine whether it's player1's turn or 2's

grid = []   # Create a grid of numbers to represent the board and selections:
            # 0 for empty, 1 for player 1, 2 for player 2
origGrid = []
tempGrid = []
tempGrid2 = []
running = ''  #to keep the while loop running while there are events
spotsLeft = 9
linePos = 0 #variable to determine the winning line
            # out of the 8 possible lines (3 horizontal, 3 vertical and 2 diagonal
SCREEN = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE+50)) #EXTRA 50 FOR THE RESTART BUTTON

def main():  #Controller part of the MVC
    global SCREEN, player, running, spotsLeft
    while running != 'False':
        for event in pygame.event.get():   #collect all the events
            if event.type == pygame.QUIT:  #to handle closing of the application
                running = 'False'
                pygame.quit()
                #sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:    #to restart the game when 'r' is pressed
                    #top.mainloop()
                    gridInit()
                    main()
                    break       #break the original while loop
            elif event.type == pygame.MOUSEBUTTONDOWN and running != 'gameover':
                #running=gameover means that someone has won
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                #check whether restart button is clicked
                if pos[1] > 3*blockSize:
                    gridInit()
                    main()
                    break
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // blockSize  #quotient
                row = pos[1] // blockSize
                #print(row,column)
                gridUpdate(row, column)


            #nothing changes on the screen with further mouse clicks, if the game is over.
            #game can only be restarted or quitted
            elif event.type == pygame.MOUSEBUTTONDOWN and running == 'gameover':
                pos = pygame.mouse.get_pos()
                if pos[1] > 3 * blockSize:
                    gridInit()
                    main()
                    break

#updates the grid with 1's and 2's
def gridUpdate(row,column): #Model part of the MVC
    global player, spotsLeft, grid,origGrid,tempGrid,tempGrid2
    #print(row, column)

    if player == 'Player1' and grid[row][column] == 0:  # check whether the spot is empty
        # Set that location to 1
        grid[row][column] = 1
        #print(grid,player)
        spotsLeft-=1
        player = 'Player2'
        drawGrid()
        if playerMode=='vAI' and running != 'gameover' and spotsLeft!=0:
            origGrid = copy.deepcopy(grid)
            tempGrid = copy.deepcopy(grid)
            tempGrid2 = copy.deepcopy(grid)
            bestMove()   #this function finds the best possible move for the AI
        elif playerMode == 'vRandAI' and running != 'gameover' and spotsLeft!=0:
            randMove()    #this function finds a random empty square
    elif player == 'Player2' and grid[row][column] == 0:
        grid[row][column] = 2  # Set that location to 2
        #print(grid,player)
        spotsLeft-=1
        player = 'Player1'
        drawGrid()


#initialize the grid and the board
def gridInit():  #Initial setup of the View and Model (MVC)
    # Background Sound
    mixer.music.load('data/background.mp3')
    mixer.music.play(-1)
    global player, grid, running,spotsLeft,linePos
    linePos = 0
    spotsLeft = 9
    running = 'True'  #to keep the while loop running while there are events
    grid=[]
    player = 'Player1'
    SCREEN.fill(BLACK)  #black background
    for row in range(3):
        # For each row, create a list that will
        # represent an entire row
        grid.append([])
        # Loop for each column
        for column in range(3):
            # initialize with zeroes
            grid[row].append(0)
            #draw WHITE squares of length = blockSize-5.
            # it looks like the squares have a border of thickness 5 because of the black background
            rect = pygame.Rect(row * blockSize, column * blockSize, blockSize-5, blockSize-5)
            pygame.draw.rect(SCREEN, WHITE, rect)

    rect = pygame.Rect(5, blockSize * 3 + 5, blockSize * 3 - 5, blockSize - 5)  # create the restart button
    pygame.draw.rect(SCREEN, BLUE, rect)
    SCREEN.blit(restart, (5, blockSize * 3 + 5))  # display Restart as the button name

    pygame.display.set_caption(f'Your turn {player}')
    pygame.display.update()


#function to redraw the board based on the clicks
def drawGrid():  #View part of the MVC
    #change the color of the box depending on whether it is player 1 or 2
    for row in range(3):
        for column in range(3):
            color = WHITE
            if grid[row][column] == 1:
                color = RED
            elif grid[row][column] == 2:
                color = GREEN
            rect = pygame.Rect(column*blockSize, row*blockSize, blockSize-5, blockSize-5)
            pygame.draw.rect(SCREEN, color, rect)

    # mark the box with X or O depending on whether it is player 1 or 2
    for row in range(3):
        for column in range(3):
            if grid[row][column] == 1:
                SCREEN.blit(X, (column * blockSize + blockSize / 2, row * blockSize + blockSize / 2))
            elif grid[row][column] == 2:
                SCREEN.blit(O, (column * blockSize + blockSize / 2, row * blockSize + blockSize / 2))

    pygame.display.set_caption(f'Your turn {player}')
    pygame.display.update()
    gameOver() #check whether the game is over


def drawLine():
    global linePos
    if linePos<4 and linePos>0:
        pygame.draw.line(SCREEN, BLACK, (blockSize/2, (linePos-.5)*blockSize), (2.5*blockSize,(linePos-.5)*blockSize),5)
    elif linePos<7 and linePos>3:
        linePos=linePos-3
        pygame.draw.line(SCREEN, BLACK, ((linePos-.5)*blockSize, blockSize/2), ((linePos-.5)*blockSize, 2.5*blockSize),5)
    elif linePos == 7:
        pygame.draw.line(SCREEN, BLACK, (blockSize/2, blockSize/2), (2.5*blockSize, 2.5*blockSize),5)
    elif linePos == 8:
        pygame.draw.line(SCREEN, BLACK, (2.5*blockSize, blockSize/2), (blockSize/2, 2.5*blockSize),5)

def gameOver():
    global running
    if player == 'Player2':   #immediately after player1's turn player='Player2'
        if SumOfGrid(1) == 'Winner':  #will check whether player1 won after the last click,
                                    # by doing a sum of the 1's in the grid. 1 represents player 1
            running = 'gameover'
            pygame.display.set_caption(f'Player1 wins')
            drawLine()          #function to draw the line representing the winning combination
            pygame.display.update()
    else:
        if SumOfGrid(2) == 'Winner':
            running = 'gameover'
            pygame.display.set_caption(f'Player2 wins')
            drawLine()
            pygame.display.update()

    if running != 'gameover' and spotsLeft == 0: #to check that the spots got filled without a winner
        pygame.display.set_caption(f'Game Over. No winner.')
        pygame.display.update()

#will do a sum of the 1's or 2's in the grid along the rows, columns and diagonals
def SumOfGrid(i):
    global linePos
    colSum=0
    rowSum=0
    diagSum1=0
    diagSum2=0
    for row in range(3):
        rowSum = 0  #initialize each row's sum
        for column in range(3):
            if grid[row][column] == i: #adding 1's with 1's and 2's with 2's
                rowSum += grid[row][column]
        if rowSum == 3*i:  #winning sum=3 for player1 and 6 for player 2
            linePos = row+1   #linepos 1,2 or 3
            return 'Winner'

    for column in range(3):
        colSum = 0  #initialize each column's sum
        for row in range(3):
            if grid[row][column]==i:
                colSum+=grid[row][column]
        if colSum==3*i:
            linePos = column + 4 #linepos 4,5 or 6
            return 'Winner'

    for row in range(3):
        for column in range(3):
            if grid[row][column]==i and row==column:
                diagSum1+=grid[row][column]
    if diagSum1==3*i:
        linePos=7
        return 'Winner'

    for row in range(3):
        for column in range(3):
            if grid[row][column]==i and row+column==2:
                diagSum2+=grid[row][column]
    if diagSum2==3*i:
        linePos=8
        return 'Winner'


def randMove():
    tempGrid9 = copy.deepcopy(grid)
    randList=[]
    r=10
    for row in range(3):
        for column in range(3):
            if tempGrid9[row][column] == 0:
                tempGrid9[row][column]=r #inserts an integer greater than 9 where the grid is empty
                randList.append(r)       #appends this integer to a list
                r+=1

    r=random.choice(randList)          #one of the inserted integers is chosen at random
    for row in range(3):
        for column in range(3):
            if tempGrid9[row][column] == r:
                gridUpdate(row, column)     #the place of the chosen integer is marked by the AI

#took inspiration from the Minimax algorithm
#this AI will try to stop the human player from winning on the next turn
#need to add more layers/forward looking to make the AI unbeatable
def bestMove():  #find a move where player1 cannot win
    global grid,player,tempGrid,tempGrid2
    for row in range(3):
        for column in range(3):
            if tempGrid[row][column] == 0 and player == 'Player2':
                grid[row][column] = 2  # trying with this branch
                tempGrid[row][column] = 3  # to mark the trial
                player = 'Player1'
                tempGrid2 = copy.deepcopy(grid)
                r=row
                c=column

            elif grid[row][column] == 0 and player == 'Player1':
                grid[row][column] = 1  # trying with this sub-branch
                if SumOfGrid(1) == 'Winner': #check whether player1 can win in the next turn
                    player = 'Player2'
                    grid = copy.deepcopy(origGrid)
                    bestMove()          #to try with the next move for the AI
                    return          # to end the recursive call here, without doing anything further
                else:
                    grid[row][column] = 0 #reversing the sub-branch trial
            #print(row,column,grid,player)    #used for testing and debugging
    player = 'Player2'
    grid =copy.deepcopy(origGrid)  #reset the grid to the original grid before this function was called
    gridUpdate(r,c)   #update the grid with the move decided by this function


gridInit()
main()

