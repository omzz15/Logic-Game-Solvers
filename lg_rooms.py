# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 20:54:26 2021

@author: dromp_50a1bpc
"""
import enum

gridSize = 2
board = [
    [2,2],
    [1,1]
]
grange = range(gridSize)

class Dir(enum.Enum):
    UP = 0
    DOWN = 2
    LEFT = 1
    RIGHT = 3
    
class Node:
    def __init__(self, row, col, solNum):
        self.neighbors = [None]*4
        self.solNum = solNum
        self.row = row
        self.col = col
    
    def is_solved(self):
        return self.calc_curr_num() == self.solNum
    
    def is_valid(self, d):
        return self.calc_curr_num() - self.get_cnt(d) >= self.solNum

    def get_cnt(self, d):
        if self.neighbors[d]:
            return self.neighbors[d].get_cnt(d)+1
        return 0
    
    def calc_curr_num(self):
        return self.get_cnt(0) + self.get_cnt(1) + self.get_cnt(2) + self.get_cnt(3)
        
    def get_node_rank(self):
        return self.solNum + sum(1 for n in self.neighbors if n)
    
def build_nodes(b):
    node_b = [[None]*gridSize for _ in grange]
    for r in grange:
        for c in grange:
            node_b[r][c] = Node(r,c,board[r][c])
            if(r > 0):
                node_b[r][c].neighbors[Dir.UP.value] = node_b[r-1][c]
                node_b[r-1][c].neighbors[Dir.DOWN.value] = node_b[r][c]
            if(c > 0):
                node_b[r][c].neighbors[Dir.LEFT.value] = node_b[r][c-1]
                node_b[r][c-1].neighbors[Dir.RIGHT.value] = node_b[r][c]
    return node_b

def get_least_rank(ng):
    min_rn = ng[0][0]
    for r in grange:
        for c in grange:
            if ng[r][c].is_solved(): continue
            if ng[r][c].get_node_rank() < min_rn.get_node_rank():
                min_rn = ng[r][c]
    return min_rn

def is_board_solved(ng):
    for r in ng:
        for node in r:
            if not node.is_solved(): return False
    return True
    
    
def solve_rec(ng):
    if is_board_solved(ng): return (True, None)
    sn = get_least_rank(ng)
    print(sn)
    any_valid_move = False
    
    for i in range(4):
        if sn.neighbors[i] and sn.is_valid(i):
            opp = i - 2
            if opp < 0:
                opp += 4
            sn.neighbors[i].neighbors[opp] = None
            sn.neighbors[opp] = None
            any_valid_move = True
            r = solve_rec(ng)
            if r[0]: return r
    return (False, any_valid_move)
    
    
ng = build_nodes(board)
sn = solve_rec(ng)
print(is_board_solved(ng))
