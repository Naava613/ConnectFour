#"I hereby certify that this program is solely the result of my own work and is
#in compliance with the Academic Integrity policy of the course syllabus and 
#the academic integrity policy of the CS department.”

import Draw
import random
import time

#initialize 2D list to represent the board with pieces
gameBoard = [
    [None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None],    
    [None, None, None, None, None, None, None]

]
#initialize a list to keep track of how many spaces are left in each col 
#(each item in the list represents the col it corresponds to)
inRows = [len(gameBoard)-1 for i in range(len(gameBoard[0]))]

#draw play button
def introScreen():
    Draw.setColor(Draw.BLUE)
    Draw.filledRect(150, 250, 600, 200)
    Draw.setColor(Draw.RED)
    Draw.setFontSize(100)
    Draw.string("PLAY", 250, 300)

# waiting for mouse to be pressed    
def startGame(): 
    while True: # waits for play button to be pressed        
        if Draw.mousePressed():
            x=Draw.mouseX()
            y=Draw.mouseY()
            if x<750 and x>150 and y>250 and y<450:
                board()
                return       

#draw the board   
def board():
    #initialize the variables that will calculate each col, row,
    #and the size of each cell/piece on the game board
    pixelBegFirstRow = 1
    pixelBegFirstCol = 20
    
    numPixelsRows = 500 + pixelBegFirstRow
    numPixelsCols = 700 + pixelBegFirstCol  
    
    # Mathematical calculations for rows
    sizeRow = numPixelsRows // len(gameBoard)
    pixelBegLastRow = numPixelsRows - sizeRow + pixelBegFirstRow
    
    # Mathematical calculations for columns
    sizeCol = numPixelsCols // len(gameBoard[0])
    pixelBegLastCol = numPixelsCols - sizeCol + pixelBegFirstCol
    
    sizeOval = 50
    
    #graphic representation of the gameboard
    Draw.clear()
    Draw.setColor(Draw.BLUE)
    Draw.filledRect(80, 80, numPixelsCols, numPixelsRows)
    for row in range(pixelBegFirstRow, pixelBegLastRow, sizeRow):
        for col in range(pixelBegFirstCol, pixelBegLastCol, sizeCol):
            #setting the color for the circles
            if gameBoard[row//sizeRow][col//sizeCol]==Draw.RED:
                Draw.setColor(Draw.RED)
            elif gameBoard[row//sizeRow][col//sizeCol]==Draw.YELLOW:
                Draw.setColor(Draw.YELLOW)
            else:
                Draw.setColor(Draw.WHITE)
            Draw.filledOval(sizeCol+col, sizeRow+row, sizeOval, sizeOval)

#draw the turn plaque to say who's turn it is
def turnPlaque(turnNumber):
    Draw.setColor(Draw.WHITE)
    Draw.setFontSize(20)
    if turnNumber%2==0:
        Draw.string("Your Turn", 360, 45)
    else: 
        Draw.string("Computer's Turn", 360, 45)
    Draw.show()
    
#Find out where the player wants to put a piece.

#First get a click from the player.
def getClick():
    x=Draw.mouseX()
    y=Draw.mouseY()
    return x, y

#Next, check if click is valid, if so, return which col was clicked on          
def isValidClick(x,y): 
    #set width of each column to know which col player clicked in
    columnWidth = 111.42857142857143 #board size divided by amount of columns  
    if y>=80 and y<=580:
        colNumber = int((x-80)/columnWidth)
        tempRow = inRows[colNumber] #calculate which row to place the piece in
        # check if it's valid - if there are empty spots in the column
        if tempRow>=0: 
            return colNumber
    return None

#update 2D list (board) after the player's turn
def gameBoardAndUpdating(turnNumber, x, y):
    tempCol = isValidClick(x,y) #get which col player clicked on   
    if tempCol is None: #don't do anything if click wasn't valid
        return False    
    tempRow = inRows[tempCol] #calculate which row to place the piece in  
    if tempRow>=0 and turnNumber%2==0: 
        gameBoard[tempRow][tempCol] = Draw.RED
        inRows[tempCol] = inRows[tempCol] - 1
        return True
        
            
#finding where there are the most peices in a row - loop in all directions:

#loop horizontally through the rows
def horizontalPiecesInRow():  
    #The first item of each list is the highest number of pieces that were found
    #in a row, the next two items of list are the row and col number of where 
    #the last piece of that "string" of pieces was found.
    bestHorizontalRed = [0, None, None] 
    bestHorizontalYellow = [0, None, None]     
    
    #Loop through each row to find amount of each color next to eachother.
    for row in range(len(gameBoard)): 
        #initialize/set variables equal to zero before each loop
        currRed=0
        currYellow=0
        for col in range(len(gameBoard[0])):
            #If a yellow is found in the cell, add one to the first item of 
            #current yellow list and reset red's current bestRun to zero
            if gameBoard[row][col]== Draw.YELLOW:
                currYellow+=1
                currRed = 0 
                #update original bestRuns if a longer bestRun is found, and
                #there is an empty space next to it
                if currYellow>bestHorizontalYellow[0] and col!=6 \
                   and inRows[col+1]==row:
                    bestHorizontalYellow[0] = currYellow
                    bestHorizontalYellow[1] = row
                    bestHorizontalYellow[2] = col +1 #exactly where the piece should be placed
                #if no empty space after the "string" of yellows, check before it
                elif currYellow>bestHorizontalYellow[0] and col-currYellow!=0 \
                     and inRows[col-currYellow]==row: 
                    bestHorizontalYellow[0] = currYellow
                    bestHorizontalYellow[1] = row
                    bestHorizontalYellow[2] = col-currYellow #exactly where to place the piece
                    
            #If a red is found in the cell, add one to the first item of 
            #current red list and reset yellow's current best run to zero
            elif gameBoard[row][col]== Draw.RED:
                currRed+=1
                currYellow = 0
                #update original bestRuns if a larger bestRun is found
                if currRed>bestHorizontalRed[0] and col!= 6 and \
                   inRows[col+1]==row:
                    bestHorizontalRed[0] = currRed
                    bestHorizontalRed[1] = row
                    bestHorizontalRed[2] = col +1 #add one because it's exactly where the piece should be placed
                #if no empty space after the "string" of reds, check before it
                elif currRed>bestHorizontalRed[0] and col-currRed!= 6 \
                     and inRows[col-currRed]==row:
                    bestHorizontalRed[0] = currRed
                    bestHorizontalRed[1] = row
                    bestHorizontalRed[2] = col-currRed #add one to update exactly where the piece should be placed
      
    return bestHorizontalYellow, bestHorizontalRed
        
#loop through the board to find pieces that are vertically next to eachother (in a col)
def verticalPiecesInRow(): 
    #first item of list is the highest number of pieces that were found in a row, 
    #the next two items of list are the row and col number of where the last 
    #piece of that "string" of pieces was found
    bestVerticalRed = [0, None, None] 
    bestVerticalYellow = [0, None, None]
    #Loop through each column to find amount of each color on top of eachother
    for col in range(len(gameBoard[0])):
        #initialize variables and set equal to zero before starting loop
        currRed=0
        currYellow=0
        for row in range(len(gameBoard)):
            #If a yellow is found in the cell, add one to the first item of 
            #current yellow list and reset currRed's bestRun to zero
            if gameBoard[row][col]== Draw.YELLOW:
                currYellow+=1
                currRed = 0 
                #update original bestRun if a longer bestRun, with an empty 
                #space above it, is found
                if currYellow>bestVerticalYellow[0] and row!=0 and \
                   inRows[col]>=0: 
                    bestVerticalYellow[0] = currYellow
                    bestVerticalYellow[1] = row -1 #exactly where to place piece
                    bestVerticalYellow[2] = col
            #If a red is found in the cell, add one to the first item of 
            #current red list and reset yellow's best run to zero
            elif gameBoard[row][col]== Draw.RED:
                currRed+=1
                currYellow = 0
                #update original bestRuns if a larger bestRun is found
                if currRed>bestVerticalRed[0] and row!=0 and inRows[col]>=0:
                    bestVerticalRed[0] = currRed
                    bestVerticalRed[1] = row - 1 #exactly where to place piece
                    bestVerticalRed[2] = col
                
    return bestVerticalYellow, bestVerticalRed
            
#loop to find pieces of the same color that are digonally in a row

def firstPositiveDiagLoop():
    #initialize variables and set equal to zero before starting loop
    bestDiag1Yellow = [0, None, None]
    bestDiag1Red = [0, None, None]
    for row in range(len(gameBoard)):
        #reset the bestRuns each new loop
        currRed=0
        currYellow=0  
        #set which row and col to start looping from
        startCol = row
        row=0
        for col in range(startCol, len(gameBoard[0])-1, 1):
            #don't check any further if it's already going to be out of range
            if row >= len(gameBoard):
                break
            #If a yellow is found in the cell, add one to the first item of 
            #current yellow list and reset currRed's bestRun to zero
            if gameBoard[row][col]== Draw.YELLOW:
                currYellow+=1
                currRed = 0
                #update original bestRun if a longer bestRun, with an empty 
                #space next to it, is found (first need to make sure that it's 
                #not in the last col and row of the gameBoard and that the next 
                #space is the one it would drop into - meaning, the bottom most 
                #empty space of the col next to this piece is the row that is 
                #diagonally next.)
                #check if there's an empty space diagonally below it
                if currYellow>bestDiag1Yellow[0] and col!=len(gameBoard[0]) and\
                   row!=len(gameBoard) and inRows[col+1] == row+1:
                    bestDiag1Yellow[0] = currYellow
                    bestDiag1Yellow[1] = row+1
                    bestDiag1Yellow[2] = col+1
                #if not, check if there is an empty space diagonally above the
                #"string of pieces"
                elif currYellow>bestDiag1Yellow[0] and col>=currYellow and \
                     inRows[col-currYellow] == row-1:
                    bestDiag1Yellow[0] = currYellow
                    bestDiag1Yellow[1] = row-1
                    bestDiag1Yellow[2] = col-1
            #If a red is found in the cell, add one to the first item of current
            #red list and reset yellow's best run to zero
            elif gameBoard[row][col]== Draw.RED:
                currRed+=1
                currYellow = 0
                #update original bestRuns if a larger bestRun is found with an 
                #empty space diagonally above of below it
                if currRed>bestDiag1Red[0] and col!=len(gameBoard[0]) and \
                   row!=len(gameBoard) and inRows[col+1] == row+1:
                    bestDiag1Red[0] = currRed
                    bestDiag1Red[1] = row+1
                    bestDiag1Red[2] = col+1
                #if not, check if there is an empty space diagonally above the "string of pieces"
                elif currRed>bestDiag1Red[0] and col>=currRed and inRows[col-currRed] == row-1: #and gameBoard[row-1][col-1]== None 
                    bestDiag1Red[0] = currRed
                    bestDiag1Red[1] = row-1
                    bestDiag1Red[2] = col-1
            #if no color is found in cell, reset both current bestRuns to zero
            else:
                currRed = 0
                currYellow = 0 
            row+=1
            startCol+=1
    return bestDiag1Yellow, bestDiag1Red


def secondPositiveDiagLoop():
    #initialize variables and set equal to zero before starting loop
    bestDiag2Yellow = [0, None, None]
    bestDiag2Red = [0, None, None]    
    
    for row in range(1, len(gameBoard), 1):
        #set which col to always start looping from
        startCol = 0
        #reset current bestRuns to zero before each loop through
        currRed=0
        currYellow=0          
        for col in range(startCol, len(gameBoard[0]), 1):
            #don't check any further if it's already going to be out of range
            if row >= len(gameBoard):
                break
            #If a yellow is found in the cell, add one to the first item of 
            #current yellow list and reset currRed's bestRun to zero
            if gameBoard[row][col]== Draw.YELLOW:
                currYellow+=1
                currRed = 0          
                
                #update original bestRun if a longer bestRun, with an empty 
                #space next to it, is found (first check if there's an empty 
                #space diagonally below it)
                if currYellow>bestDiag2Yellow[0] and col!=len(gameBoard[0]) and\
                   row!=len(gameBoard) and inRows[col+1] == row+1:
                    bestDiag2Yellow[0] = currYellow
                    bestDiag2Yellow[1] = row+1
                    bestDiag2Yellow[2] = col+1
                #if not, check if there is an empty space diagonally above the "string of pieces"
                elif currYellow>bestDiag2Yellow[0] and col>=currYellow and inRows[col-currYellow] == row-1:
                    bestDiag2Yellow[0] = currYellow
                    bestDiag2Yellow[1] = row-1
                    bestDiag2Yellow[2] = col-1
            #If a red is found in the cell, add one to the first item of current
            #red list and reset yellow's best run to zero
            elif gameBoard[row][col]== Draw.RED:
                currRed+=1
                currYellow = 0
                #update original bestRun if a larger bestRun is found with an empty space diagonally above or below it
                if currRed>bestDiag2Red[0] and col!=len(gameBoard[0]) and \
                   row!=len(gameBoard) and inRows[col+1] == row+1:
                    bestDiag2Red[0] = currRed
                    bestDiag2Red[1] = row+1
                    bestDiag2Red[2] = col+1
                #if not, check if there is an empty space diagonally above the 
                #"string of pieces"
                elif currRed>bestDiag2Red[0] and col>=currRed and \
                     inRows[col-currRed] == row-1: 
                    bestDiag2Red[0] = currRed
                    bestDiag2Red[1] = row-1
                    bestDiag2Red[2] = col-1
            #if no color is found in cell, reset both yellow's and red's current bestRuns to zero
            else:
                currRed = 0
                currYellow = 0  
            #increment row and col so that it loops properly
            row+=1
            startCol+=1
    return bestDiag2Yellow, bestDiag2Red

def firstNegativeDiagLoop():
    #initialize variables and set equal to zero before starting loop 
    bestDiag3Yellow = [0, None, None]
    bestDiag3Red = [0, None, None]     
    startCol = len(gameBoard[0])-1
    endCol = -1
    for row in range(len(gameBoard)):
        row=0 # so that it will always start looping from the first row
        #reset current bestRuns to zero before each loop through
        currRed=0
        currYellow=0         
        for col in range(startCol, endCol, -1):
            #don't check any further if it's already going to be out of range
            if row >= len(gameBoard):
                break
            #If a yellow is found in the cell, add one to the first item of current yellow list and reset currRed's bestRun to zero
            if gameBoard[row][col]== Draw.YELLOW:
                currYellow+=1
                currRed = 0               
                #update original bestRun if a longer bestRun, with an empty 
                #space next to it, is found (first check if there's an empty
                #space diagonally below it)
                if currYellow>bestDiag3Yellow[0] and row!=len(gameBoard) and \
                   col!=0 and inRows[col-1] == row+1:                    
                    bestDiag3Yellow[0] = currYellow
                    bestDiag3Yellow[1] = row+1
                    bestDiag3Yellow[2] = col-1
                #if not, check if there is an empty space diagonally above the
                #"string of pieces"      
                elif currYellow>bestDiag3Yellow[0] and col+currYellow<=6 and \
                     inRows[col+currYellow] == row-currYellow and \
                     gameBoard[row-currYellow][col+currYellow]== None: 
                    bestDiag3Yellow[0] = currYellow
                    bestDiag3Yellow[1] = row-currRed
                    bestDiag3Yellow[2] = col+currYellow            
            
            #If a red is found in the cell, add one to the first item of 
            #current red list and reset yellow's best run to zero
            elif gameBoard[row][col]== Draw.RED:
                currRed+=1
                currYellow = 0
                #update original bestRun if a larger bestRun is found with an 
                #empty space diagonally above or below it
                if currRed>bestDiag3Red[0] and row!=len(gameBoard) and col!=0 \
                   and inRows[col-1] == row+1:
                    bestDiag3Red[0] = currRed
                    bestDiag3Red[1] = row+1
                    bestDiag3Red[2] = col-1
                #if not, check if there is an empty space diagonally above the
                #"string of pieces"      
                elif currRed>bestDiag3Red[0] and col+currRed<=6 and \
                     inRows[col+currRed] == row-currRed: 
                    bestDiag3Red[0] = currRed
                    bestDiag3Red[1] = row-currRed
                    bestDiag3Red[2] = col+currRed              
            row+=1
        startCol-=1
    return bestDiag3Yellow, bestDiag3Red


def secondNegativeDiagonalLoop():
    #initialize variables and set equal to zero before starting loop    
    bestDiag4Yellow = [0, None, None]
    bestDiag4Red = [0, None, None]     
       
    startCol = len(gameBoard[0])-1 # col loop should start in
    endCol = -1 #ending of one loop
    
    for row in range(1, len(gameBoard)):
       #set current runs to zero before each loop
        currRed=0
        currYellow=0         
        for col in range(startCol, endCol, -1):
            if row >= len(gameBoard):
                break  
            #If a yellow is found in the cell, add one to the first item of 
            #current yellow list and reset currRed's bestRun to zero
            if gameBoard[row][col]== Draw.YELLOW:
                currYellow+=1
                currRed = 0    
                #update original bestRun if a longer bestRun, with an empty 
                #space next to it, is found (first check if there's an empty 
                #space diagonally below it)
                if currYellow>bestDiag4Yellow[0] and row!=len(gameBoard) and \
                   col!=0 and inRows[col-1] == row+1:
                    bestDiag4Yellow[0] = currYellow
                    bestDiag4Yellow[1] = row+1
                    bestDiag4Yellow[2] = col-1
                #if not, check if there is an empty space diagonally above the 
                #"string of pieces"      
                elif currYellow>bestDiag4Yellow[0] and col+currYellow<=6 and \
                     inRows[col+currYellow] == row-currYellow:
                    bestDiag4Yellow[0] = currYellow
                    bestDiag4Yellow[1] = row-currYellow
                    bestDiag4Yellow[2] = col+currYellow    
            #If a red is found in the cell, add one to the first item of current
            #red list and reset yellow's best run to zero
            elif gameBoard[row][col]== Draw.RED:
                currRed+=1
                currYellow = 0
                #update original bestRun if a larger bestRun is found with an 
                #empty space diagonally above or below it  
                if currRed>bestDiag4Red[0] and row!=len(gameBoard) and col!=0 \
                   and inRows[col-1] == row+1:
                    bestDiag4Red[0] = currRed
                    bestDiag4Red[1] = row+1
                    bestDiag4Red[2] = col-1
                #if not, check if there is an empty space diagonally above the "string of pieces"      
                elif currRed>bestDiag4Red[0] and col+currRed<=6 and inRows[col+currRed] == row-currRed and gameBoard[row-currRed][col+currRed]== None: #and row!=0 
                    bestDiag4Red[0] = currRed
                    bestDiag4Red[1] = row-currRed
                    bestDiag4Red[2] = col+currRed                   
            row+=1
    return bestDiag4Yellow, bestDiag4Red

#Figure out the bestRun out of all the diagonals (red and then yellow). 
#Going to use these new variables in the yellowBest and redBest functions 
#when looking for the total bestRun of each color.
def diagonalREDPiecesInRow(bestDiag1Red, bestDiag2Red, \
                           bestDiag3Red, bestDiag4Red):
    bestRedDiag = [0, None, None]
    if bestDiag1Red[0]>bestDiag2Red[0] and \
       bestDiag1Red[0]>bestDiag3Red[0] and \
       bestDiag1Red[0]>bestDiag4Red[0]:
        bestRedDiag = bestDiag1Red
    elif bestDiag2Red[0]>bestDiag1Red[0] and \
         bestDiag2Red[0]>bestDiag3Red[0] and \
         bestDiag2Red[0]>bestDiag4Red[0]:
        bestRedDiag = bestDiag2Red
    elif bestDiag3Red[0]>bestDiag1Red[0] and \
         bestDiag3Red[0]>bestDiag2Red[0] and \
         bestDiag3Red[0]>bestDiag4Red[0]:
        bestRedDiag = bestDiag3Red
    elif bestDiag4Red[0]>bestDiag1Red[0] and \
         bestDiag4Red[0]>bestDiag2Red[0] and \
         bestDiag4Red[0]>bestDiag3Red[0]:
        bestRedDiag = bestDiag4Red  
    return bestRedDiag

def diagonalYELLOWPiecesInRow(bestDiag1Yellow, bestDiag2Yellow, \
                              bestDiag3Yellow, bestDiag4Yellow):
    if bestDiag1Yellow[0]>bestDiag2Yellow[0] and \
       bestDiag1Yellow[0]>bestDiag3Yellow[0] and \
       bestDiag1Yellow[0]>bestDiag4Yellow[0]:
        return bestDiag1Yellow
    elif bestDiag2Yellow[0]>bestDiag1Yellow[0] and \
         bestDiag2Yellow[0]>bestDiag3Yellow[0] and \
       bestDiag2Yellow[0]>bestDiag4Yellow[0]:
        return bestDiag2Yellow
    elif bestDiag3Yellow[0]>bestDiag1Yellow[0] and \
         bestDiag3Yellow[0]>bestDiag2Yellow[0] and \
       bestDiag3Yellow[0]>bestDiag4Yellow[0]:
        return bestDiag3Yellow
    elif bestDiag4Yellow[0]>bestDiag1Yellow[0] and \
         bestDiag4Yellow[0]>bestDiag2Yellow[0] and \
       bestDiag4Yellow[0]>bestDiag3Yellow[0]:
        return bestDiag4Yellow


#finding the bestRun out of all the loopings:
def yellowBest(bestVerticalYellow, bestHorizontalYellow, bestYellowDiagonal):
    bestYellow = [0, None, None]
    if bestVerticalYellow[0] > bestHorizontalYellow[0] and \
       bestVerticalYellow[0] > bestYellowDiagonal[0]:
        bestYellow = bestVerticalYellow
    elif bestHorizontalYellow[0] > bestVerticalYellow[0] and \
         bestHorizontalYellow[0] > bestYellowDiagonal[0]:
        bestYellow = bestHorizontalYellow
    elif bestYellowDiagonal[0] > bestVerticalYellow[0] and \
         bestYellowDiagonal[0] > bestHorizontalYellow[0]:
        bestYellow = bestYellowDiagonal
    elif bestYellowDiagonal[0]== bestVerticalYellow[0] or \
         bestYellowDiagonal[0] == bestHorizontalYellow[0]:
        bestYellow = bestYellowDiagonal
    elif bestVerticalYellow[0] == bestHorizontalYellow[0]:
        bestYellow = bestVerticalYellow
    return bestYellow 

def redBest(bestVerticalRed, bestHorizontalRed, bestRedDiagonal):
    bestRed = [0, None, None]
    if bestVerticalRed[0]>bestHorizontalRed[0] and \
       bestVerticalRed[0] > bestRedDiagonal[0]:
        bestRed = bestVerticalRed
    elif bestHorizontalRed[0]> bestVerticalRed[0] and \
         bestHorizontalRed[0] > bestRedDiagonal[0]:
        bestRed = bestHorizontalRed
    elif bestRedDiagonal[0] > bestHorizontalRed[0] and \
         bestRedDiagonal[0] > bestVerticalRed[0]:
        bestRed = bestRedDiagonal
    elif bestRedDiagonal[0]== bestHorizontalRed[0] or \
         bestRedDiagonal[0] == bestVerticalRed[0]:
        bestRed = bestRedDiagonal
    elif bestVerticalRed[0] == bestHorizontalRed[0]:
        bestRed = bestVerticalRed    
    return bestRed

def bestRunsInformation():
    #get the information about bestRuns from each loop
    bestHorizontalYellow, bestHorizontalRed = horizontalPiecesInRow()
    bestVerticalYellow, bestVerticalRed = verticalPiecesInRow()
    
    #get the info from diagonal loops and then use that info to compare 
    #all diagonal bestRuns
    bestDiag1Yellow, bestDiag1Red = firstPositiveDiagLoop()
    bestDiag2Yellow, bestDiag2Red = secondPositiveDiagLoop()            
    bestDiag3Yellow, bestDiag3Red = firstNegativeDiagLoop()            
    bestDiag4Yellow, bestDiag4Red = secondNegativeDiagonalLoop()
    
    #finding the bestRun out off all the diagonals of red
    bestRedDiagonal = diagonalREDPiecesInRow(bestDiag1Red, bestDiag2Red, \
                                             bestDiag3Red, bestDiag4Red)
    #finding the bestRun out off all the diagonals of yellow
    bestYellowDiagonal = diagonalYELLOWPiecesInRow(bestDiag1Yellow, \
                                                   bestDiag2Yellow, \
                                                   bestDiag3Yellow, \
                                                   bestDiag4Yellow)
    
    theBestRed = redBest(bestVerticalRed, bestHorizontalRed, bestRedDiagonal)
    theBestYellow = yellowBest(bestVerticalYellow, bestHorizontalYellow, \
                               bestRedDiagonal)
    
    return  theBestRed, theBestYellow




#Computer's Turn:
#Check what the final best run of each color is and 
#use that info to choose where to go
def compStrategy(totalRedBestRun, totalYellowBestRun):
    #best place for comp to go is if can add onto a yellow's (comp) bestRun of 3
    if totalYellowBestRun[0] == 3:
        row = totalYellowBestRun[1]
        col = totalYellowBestRun[2]
        gameBoard[row][col] = Draw.YELLOW
        inRows[col]= inRows[col] - 1
    #if can't, comp should block player from getting 4 in a row (ie. winning)
    elif totalRedBestRun[0] == 3:
        row = totalRedBestRun[1]
        col = totalRedBestRun[2]
        gameBoard[row][col] = Draw.YELLOW
        inRows[col]= inRows[col] - 1
    #if there's no bestRun of 3 (with valid space next to it), then look for a
    #bestRun of 2 yellows
    elif totalYellowBestRun[0] == 2:
        row = totalYellowBestRun[1]
        col = totalYellowBestRun[2]
        gameBoard[row][col] = Draw.YELLOW
        inRows[col]= inRows[col] - 1
    #if no bestRun of 2 yellows, check for bestRun of 2 reds (player's pieces)
    elif totalRedBestRun[0] == 2:
        row = totalRedBestRun[1]
        col = totalRedBestRun[2]      
        gameBoard[row][col] = Draw.YELLOW 
        inRows[col]= inRows[col] - 1
    #if there is no bestRun of at least 2 or more, with a valid space next to 
    #it, comp should go in a random valid space
    else:
        while True:
            col = random.randint(0, len(gameBoard[0])-1)
            row = inRows[col]

            if inRows[col]>=0:
                gameBoard[row][col] = Draw.YELLOW
                inRows[col]= inRows[col] - 1
                break
            
def gameOver(totalRedBestRun, totalYellowBestRun):
    #If someone won, draw the gameOver plaque
    if totalRedBestRun[0] == 4 or totalYellowBestRun[0] ==4:
        Draw.setColor(Draw.WHITE) 
        Draw.filledRect(150, 250, 600, 200)
        Draw.setColor(Draw.RED)
        Draw.setFontSize(70)        
        if totalRedBestRun[0] == 4:   
            #player won, make exciting sign!
            Draw.string("YOU WON!!", 165, 300)
            Draw.show()
            time.sleep(3)
            introScreen()
            return True
        elif totalYellowBestRun[0] ==4:
            #comp won, write "you lost"
            Draw.string("You lost", 165, 300) 
            Draw.show()
            time.sleep(3)
            introScreen()
            return True
    return False           

def main():
    #drawing the canvas
    Draw.setCanvasSize(900, 700)
    Draw.setBackground(Draw.BLACK)        
    
    introScreen()   # display "start" button
    startGame()     # wait for player to press "start" button
    turnNumber = 0
    gameAllOver = False
    
    board()     # draws the updated board
    turnPlaque(turnNumber) # changes plaque saying whose turn it is
    Draw.show()
    
        
    # the game itself - player clicks where to put pieces and comp uses strategy
    while not gameAllOver:    
        #if player clicks, check if valid click
        #if valid click, place the piece there and turnNumber+=1
        #if it's the player's turn and mouse was pressed, run player's turn
        if turnNumber%2==0 and Draw.mousePressed(): 
            x, y = getClick()
            playerWent = gameBoardAndUpdating(turnNumber, x, y)  # Wait for click and update board
            if playerWent==True: #only change things if player's click was valid
                totalRedBestRun , totalYellowBestRun  = bestRunsInformation()
                #if game is over, sign should show and game should stop running:
                gameAllOver = gameOver(totalRedBestRun, totalYellowBestRun)
                turnNumber+=1 #update turnNumber so that it will go to comp turn
            
        elif turnNumber%2!=0: #then it's the comp's turn
            time.sleep(1)
            turnPlaque(turnNumber) # changes plaque saying whose turn it is
            #gather info of bestRuns and use it for startegy for comp's turn
            totalRedBestRun , totalYellowBestRun  = bestRunsInformation()
            compTurn = compStrategy(totalRedBestRun, totalYellowBestRun) 
            turnNumber+=1 #update turnNumber so it will be player's turn again
            gameAllOver = gameOver(totalRedBestRun, totalYellowBestRun)
        
        board()     # draws the updated board
        turnPlaque(turnNumber) # changes plaque saying whose turn it is
        
main()
    
            

        