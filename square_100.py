# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 13:48:44 2020

@author: q774283
"""
import itertools

grid_2_solve = [[1,8,2],[8,9,8],[7,4,5]]

def get_num_comb():
    num_comb_l = [set() for _ in range(100)]
    for i in range(1, 100):
        for j in range(1, 100):
            for k in range(1, 100):
                if i+j+k == 100:
                    val = order_triplet(i, j, k)
                    mi, ot, ma = val
                    num_comb_l[mi].add(val)
                    num_comb_l[ot].add(val)
                    num_comb_l[ma].add(val)
    return num_comb_l

def order_triplet(i, j, k):
    mi, ma = min(i, j, k), max(i, j, k)
    ot = j
    if (mi == i or mi == j) and (ma == i or ma == j):
        ot = k
    if (mi == k or mi == j) and (ma == k or ma == j):
        ot = i
    return (mi, ot, ma)

def break_num_digit(i):
    if i < 10: return [i]
    if i%11 == 0: return [i%10]
    return [i%10, i//10]

def get_digit_triplet(i, j, k):
    il = break_num_digit(i)
    jl = break_num_digit(j)
    kl = break_num_digit(k)
    return itertools.product(il, jl, kl)

def get_digit_comb():
    digit_comb = {}
    num_comb_l = get_num_comb()
    for num_comb in num_comb_l:
        if len(num_comb) == 0: continue
        for val in num_comb:
            i, j, k = val
            for t in get_digit_triplet(i, j, k):
                if t not in digit_comb: digit_comb[t] = set()
                digit_comb[t].add(val)
    return digit_comb

def get_match(digit_comb, i, j, k):
    mdc = set()
    if (i,j,k) in digit_comb:
        for dc in digit_comb[(i,j,k)]:
            mdc.add(dc)
    if (j,i,k) in digit_comb:
        for dc in digit_comb[(j,i,k)]:
            mdc.add((dc[1], dc[0], dc[2]))
    if (k,j,i) in digit_comb:
        for dc in digit_comb[(k,j,i)]:
            mdc.add((dc[2], dc[1], dc[0]))
    if (i,k,j) in digit_comb:
        for dc in digit_comb[(i,k,j)]:
            mdc.add((dc[0], dc[2], dc[1]))
    if (j,k,i) in digit_comb:
        for dc in digit_comb[(j,k,i)]:
            mdc.add((dc[2], dc[0], dc[1]))
    if (k,i,j) in digit_comb:
        for dc in digit_comb[(k,i,j)]:
            mdc.add((dc[1], dc[2], dc[0]))
    return mdc
    
def get_grid_loc_match(digit_comb, grid, gr, gc):
    rc_match = []
    row_match = get_match(digit_comb, grid[gr][0], grid[gr][1], grid[gr][2])
    col_match = get_match(digit_comb, grid[0][gc], grid[1][gc], grid[2][gc])
    for ri in row_match:
        for cj in col_match:
            if ri[gc] == cj[gr]:
                mat_g = [None]*9
                mat_g[gr*3+0], mat_g[gr*3+1], mat_g[gr*3+2] = ri[0], ri[1], ri[2]
                mat_g[0*3+gc], mat_g[1*3+gc], mat_g[2*3+gc] = cj[0], cj[1], cj[2]                
                rc_match.append(mat_g)
    return rc_match

def merge_grid(g1, g2):
    mer_g = [None]*9
    for i in range(9):
        if g1[i] and g2[i]:
            if g1[i] != g2[i]:
                return (False, None)
            mer_g[i] = g1[i]
        elif g1[i]:
            mer_g[i] = g1[i]
        elif g2[i]:
            mer_g[i] = g2[i]
    return (True, mer_g)

def merge_grid_loc_match(g1m_l, g2m_l):
    mer_g_l = []
    for g1 in g1m_l:
        for g2 in g2m_l:
            success, mer_g = merge_grid(g1, g2)
            if success:
                mer_g_l.append(mer_g)
    return mer_g_l

def is_valid(g):
    for i in range(9):
        if not g[i]: return False
    if g[0]+g[1]+g[2] != 100: return False
    if g[3]+g[4]+g[5] != 100: return False
    if g[6]+g[7]+g[8] != 100: return False
    if g[0]+g[3]+g[6] != 100: return False
    if g[1]+g[4]+g[7] != 100: return False
    if g[2]+g[5]+g[8] != 100: return False
    return True

digit_comb = get_digit_comb()
all_choices = get_grid_loc_match(digit_comb, grid_2_solve, 0, 0)
cell_choices = get_grid_loc_match(digit_comb, grid_2_solve, 0, 1)
all_choices = merge_grid_loc_match(all_choices, cell_choices)
cell_choices = get_grid_loc_match(digit_comb, grid_2_solve, 0, 2)
all_choices = merge_grid_loc_match(all_choices, cell_choices)
# filter out the ones that do not add to 100
for m in filter(is_valid, all_choices):
    print(m)
