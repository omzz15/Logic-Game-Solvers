# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 09:33:58 2020

@author: q774283
"""
import random
import itertools
import copy

grid_size = 4
grange = range(grid_size)
col_sum = [17,21,18, 4]
row_sum = [17,14,20, 9]
board = [
    '..00',
    '...0',
    '0...',
    '00..'
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
            mat_cmbs[r][c] = []
            if b[r][c] == 0: continue
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
                        pass
                        #print(f'{r}-{c} : {lpi} - {lni}')
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

def is_filled(b):
    for r in grange:
        for c in grange:
            if b[r][c] == None:
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
    
def get_sorted_comb_list(b, mcmbs):
    sl = []
    for r in grange:
        for c in grange:
            if b[r][c] == 0 or len(mcmbs[r][c]) == 0: continue
            sl.append((r, c, len(mcmbs[r][c])))
    #print(sl)
    return sorted(sl, key=lambda item: item[2])
    
def get_valid_choice(b, mcmbs):
    sl = get_sorted_comb_list(b, mcmbs)
    r, c, rc_choice_len = sl[0]
    #print(f'{r} - {c} : {rc_choice_len}')
    valid_choice_l = []
    for achoice in mcmbs[r][c]:
        is_valid_choice = True
        for i in grange:
            if b[r][i] != None and b[r][i] != achoice[0][i]:
                is_valid_choice = False
                break
            if b[i][c] != None and b[i][c] != achoice[1][i]:
                is_valid_choice = False
                break
        if is_valid_choice:
            for i in grange:
                if b[r][i] != 0 and len(mcmbs[r][i]) > 0:
                    fl = list(filter(lambda item: item[0] == achoice[0], mcmbs[r][i]))
                    if len(fl) == 0:
                        is_valid_choice = False
                        break
                if b[i][c] != 0 and len(mcmbs[i][c]) > 0:
                    fl = list(filter(lambda item: item[1] == achoice[1], mcmbs[i][c]))
                    if len(fl) == 0:
                        is_valid_choice = False
                        break
        if is_valid_choice:
            valid_choice_l.append(achoice)
    if len(valid_choice_l) == 0:
        return (None, None, None)
    else:
        return (r, c, random.choice(valid_choice_l))
    
def solve():
    itr = 1000000
    b = get_board()
    mcmbs = get_matching_combinations(b)
    while itr > 0:
        success, newb = solve_itr(copy.deepcopy(b), copy.deepcopy(mcmbs))
        if success:
            return newb
        itr -= 1
        print(itr)
        #input()
    return None

def solve_itr(b, mcmbs):
    if is_solved(b, row_sum, col_sum): return (True, b)
    if is_filled(b): return (False, b)
    r, c, achoice = get_valid_choice(b, mcmbs)
    if r == None or c == None or achoice == None:
        return (False, b)
    mcmbs[r][c] = list()
    for i in grange:
        b[r][i] = achoice[0][i]
        mcmbs[r][i] = list(filter(lambda item: item[0] == achoice[0], mcmbs[r][i]))
        b[i][c] = achoice[1][i]
        mcmbs[i][c] = list(filter(lambda item: item[1] == achoice[1], mcmbs[i][c]))
    #print(b)
    #input()
    return solve_itr(b, mcmbs)

sol = solve()
print(sol)
