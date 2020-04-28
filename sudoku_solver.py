import numpy as np
from tkinter import *
import time

class Sudoku:
    def __init__(self, shuffle = False):
        self.board = np.zeros((9,9))
        self.shuffle = shuffle
        self.entry_dict = {}
        self.tasks = []
        self.tasks_len = -1
   
    def generate(self):
        self.board = np.zeros((9,9))
        self.updateUI()
        if self.solve(True):
            idx_toZero = np.random.choice(a= 81, size= int(81 * .9), replace=False)
                       
            self.board = self.board.flatten()
            self.board[idx_toZero] = 0
            self.board = np.reshape(self.board, (9,9))

        self.updateUI()   

    def makeBoard(self):
        dimen = 600
        border = 75
        playable_area = dimen - 2*border
        entry_dimen = playable_area // 9

        self.tk = Tk()
        self.tk.geometry(str(dimen) + 'x' + str(dimen))
        self.tk.resizable(0, 0) 
        
        canvas = Canvas(self.tk, bg='white')
        for x in range(border, dimen, playable_area//3):
            canvas.create_line(x, border, x, dimen - border)
            canvas.create_line(x + 1, border, x + 1, dimen - border)

        for y in range(border, dimen, playable_area//3):
            canvas.create_line(border, y, dimen - border, y)
            canvas.create_line(border, y + 1, dimen - border, y + 1)
        canvas.pack(fill=BOTH, expand=True)

        gen = Button(self.tk, text='Generate', command= self.generate)
        gen.place(x=dimen/2 - 50 , y= dimen - border//2)
        solv = Button(self.tk, text='Solve', command= self.solve)
        solv.place(x=dimen/2 + 50, y= dimen - border//2)
        
        for row in range(9):
            for col in range(9):
                y = border  + ((entry_dimen) * row)
                x = border +  ((entry_dimen) * col)
                if col > 2: 
                    if col > 5:
                        x+=1
                    x+=1
                if row > 2: 
                    if row > 5:
                        y+=1
                    y+=1  

                entry = Entry(self.tk, justify='center', highlightthickness=1, bd=-5, highlightbackground='grey')
                entry.place(x = x, y = y, height = entry_dimen, width = entry_dimen)
                self.entry_dict[(row,col)] = entry    
        
    def isValid(self, coords, entry):
        row_idx, col_idx = coords
        row = self.board[row_idx:row_idx + 1:]
        col = self.board[...,col_idx:col_idx + 1]
        
        block_row = row_idx - row_idx % 3
        block_col = col_idx - col_idx % 3
        block = self.board[block_row: block_row +3, block_col: block_col + 3]
        
        return not (entry in row or entry in col or entry in block) 
    
    def solve(self, generating=False):
        zero = np.where(self.board == 0)
        idx_zero = list(zip(zero[0], zero[1]))
        
        if (len(idx_zero) == 0): 
            return True     

        coords = idx_zero[0]
        values = np.arange(1,10)
        if (generating or self.shuffle): 
            np.random.shuffle(values)

        for num in values:
            if (self.isValid(coords, num)):
                self.board[coords] = num
                if (not generating): self.tasks.append(('ADD', coords, num))
                if (self.solve(generating)): return True
                
                self.board[coords] = 0
                if (not generating): self.tasks.append(('REMOVE', coords, 0))                  

    def updateUI(self):
        for row in range(9):
            for col in range(9):
                sudoku.entry_dict[(row,col)].delete(0, END)
                self.entry_dict[(row, col)].configure(bg = 'white')
                if self.board[row][col] != 0:
                    sudoku.entry_dict[(row,col)].insert(0, int(self.board[row][col]))

    def startUI(self):
        self.makeBoard()
        while True:
            self.tk.update_idletasks()
            if self.tasks_len < len(self.tasks): self.tasks_len = len(self.tasks)
            if self.tasks_len > 0:  print(self.tasks_len)
            if self.tasks:
                action, coords, num = self.tasks[0]
                if action == 'ADD':
                    self.entry_dict[coords].insert(0, int(num))
                    self.entry_dict[coords].configure(bg = 'PaleGreen4')
                elif action == 'REMOVE':
                    self.entry_dict[coords].configure(bg = 'IndianRed3')
                    self.tasks[0] = 'REMOVE2', coords, num
                elif action == 'REMOVE2':
                    self.entry_dict[coords].configure(bg = 'white')
                    self.entry_dict[coords].delete(0, END)
                if action != 'REMOVE': self.tasks.pop(0)
                time.sleep(.1)
            self.tk.update()

sudoku = Sudoku(shuffle = True)
sudoku.startUI()


