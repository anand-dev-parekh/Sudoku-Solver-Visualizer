from collections import deque
import tkinter

root = tkinter.Tk()
root.title("Sudoku Solver")


class Solver:
    def __init__(self, master):
        
        #Initializing objects
        self.cells = {}
        self.entries = []
        for row in range(1, 10):
            for column in range(1, 10):
                if ((row in (1,2,3,7,8,9) and column in (4,5,6)) or (row in (4,5,6) and column in (1,2,3,7,8,9))):
                    color='gray20'
                else:
                    color='gray80'
                cell = tkinter.Frame(master, highlightbackground=color, highlightcolor=color, highlightthickness=2, width=50, height=50, padx=3,  pady=3, background='black')
                cell.grid(row=row, column=column)
                self.cells[(row, column)] = cell


                e = tkinter.Entry(self.cells[row, column], justify='center')
                e.place(height=40, width=40)
                
                self.entries.append(e)

        #Creates buttons 
        topFrame = tkinter.Frame(master)
        topFrame2 = tkinter.Frame(master)
        topFrame3 = tkinter.Frame(master)


        solveButton = tkinter.Button(topFrame, text="SOLVE", command=self.solve)
        solveButton.pack()
        

        visualButton = tkinter.Button(topFrame2, text="VISUAL", command=self.visualbacktrack)
        visualButton.pack()


        resetButton = tkinter.Button(topFrame3, text="CLEAR", command=self.reset)
        resetButton.pack()

        topFrame.grid(column=5, row=0)
        topFrame2.grid(column=4, row=0)
        topFrame3.grid(column=6, row=0)


    #Converts user input into an array/python list
    def turnToList(self):
        outputList = []

        for row in range(9):
            nestedList = []

            for column in range(9):

                if self.entries[column + (row * 9)].get() == "":
                    nestedList.append(0)
                else:
                    nestedList.append(int(self.entries[column + (row * 9)].get()))

            outputList.append(nestedList)

        return outputList

    #BACKTRACKING METHOD
    def pickEmpty(self, inputBoard, vis):
        self.stack = deque()
        rowIndex = 0
        columnIndex = 0

        while rowIndex < 9:
            columnIndex = 0

            while columnIndex < 9:
                if inputBoard[rowIndex][columnIndex] == 0:
                    
                    #Trys to input num from 1-9
                    index = self.trynum([rowIndex, columnIndex], 1, inputBoard, vis)
                    
                    rowIndex = index[0]
                    columnIndex = index[1]

                columnIndex += 1
            rowIndex += 1


    #If number does not exist in row, column, or square
    def validInput(self, number, boardInput, indexes):
        if (not self.inColumn(number, boardInput, indexes) and not self.inRow(number, boardInput, indexes) and not self.inSquare(number, boardInput, indexes)):
            return True
        return False


    #HELPER FUNCTIONS FOR validInput

    #If number exists in its row
    def inRow(self, number, boardInput, indexes):
        for num in boardInput[indexes[0]]:
            if number == num:
                return True
        return False
    
    #If number exists in its column
    def inColumn(self, number, boardInput, indexes):
        for row in boardInput:
            if row[indexes[1]] == number:
                return True
        return False 
    
    #If number exists in the square of it self
    def inSquare(self, number, boardInput, indexes):
        botX = (indexes[0] // 3) * 3
        topX = ((indexes[0] // 3) * 3) + 3
                  
        botY = (indexes[1] // 3) * 3
        topY = ((indexes[1] // 3) * 3) + 3

        for x in range(botX, topX):
            for y in range(botY, topY):
                if boardInput[x][y] == number:
                    return True
        return False
    #END HELPER FUNCTIONS FOR 

    def trynum(self, indexes, start, boardInput, visual):
        
        for number in range(start, 10):
            if self.validInput(number, boardInput, indexes):
                
                boardInput[indexes[0]][indexes[1]] = number

                #Updates color change if visual
                if visual:
                    self.entries[(indexes[0] * 9 + indexes[1])].configure(foreground="red", highlightbackground="green")
                    self.entries[(indexes[0] * 9 + indexes[1])].insert(0, number)
                    root.update()
                    self.entries[(indexes[0] * 9 + indexes[1])].configure(foreground="red", highlightbackground="white")
                
                else:
                    self.entries[(indexes[0] * 9 + indexes[1])].configure(foreground="red")
                    self.entries[(indexes[0] * 9 + indexes[1])].insert(0, number)
                

                self.stack.append(indexes)

                return indexes

        return self.backtrack(boardInput, visual)


    def backtrack(self, boardinp, vis):
        lastWrong = self.stack.pop()
        
        #Stores previous wrong value
        prevVal = boardinp[lastWrong[0]][lastWrong[1]]
        
        #Resets last wrong to 0 + deltes from GUI
        boardinp[lastWrong[0]][lastWrong[1]] = 0
        self.entries[lastWrong[0] * 9 + lastWrong[1]].delete(0, tkinter.END)

        return self.trynum(lastWrong, prevVal + 1, boardinp, vis)
    #END BACKTRACK 


    def isBoardValid(self, userBoard):
        return True

    #Normal Solve
    def solve(self):
        if self.isBoardValid("Not Finished"):
            self.pickEmpty(self.turnToList(), False)

    #Visual Solve
    def visualbacktrack(self):
        if self.isBoardValid("Not Finished"):
            self.pickEmpty(self.turnToList(), True)

    #Reset Board
    def reset(self):
        for value in self.entries:
            value.delete(0, tkinter.END)
            value.configure(foreground="black")



ye = Solver(root)


root.mainloop() 
