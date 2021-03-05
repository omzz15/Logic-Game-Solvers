# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 12:22:37 2020

@author: q774283
"""

grid_size = 5
range5 = range(5)

snail_board = [
    '...23',
    '..231',
    '1...2',
    '3....',
    '213..'
]

def get_snail_data():
    sd = SnailData()
    for r in range5:
        for c in range5:
            if snail_board[r][c] != '.':
                sd.set_value(int(snail_board[r][c]), r, c)
    return sd

def get_all_possible_values():
    return [0, 1, 2, 3]

class SnailData:
    
    def __init__(self):
        self.data = [[None]*grid_size for _ in range5]
        self.possible_values = [[None]*grid_size for _ in range5]
        for r in range5:
            for c in range5:
                self.possible_values[r][c] = get_all_possible_values()
        # 1st row constraints
        self.possible_values[0][0].remove(2)
        self.possible_values[0][0].remove(3)
        self.possible_values[0][1].remove(3)
        self.possible_values[0][3].remove(1)
        self.possible_values[0][4].remove(1)
        self.possible_values[0][4].remove(2)
        # last column constraints
        self.possible_values[1][4].remove(2)
        self.possible_values[1][4].remove(3)
        self.possible_values[2][4].remove(3)
        self.possible_values[4][4].remove(1)
        
        # center part constraints
        self.possible_values[2][2].remove(1)
        self.possible_values[2][2].remove(2)
        self.possible_values[2][1].remove(1)
        
    
    def set_value(self, val, row, col):
        self.data[row][col] = val
        for i in range5:
            if val in self.possible_values[row][i]:
                self.possible_values[row][i].remove(val)
            if val in self.possible_values[i][col]:
                self.possible_values[i][col].remove(val)
        self.possible_values[row][col] = [val]
            
    def solve(self):
        pass
    
    def print(self):
        for d in self.data:
            print(d)
        for pv in self.possible_values:
            print(pv)

sd = get_snail_data()
sd.print()
