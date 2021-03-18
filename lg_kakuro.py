# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 09:33:58 2020

@author: q774283
"""
import random
import itertools

grid_size = 4
grange = range(grid_size)
row_sum = [12,24, 7, 6]
col_sum = [17,15,13, 4]
board = [
    '...0',
    '...0',
    '0...',
    '0...'
]

def plugin_to_row(l, r):
    ol = []
    lcnt = 0
    for c in grange:
        if board[r][c] == '0':
            ol.append(0)
        else:
            ol.append(l[lcnt])
            lcnt += 1
    return ol

def plugin_to_col(l, c):
    ol = []
    lcnt = 0
    for r in grange:
        if board[r][c] == '0':
            ol.append(0)
        else:
            ol.append(l[lcnt])
            lcnt += 1
    return ol
    
def get_board():
    b = [[None]*grid_size for _ in grange]
    for r in grange:
        for c in grange:
            if board[r][c] == '0':
                b[r][c] = 0
    return b

def get_row_combination(b, r, rt):
    rcmb = []
    rcnt = grid_size
    for i in grange:
        if b[r][i] == 0: 
            rcnt -= 1
    for p in itertools.permutations(range(1,10), rcnt):
        if sum(p) == rt:
            rcmb.append(plugin_to_row(p, r))
    return rcmb

def get_col_combination(b, c, ct):
    ccmb = []
    ccnt = grid_size
    for i in grange:
        if b[i][c] == 0: 
            ccnt -= 1
    for p in itertools.permutations(range(1,10), ccnt):
        if sum(p) == ct:
            ccmb.append(plugin_to_col(p, c))
    return ccmb

def get_combinations(b):
    rcmb = [None]*grid_size
    ccmb = [None]*grid_size
    for i in grange:
        rcmb[i] = get_row_combination(b, i, row_sum[i])
        ccmb[i] = get_col_combination(b, i, col_sum[i])
    return (rcmb, ccmb)

def get_matching_combinations(b):
    rcmb, ccmb = get_combinations(b)
    mat_cmbs = [[None]*grid_size for _ in grange]
    for r in grange:
        for c in grange:
            if b[r][c] == 0: continue
            mat_cmbs[r][c] = []
            for rc, cc in itertools.product(rcmb[r], ccmb[c]):
                if rc[c] == cc[r]:
                    mat_cmbs[r][c].append((rc, cc))
    for r in grange:
        for c in grange:
            if r == 0 or c == 0 or b[r][c] == 0: continue
            lp = mat_cmbs[r][c-1]
            ln = mat_cmbs[r][c]
            if lp == None or ln == None: continue
            for lpi in lp:
                for lni in ln:
                    if lpi[0] == lni[0]:
                        print(f'{r}-{c} : {lpi} - {lni}')
    return mat_cmbs
    
def is_solved(b, rsum, csum):
    for r in grange:
        rsum = 0
        csum = 0
        for c in grange:
            if b[r][c] == None or b[c][r] == None: return False
            csum += b[c][r]
            rsum += b[r][c]
        if rsum != row_sum[r] or csum != col_sum[r]:
            return False
    return True

def get_empty_loc(b):
    for r in grange:
        for c in grange:
            if b[r][c] == None:
                return (r, c)
    return (None, None)
    
def get_possible_value(b, r, c, rsum, csum):
    pv = [1,2,3,4,5,6,7,8,9]
    for i in grange:
        if b[i][c] in pv and b[i][c] > csum[i]:
            pv.remove(b[i][c])
        if b[r][i] in pv and b[r][i] > rsum[i]:
            pv.remove(b[r][i])
    return pv
    
def solve():
    itr = 1000000
    while itr > 0:
        b = get_board()
        success, newb = solve_itr(b, row_sum.copy(), col_sum.copy())
        if success:
            return newb
        itr -= 1
        print(itr)
    return None

def solve_itr(b, rsum, csum):
    if is_solved(b, rsum, csum): return (True, b)
    r, c = get_empty_loc(b)
    if r == None or c == None: return (False, b)
    pv = get_possible_value(b, r, c, rsum, csum)
    if len(pv) == 0: return (False, b)
    val = random.choice(pv)
    b[r][c] = val
    rsum[r] -= val
    csum[c] -= val
    if rsum[r] < 0 or csum[c] < 0: return (False, b)
    return solve_itr(b, rsum, csum)

b = get_board()
mcmbs = get_matching_combinations(b)
