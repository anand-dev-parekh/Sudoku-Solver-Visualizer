from collections import deque
import tkinter

root = tkinter.Tk()
root.title("Sudoku Solver")







class Solver:
    def __init__(self, master):
        
        
        self.cells = {}
        self.entries = []
        for row in range(1, 10):
            for column in range(1, 10):
                if ((row in (1,2,3,7,8,9) and column in (4,5,6)) or (row in (4,5,6) and column in (1,2,3,7,8,9))):
                    color='gray20'
                else:
                    color='gray80'
                cell = tkinter.Frame(master, bg='white', highlightbackground=color, highlightcolor=color, highlightthickness=2, width=50, height=50, padx=3,  pady=3, background='black')
                cell.grid(row=row, column=column)
                self.cells[(row, column)] = cell


                e = tkinter.Entry(self.cells[row, column], justify='center')
                e.place(height=40, width=40)
                
                self.entries.append(e)


        self.topFrame = tkinter.Frame(master)
        self.topFrame2 = tkinter.Frame(master)
        self.topFrame3 = tkinter.Frame(master)

        self.solveButton = tkinter.Button(self.topFrame, text="SOLVE", command=self.solve)
        self.solveButton.pack()
        

        self.visualButton = tkinter.Button(self.topFrame2, text="VISUAL", command=self.visualbacktrack)
        self.visualButton.pack()


        self.resetButton = tkinter.Button(self.topFrame3, text="CLEAR", command=self.reset)
        self.resetButton.pack()

        self.topFrame.grid(column=5, row=0)
        self.topFrame2.grid(column=4, row=0)
        self.topFrame3.grid(column=6, row=0)





    def turnToList(self):
        outputList = []
        for row in range(9):
            nestedList = []
            for column in range(9):
                if self.entries[column + (row * 9)].get() == "":
                    nestedList.append("")
                else:
                    nestedList.append(int(self.entries[column + (row * 9)].get()))
            outputList.append(nestedList)
        return outputList



    #BACKTRACKING METHOD

    def pickEmpty(self, inputBoard, slow):
        self.stack = deque()
        rowIndex = 0
        columnIndex = 0
        while rowIndex < 9:
            columnIndex = 0
            while columnIndex < 9:
                if inputBoard[rowIndex][columnIndex] == '':
                    index = self.trynum([rowIndex, columnIndex], 1, inputBoard, slow)
                    rowIndex = index[0]
                    columnIndex = index[1]

                columnIndex += 1
            rowIndex += 1



    def sqaureIndex(self, indexes, daboard):

        if indexes[0] >= 0 and indexes[0] < 3:
            if indexes[1] >= 0 and indexes[1] < 3:
                return [daboard[0][0], daboard[0][1], daboard[0][2], daboard[1][0], daboard[1][1], daboard[1][2], daboard[2][0], daboard[2][1], daboard[2][2]]
            elif indexes[1] >= 3 and indexes[1] < 6:
                return [daboard[0][3], daboard[0][4], daboard[0][5], daboard[1][3], daboard[1][4], daboard[1][5], daboard[2][3], daboard[2][4], daboard[2][5]]
            else:
                return [daboard[0][6], daboard[0][7], daboard[0][8], daboard[1][6], daboard[1][7], daboard[1][8], daboard[2][6], daboard[2][7], daboard[2][8]]

        elif indexes[0] >= 3 and indexes[0] < 6:
            if indexes[1] >= 0 and indexes[1] < 3:
                return [daboard[3][0], daboard[3][1], daboard[3][2], daboard[4][0], daboard[4][1], daboard[4][2], daboard[5][0], daboard[5][1], daboard[5][2]]
            elif indexes[1] >= 3 and indexes[1] < 6:
                return [daboard[3][3], daboard[3][4], daboard[3][5], daboard[4][3], daboard[4][4], daboard[4][5], daboard[5][3], daboard[5][4], daboard[5][5]]
            else:
                return [daboard[3][6], daboard[3][7], daboard[3][8], daboard[4][6], daboard[4][7], daboard[4][8], daboard[5][6], daboard[5][7], daboard[5][8]]

        else:
            if indexes[1] >= 0 and indexes[1] < 3:
                return [daboard[6][0], daboard[6][1], daboard[6][2], daboard[7][0], daboard[7][1], daboard[7][2], daboard[8][0], daboard[8][1], daboard[8][2]]
            elif indexes[1] >= 3 and indexes[1] < 6:
                return [daboard[6][3], daboard[6][4], daboard[6][5], daboard[7][3], daboard[7][4], daboard[7][5], daboard[8][3], daboard[8][4], daboard[8][5]]
            else:
                return [daboard[6][6], daboard[6][7], daboard[6][8], daboard[7][6], daboard[7][7], daboard[7][8], daboard[8][6], daboard[8][7], daboard[8][8]]


    def trynum(self, indexes, start, boardInput, visual):
        
        for number in range(start, 10):
            if number not in set(boardInput[indexes[0]]) and number not in set([x[indexes[1]] for x in boardInput]) and number not in set(self.sqaureIndex(indexes, boardInput)):
                boardInput[indexes[0]][indexes[1]] = number




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


    def backtrack(self, boardinp, slow):
        lastWrong = self.stack.pop()
        prevVal = boardinp[lastWrong[0]][lastWrong[1]]
        boardinp[lastWrong[0]][lastWrong[1]] = ''


        self.entries[lastWrong[0] * 9 + lastWrong[1]].delete(0, tkinter.END)

        return self.trynum(lastWrong, prevVal + 1, boardinp, slow)
    #END BACKTRACK 


    def isvalid(self, userBoard):
        return True



    def solve(self):
        if self.isvalid("Not Finished"):
            self.pickEmpty(self.turnToList(), False)


    def visualbacktrack(self):
        if self.isvalid("Not Finished"):
            self.pickEmpty(self.turnToList(), True)


    def reset(self):
        for value in self.entries:
            value.delete(0, tkinter.END)
            value.configure(foreground="black")



ye = Solver(root)


root.mainloop() 

