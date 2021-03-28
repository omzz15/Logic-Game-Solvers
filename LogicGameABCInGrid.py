# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 10:17:53 2018

@author: gauta
"""
import itertools

n = 'CAABB'
e = 'BCAAA'
s = 'BBBCA'
w = 'CABBB'
g_len = 5
last_idx = g_len-1

def filterCombinations(s, begin_ch, end_ch):
    begin_match = []
    for itm in s:
        for j in range(g_len):
            if itm[j] == ' ':
                continue
            if itm[j] == begin_ch:
                begin_match.append(itm)
            else:
                break
    result = []
    for itm in begin_match:
        for j in range(last_idx, 0, -1):
            if itm[j] == ' ':
                continue
            if itm[j] == end_ch:
                result.append(itm)
            else:
                break            
    return result
    
def generateCombinations():
    arr = ['A', 'B', 'C', ' ', ' ']
    comb = set(itertools.permutations(arr, g_len))
    ns_comb = [None]*g_len
    for i in range(g_len):
        if n[i] != ' ' and s[i] != ' ':
            ns_comb[i] = filterCombinations(comb, n[i], s[i])
    we_comb = [None]*g_len
    for i in range(g_len):
        if w[i] != ' ' and e[i] != ' ':
            we_comb[i] = filterCombinations(comb, w[i], e[i])
    return (ns_comb, we_comb)
    
    
def analyzeAllSideFace(g):
    for i in range(1, last_idx):
        # north face analyzed with each corner values
        if w[0] != ' ' and w[0] == n[i]:
            g[0][i] = '.'
        if e[0] != ' ' and e[0] == n[i]:
            g[0][i] = '.'
        # south face analyzed with each corner values
        if w[last_idx] != ' ' and w[last_idx] == s[i]:
            g[last_idx][i] = '.'
        if e[last_idx] != ' ' and e[last_idx] == s[i]:
            g[last_idx][i] = '.'
        # west face analyzed with each corner values
        if n[0] != ' ' and n[0] == w[i]:
            g[i][0] = '.'
        if s[0] != ' ' and s[0] == w[i]:
            g[i][0] = '.'
        # east face analyzed with each corner values
        if n[last_idx] != ' ' and n[last_idx] == e[i]:
            g[i][last_idx] = '.'
        if s[last_idx] != ' ' and s[last_idx] == e[i]:
            g[i][last_idx] = '.'
    return g
    
    
def getInitGrid():
    g = [None]*g_len
    for i in range(g_len):
        g[i] = [None]*g_len
        for j in range(g_len):
            g[i][j] = ' '
    # set all the corners
    if n[0] != ' ' and w[0] == n[0]:
        g[0][0] = n[0]
    if n[last_idx] != ' ' and e[0] == n[last_idx]:
        g[0][last_idx] = n[last_idx]
    if e[last_idx] != ' ' and s[last_idx] == e[last_idx]:
        g[last_idx][last_idx] = e[last_idx]
    if s[0] != ' ' and s[0] == w[last_idx]:
        g[last_idx][0] = s[0]
    return analyzeAllSideFace(g)

def isValid(g):
    def isGridValid(f):
        for r in range(g_len):
            found_a = False
            found_b = False
            found_c = False
            cnt = 0
            for c in range(g_len):
                ch = f(r, c)
                if ch == 'A':
                    found_a = True
                    cnt += 1
                if ch == 'B':
                    found_b = True
                    cnt += 1
                if ch == 'C':
                    found_c = True
                    cnt += 1
            if cnt != 3 or not (found_a and found_b and found_c):
                return False
        return True
    
    return isGridValid(lambda r, c: g[r][c]) and isGridValid(lambda r, c: g[c][r])

def isMatching(g):
    def isFaceMatching(f, f_ch):
        for i in range(g_len):
            if f_ch[i] != ' ':
                for j in range(g_len):
                    ch = f(i, j)
                    if (ch == 'A' or ch == 'B' or ch == 'C'):
                        if ch != f_ch[i]:
                            return False
                        else:
                            break
        return True
    
    return  isFaceMatching(lambda i, j: g[j][i], n) and             \
            isFaceMatching(lambda i, j: g[last_idx-j][i], s) and    \
            isFaceMatching(lambda i, j: g[i][j], w) and             \
            isFaceMatching(lambda i, j: g[i][last_idx-j], e)
    
def printGrid(g):
    print('  ' + n)
    for i in range(g_len):
        print(w[i] + ' ' + ''.join(g[i]) + ' ' + e[i])
    print('  ' + s)
    
#g = getInitGrid()
#printGrid(g)
(ns_comb, we_comb) = generateCombinations()

for i in ns_comb:
    print(i)
for i in we_comb:
    print(i)




