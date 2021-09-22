#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  3 15:35:40 2021

@author: diegotoledano
"""
#Board object to represent game 

import random
import re


class Board:
    
    def __init__(self, dim_size, num_bombs):
        #keep rack of these parameters
        self.dim_size = dim_size
        self.num_bombs = num_bombs        
        
        #create board
        #use helper function
        self.board = self.make_new_board() #plant the bombs
        self.assign_values_to_board()

        #initialize a set to keep track of which locations have been uncovered
        #well save row, columns into this tuple
        self.dug = set() #if we dig at 0,0 then self.dug = {(0,0)}
    
    def make_new_board(self):
        
        #construct a new board based on the dimseze and numbombs
        #since its 2d list of lists is appropriate
        
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        
        #plant the bombs
        
        bombs_planted = 0
        
        
        while bombs_planted < self.num_bombs:
            
            loc = random.randint(0, self.dim_size**2 -1)
            row = loc // self.dim_size
            col = loc % self.dim_size
            
            if board[row][col] == '*':
                #this means weve actually planted a bomb there already
                continue
            board[row][col] = '*' # planting bomb
            bombs_planted += 1
            
        return board
            
    
    def assign_values_to_board(self):
        
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    # if this is already a bomb, we don't want to calculate anything
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r, c)

                
    def get_num_neighboring_bombs(self, row, col):
        
        #we iterate through all the neighboring cells with coordinates -1
        
        num_neighboring_bombs = 0
        for r in range(max(0,row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0,col-1),min(self.dim_size-1, col+1)+1):
                if r == row and c == col:
                    continue
                if self.board[r][c] == '*':
                    num_neighboring_bombs +=1
                    
        return num_neighboring_bombs


    def dig(self, row, col):
        
        #dog at that location, return True if succesful False if bomb dug
        #1. hit a bomb ---> game over, 2. dig at location with neighbor bombs
        #3. dig at location with no neighbor bombs
        
        self.dug.add((row,col)) #keep track of dig
        
        if self.board[row][col] =='*':
            return False
        elif self.board[row][col] > 0:
            return True
        
        for r in range(max(0,row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0,col-1),min(self.dim_size-1, col+1)+1):
                if (r,c) in self.dug:
                    continue
                self.dig(r,c)
        return True
    
    def __str__(self):
        visible_board = [[None for _ in range(self.dim_size)]for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                    
                else:
                    visible_board[row][col] = ' '
        
        #put together in a string
        string_rep = ''
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )
               
        #print csv strings 
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'
        
        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format %(col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'
            
        str_len = int(len(string_rep) /self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len
        
        return string_rep
                
        
#play game
def play(dim_size=10, num_bombs=10):
    
    #Step 1: create the board and plant the bombs
    board = Board(dim_size, num_bombs)
    #Step 2: show the user the board and ask for where they want to dig
    #Step 3a: If location is a bomb show 'game over message'
    #Step 3b: if location is not abomb, dig recursively until each square is at 
    #least next to a bomb
    #Step 4: repeat steps 2 and 3 a/b until there are bo more places to dig ---> VICTORY
    
    safe  = True
    
    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)
        user_input = re.split(',(\\s)*', input("Where would you like to dig? Input as row,col: "))
        row, col = int(user_input[0]), int(user_input[-1])
        
        if row < 0 or row >= board.dim_size or col < 0 or col >= dim_size:
            print('Invalid location. Try again')
            continue
        #if input is valid
        safe = board.dig(row, col)
        
        if not safe:
            break #game over
    if safe: 
        print('A PERRO GANASTE!')
        
    else:
        print('PELASTE BRO')
        board.dug = [(r,c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)
        
if __name__ == '__main__':
    play()
            
        
        
        
