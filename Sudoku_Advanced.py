# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 19:29:45 2020

@author: q774283
"""
from enum import Enum

input_grid = [
 "daswsdawwsad",
 "aawssdaswsad",
 "dawswdaswsaa",
 "adwwwaawssdd",
 "adsswdasssda",
 "aasssdawwsad",
 "aawwsddswwaa",
 "ddsssddsswaa",
 "adswsadwswdd"
]

range9 = range(9)
range3 = range(3)

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

class RelationshipType(Enum):
    LEFT = 'a'
    RIGHT = 'd'
    UP = 'w'
    DOWN = 's'
    func_d = {LEFT: left, RIGHT: right, UP: up, DOWN: down}
    
    def next_row(self, row):
        if self == RelationshipType.UP or self == RelationshipType.DOWN: return row+1
        return row

    def next_col(self, col):
        if self == RelationshipType.LEFT or self == RelationshipType.RIGHT: return col+1
        return col
    
    def get_func(self):
        return RelationshipType.func_d[self]
    
    def get_opposite(self):
        if self == RelationshipType.LEFT: return RelationshipType.RIGHT
        if self == RelationshipType.RIGHT: return RelationshipType.LEFT
        if self == RelationshipType.UP: return RelationshipType.DOWN
        if self == RelationshipType.DOWN: return RelationshipType.UP
        return None
    
    def get_relationship_type(ch):
        return RelationshipType._value2member_map_[ch]
    
    def __repr__(self):
        return self.name
    
class Board:
    def __init__(self):
        self.boxl = [None]*9
        for i in range9:
            self.boxl[i] = Box(self, i);
        self.rowl = [None]*9
        for i in range9:
            self.rowl[i] = BoardRow(self, i)
        self.coll = [None]*9
        for i in range9:
            self.coll[i] = BoardCol(self, i)

    def solve(self):
        bd = BoardData()
        itr = 5
        while itr > 0:
            self.solve_itr(bd)
            itr -= 1
        bd.print()
        
    def solve_itr(self, bd):
        while True:
            self.analyze_board_data(bd)
            snl = bd.get_single_nums()
            if len(snl) == 0: break
            for val, grow, gcol in snl:
                self.set_value(val, grow, gcol, bd)
        for i in range9:
            rem_vals = self.boxl[i].get_remaining_values(bd)
            print(f'box {i} - {rem_vals}')
            rem_vals = self.rowl[i].get_remaining_values(bd)
            print(f'row {i} - {rem_vals}')
            rem_vals = self.coll[i].get_remaining_values(bd)
            print(f'col {i} - {rem_vals}')
    
    def set_value(self, val, grow, gcol, bd):
        box_id, brow, bcol = Board.convert_grid_to_box(grow, gcol)
        cell = self.get_cell(grow, gcol)
        cell.set_value(val, bd)
        self.boxl[box_id].set_value_cb(val, brow, bcol, bd)
        self.rowl[grow].set_value_cb(val, gcol, bd)
        self.coll[gcol].set_value_cb(val, grow, bd)
        
    def analyze_board_data(self, bd):
        for box in self.boxl:
            box.analyze_board_data(bd)
                            
    def get_cell(self, grow, gcol):
        box_id, row, col = Board.convert_grid_to_box(grow, gcol)
        return self.boxl[box_id].get_cell(row, col)
  
    def add_relationship(self, row, col, rel_type):
        cell = self.get_cell(row, col)
        oth_cell = self.get_cell(rel_type.next_row(row), rel_type.next_col(col))
        cell.add_relationship(oth_cell, rel_type)
    
    def add_all_relationship(self, grid):
        box_idx = 0
        for box in grid:
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
                rel_type = RelationshipType.get_relationship_type(ch)
                grid_idx = Board.convert_box_to_grid(box_idx, row_idx, col_idx)
                self.add_relationship(grid_idx[0], grid_idx[1], rel_type)
            box_idx += 1
            
    def convert_box_to_grid(box,row,col):
        return (row + (box//3)*3, col + (box%3)*3)
    
    def convert_grid_to_box(row, col):
        return ((row//3)*3 + col//3, row%3, col%3)
    
class Box:
    def __init__(self, board, box_id):
        self.box_id = box_id
        self.board = board
        self.cells = [None]*9
        for i in range9:
            self.cells[i] = Cell(self, i//3, i%3)
            
    def get_cell(self, row, col):
        return self.cells[row*3 + col]
    
    def analyze_board_data(self, bd):
        for c in range(8,-1,-1):
            self.cells[c].analyze_board_data(bd)
            
    def get_remaining_values(self, bd):
        rem_values = [1,2,3,4,5,6,7,8,9]
        for r in range3:
            for c in range3:
                grow, gcol = Board.convert_box_to_grid(self.box_id, r, c)
                if bd.data[grow][gcol] in rem_values:
                    rem_values.remove(bd.data[grow][gcol])
        return rem_values

    def set_value_cb(self, val, brow, bcol, bd):
        for cell in self.cells:
            if cell.row != brow or cell.col != bcol:
                cell.set_value_cb(val, bd)
    
class BoardRow:
    def __init__(self, board, row_num):
        self.board = board
        self.row_num = row_num
        self.cells = [None]*9
        for i in range9:
            self.cells[i] = board.get_cell(row_num, i)
        
    def get_remaining_values(self, bd):
        rem_values = [1,2,3,4,5,6,7,8,9]
        for c in range9:
            if bd.data[self.row_num][c] in rem_values:
                rem_values.remove(bd.data[self.row_num][c])
        return rem_values
        
    def set_value_cb(self, val, gcol, bd):
        for cell in self.cells:
            if(cell.grid_col != gcol):
                cell.set_value_cb(val, bd)
            
class BoardCol:
    def __init__(self, board, col_num):
        self.board = board
        self.col_num = col_num
        self.cells = [None]*9
        for i in range9:
            self.cells[i] = board.get_cell(i, col_num)
            
    def get_remaining_values(self, bd):
        rem_values = [1,2,3,4,5,6,7,8,9]
        for r in range9:
            if bd.data[r][self.col_num] in rem_values:
                rem_values.remove(bd.data[r][self.col_num])
        return rem_values

    def set_value_cb(self, val, grow, bd):
        for cell in self.cells:
            if(cell.grid_row != grow):
                cell.set_value_cb(val, bd)
        
class Cell:
    def __init__(self, box, row, col):
        self.box = box
        self.row = row
        self.col = col
        self.grid_row, self.grid_col = Board.convert_box_to_grid(box.box_id, row, col)
        self.relationship = {} 
        
    def add_relationship(self, other_cell, rel_type):
        self.relationship[rel_type] = other_cell
        other_cell.relationship[rel_type.get_opposite()] = self

    def analyze_board_data(self, bd):
        if bd.data[self.grid_row][self.grid_col]: return
        for relation in self.relationship:
            oth_cell = self.relationship[relation]
            if relation == RelationshipType.UP or relation == RelationshipType.LEFT:
                max_val = max(bd.possible_values[oth_cell.grid_row][oth_cell.grid_col])
                for val in range(max_val, 10):
                    if val in bd.possible_values[self.grid_row][self.grid_col]:
                        bd.possible_values[self.grid_row][self.grid_col].remove(val) 
            elif relation == RelationshipType.DOWN or relation == RelationshipType.RIGHT:
                min_val = min(bd.possible_values[oth_cell.grid_row][oth_cell.grid_col])
                for val in range(1, min_val + 1):
                    if val in bd.possible_values[self.grid_row][self.grid_col]:
                        bd.possible_values[self.grid_row][self.grid_col].remove(val)
                
    def set_value(self, val, bd):
        bd.data[self.grid_row][self.grid_col] = val
        bd.possible_values[self.grid_row][self.grid_col] = [val]
        
    def set_value_cb(self, val, bd):
        pvl = bd.possible_values[self.grid_row][self.grid_col]
        if val in pvl:
            pvl.remove(val)

    def __repr__(self):
        return f'{self.box.box_id} - {self.row}, {self.col}'
        
class BoardData:
    def __init__(self):
        self.data = [None]*9
        for i in range9:
            self.data[i] = [None]*9
        self.possible_values = [None]*9
        for r in range9:
            self.possible_values[r] = [None]*9
            for c in range9:
                self.possible_values[r][c] = [1,2,3,4,5,6,7,8,9]
                
    def get_single_nums_row(self, row_id):
        for val in range(1,10):
            num_found = 0
            cols = 0
            for c in range9:
                if val in self.possible_values[row_id][c] and self.data[row_id][c] == None:
                    num_found += 1
                    cols = c
                    if num_found >= 2:
                        break
            if num_found == 1: return (val, row_id, cols)
        return (None, None, None)
            
    def get_single_nums_col(self, col_id):
        for val in range(1,10):
            num_found = 0
            rows = 0
            for r in range9:
                if val in self.possible_values[r][col_id] and self.data[r][col_id] == None:
                    num_found += 1
                    rows = r
                    if num_found >= 2:
                        break
            if num_found == 1: return (val, rows, col_id)
        return (None, None, None)
        
    def get_single_nums_box(self, box_id):
        for val in range(1,10):
            num_found = 0
            pos_found = None
            for r in range(3):
                for c in range(3):        
                    pos = Board.convert_box_to_grid(box_id, r, c)
                    if val in self.possible_values[pos[0]][pos[1]] and self.data[pos[0]][pos[1]] == None:
                        num_found += 1
                        pos_found = pos
                if num_found >= 2:
                    break
            if num_found == 1: return (val, pos_found[0], pos_found[1]) 
        return (None, None, None)
    
    def get_single_nums(self):
        all_singles = set()
        for r in range9:
            pos = self.get_single_nums_row(r)
            if pos[0]: all_singles.add(pos)
            pos = self.get_single_nums_col(r)
            if pos[0]: all_singles.add(pos)
            pos = self.get_single_nums_box(r)
            if pos[0]: all_singles.add(pos)
        return all_singles

    def print(self):
        print('|-----------------------|')        
        for r in range9:
            for c in range9:
                val = self.data[r][c]
                if c%3 == 0: print('|', end=' ')
                print(val if val else ' ', end=' ')
            print('|')
            if r%3 == 2: print('|-----------------------|')
        for r in range9:
            for c in range9:
                print(f'{r}-{c} : {self.possible_values[r][c]}')

        
b = Board()
b.add_all_relationship(input_grid)
b.solve()
