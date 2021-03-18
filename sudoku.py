# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 17:20:02 2020

@author: q774283
"""
from random import sample

check_sudoku_grids = [
 "dawssdaswwda",
 "aawssddsssdd",
 "aawwsadwswad",
 "aaswwaawwsad",
 "daswwdawwwdd",
 "dawwsddsswda",
 "adwwsadwwwdd",
 "adsswaaswsad",
 "ddswwdaswsaa"
]

itr = 10000000

base  = 3
side  = base*base

def is_greater(i, j):
    return (i > j)

def is_less(i, j):
    return (i < j)

def up(board, r, c):
    return is_less(board[r][c], board[r+1][c])

def down(board, r, c):
    return is_greater(board[r][c], board[r+1][c])

def left(board, r, c):
    return is_less(board[r][c], board[r][c+1])

def right(board, r, c):
    return is_greater(board[r][c], board[r][c+1])

char_to_func = {'a': left, 'd': right, 'w': up, 's': down}
    
# pattern for a baseline valid solution
def pattern(r,c): return (base*(r%base)+r//base+c)%side

# randomize rows, columns and numbers (of valid base pattern)

def shuffle(s): return sample(s,len(s)) 

def generate_sudoku_board():
    for _ in range(itr):
        rBase = range(base) 
        rows  = [ g*base + r for g in shuffle(rBase) for r in shuffle(rBase) ] 
        cols  = [ g*base + c for g in shuffle(rBase) for c in shuffle(rBase) ]
        nums  = shuffle(range(1,base*base+1))
        
        # produce board using randomized baseline pattern
        board = [ [nums[pattern(r,c)] for c in cols] for r in rows ]
        yield board

def turn_input_to_board(input_values):
    out = []
    box_idx = 0
    for box in input_values:
        row_idx = 0
        col_idx = 0
        num = 0
        for ch in box:
            if num in (4,9):
                col_idx = 2
            elif num in (1,3,6,8,11):
                col_idx = 1
            else:
                col_idx = 0
            row_idx = num//5
            num += 1
            out.append((char_to_func[ch], row_idx+3*(box_idx//3), col_idx+3*(box_idx%3)))
        box_idx += 1
    return out

def is_board_valid(board, l):
    for f, r, c in l:
        if not f(board, r, c): 
            #print(f'{f} - {r} {c}')
            return False
    return True

board_rules = turn_input_to_board(check_sudoku_grids)
sg = generate_sudoku_board()
while itr > 0:
    board = next(sg)
    if itr%1000 == 0: print(itr)
    if is_board_valid(board, board_rules):
        print(board)
        break
    itr -= 1
    #input()
