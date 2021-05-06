# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 20:07:42 2018

@author: gauta
"""
from functools import reduce
import copy
import random

b_size = 5
last_no = 3
#init_board = [[0, 1, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 3, 0, 2], [0, 0, 0, 0, 0], [0, 2, 0, 3, 0]]
init_board = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 3, 0, 0], [0, 0, 2, 0, 0], [0, 0, 0, 0, 0]]

b_size_half = int(b_size/2)
loop_count = int(b_size/2)
b_rc_sum = int(last_no * (last_no+1) / 2)
b_rc_product = reduce(lambda x, y: x*y, range(1, last_no+1))

def prepareNegConstraint(n):
    nc = [0]*b_size
    for i in range(b_size):
        nc[i] = [0]*b_size
    
    for i in range(b_size):
        no = 0
        for j in range(b_size):
            if init_board[j][i] == n:
                no = n
        for j in range(b_size):
            nc[j][i] = no
    return nc

def prepareAllNegConstraint():
    # define constraints based on clues given
    nc = []
    for i in range(last_no):
        nc.append(prepareNegConstraint(i+1))
    # add other general constraints
    # first row constaints
    nc[0][0][3] = 1
    nc[0][0][4] = 1
    nc[1][0][0] = 2
    nc[1][0][4] = 2
    nc[2][0][0] = 3
    nc[2][0][1] = 3
    # last column constraints
    nc[1][1][4] = 2
    nc[2][1][4] = 3
    nc[2][2][4] = 3
    nc[0][4][4] = 1
    
    # center position/cycle constraints
    nc[0][2][2] = 1
    nc[1][2][2] = 2
    
    nc[0][2][1] = 1
    
    return nc
    
    
neg_constraint = prepareAllNegConstraint()

class NoMatchException(Exception):
    pass

def isLoopMatching(g, loop_no, last_seq_no):
    def isLoopFaceMatching(r, last_seq_no, f):
        no_cnt = 0
        for i in r:
            n = f(i)
            if n != 0:
                if n != last_seq_no:
                    raise NoMatchException()
                else:
                    last_seq_no += 1
                    if last_seq_no > last_no:
                        last_seq_no = 1
                    no_cnt += 1
        return last_seq_no
    f = lambda idx: g[loop_no][idx]
    last_seq_no = isLoopFaceMatching(range(loop_no, b_size-loop_no), last_seq_no, f)
    f = lambda idx: g[idx][b_size-loop_no-1]
    last_seq_no = isLoopFaceMatching(range(loop_no+1, b_size-loop_no), last_seq_no, f)
    f = lambda idx: g[b_size-loop_no-1][idx]
    last_seq_no = isLoopFaceMatching(range(b_size-loop_no-2, loop_no-1, -1), last_seq_no, f)
    f = lambda idx: g[idx][loop_no]
    last_seq_no = isLoopFaceMatching(range(b_size-loop_no-2, loop_no, -1), last_seq_no, f)
    return last_seq_no
    
def isMatching(g):
    try:
        seq_no = 1
        for l in range(loop_count):
            seq_no = isLoopMatching(g, l, seq_no)
        if b_size%2 == 1:
            if seq_no == last_no:
                if g[b_size_half][b_size_half] != last_no:
                    return False
            elif seq_no == 1:
                if g[b_size_half][b_size_half] != 0:
                    return False
        return True
    except NoMatchException as e:
        pass
    return False

def isValid(g):
    for i in range(b_size):
        r_sum = 0
        r_prdct = 1
        c_sum = 0
        c_prdct = 1
        for j in range(b_size):
            if g[i][j] > 0:
                r_sum += g[i][j]
                r_prdct *= g[i][j]
            if g[j][i] > 0:
                c_sum += g[j][i]
                c_prdct *= g[j][i]
        if r_sum != b_rc_sum or c_sum != b_rc_sum or r_prdct != b_rc_product or c_prdct != b_rc_product:
            return False
    return True

def generateRowLocation(g, i, j):
    nc = neg_constraint[j-1]
    while True:
        loc = random.randrange(0, b_size)
        if g[i][loc] == 0 and (nc[i][loc] == 0 or nc[i][loc] != j):
             return loc    
    
def generateRandomGrid():
    while True:
        found = True
        g = copy.deepcopy(init_board)
        for i in range(b_size):
            for j in range(1, last_no+1):
                if any(k == j for k in g[i]) == False:
                    loc = generateRowLocation(g, i, j)
                    g[i][loc] = j
        if found:
            return g
    
# iterate through the loop to find solution
cnt = 0
while cnt < 1000000:
    g = generateRandomGrid()
    #print(g)
    if isValid(g):
        print('Valid')
        if isMatching(g):
            print(cnt)
            print(g)
            break
    cnt += 1
    if cnt % 5000 == 0:
        print(cnt)
