# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 18:53:49 2020

@author: gauta
"""

class logicGame:
    def __init__(self, fillers, counters):
        self.fillers = fillers
        self.counters = counters
        
    def validate(self, **kwargs):
        cnt = kwargs['count']
        for c in self.counters:
            if c.count(**kwargs) >= cnt:
                return False
        return True
    
    def fill(self, **kwargs):
        for f in self.fillers:
            f.fill(**kwargs)
                
class Counter:
    
    def count(self, **kwargs):
        return 0
    
class CountInARow(Counter):
    
    def count(self, **kwargs):
        cnt = 0
        g = kwargs['grid']
        r = kwargs['row']
        ch = kwargs['match_to']
        for i in g[r]:
            if i == ch:
                cnt += 1
        return cnt

class CountInAColumn(Counter):
    
    def count(self, **kwargs):
        cnt = 0
        g = kwargs['grid']
        c = kwargs['column']
        ch = kwargs['match_to']
        for i in range(len(g[0])):
            if g[i][c] == ch:
                cnt += 1
        return cnt

class CountInANeighbor(Counter):
    
    def count(self, **kwargs):
        cnt = 0
        g = kwargs['grid']
        r = kwargs['row']
        c = kwargs['column']
        ch = kwargs['match_to']
        r_len = len(g)
        c_len = len(g[r])
        if r > 0        and g[r-1][c  ] == ch: cnt += 1
        if c > 0        and g[r  ][c-1] == ch: cnt += 1
        if r < r_len-1  and g[r+1][c  ] == ch: cnt += 1
        if c < c_len-1  and g[r  ][c+1] == ch: cnt += 1
        if r > 0 and c > 0                  and g[r-1][c-1] == ch: cnt += 1
        if r > 0 and c < c_len-1            and g[r-1][c+1] == ch: cnt += 1
        if r < r_len-1 and c > 0            and g[r+1][c-1] == ch: cnt += 1
        if r < r_len-1 and c < c_len-1      and g[r+1][c+1] == ch: cnt += 1        
        return cnt
        
class CountInArea(Counter):

    def count(self, **kwargs):
        cnt = 0
        g = kwargs['grid']
        locs = kwargs['locations']
        ch = kwargs['match_to']
        for r, c in locs:
            if g[r][c] == ch: cnt += 1
        return cnt

class Filler:
    
    def fill(self, **kwargs):
        pass
    
class FillInARow(Filler):
    
    def fill(self, **kwargs):
        g = kwargs['grid']
        r = kwargs['row']
        ch = kwargs['match_to']
        rch = kwargs['replace_to']
        for i in range(len(g[r])):
            if g[r][i] == ch:
                g[r][i] = rch

class FillInAColumn(Filler):
    
    def fill(self, **kwargs):
        g = kwargs['grid']
        c = kwargs['column']
        ch = kwargs['match_to']
        rch = kwargs['replace_to']
        for i in range(len(g[0])):
            if g[i][c] == ch:
                g[i][c] = rch

class FillInArea(Filler):

    def fill(self, **kwargs):
        g = kwargs['grid']
        locs = kwargs['locations']
        ch = kwargs['match_to']
        rch = kwargs['replace_to']
        for r, c in locs:
            if g[r][c] == ch: g[r][c] = rch

class FillInANeighbor(Filler):
    
    def fill(self, **kwargs):
        g = kwargs['grid']
        r = kwargs['row']
        c = kwargs['column']
        ch = kwargs['match_to']
        rch = kwargs['replace_to']
        r_len = len(g)
        c_len = len(g[r])
        if r > 0        and g[r-1][c  ] == ch: g[r-1][c  ] = rch
        if c > 0        and g[r  ][c-1] == ch: g[r  ][c-1] = rch
        if r < r_len-1  and g[r+1][c  ] == ch: g[r+1][c  ] = rch
        if c < c_len-1  and g[r  ][c+1] == ch: g[r  ][c+1] = rch
        if r > 0 and c > 0                  and g[r-1][c-1] == ch: g[r-1][c-1] = rch
        if r > 0 and c < c_len-1            and g[r-1][c+1] == ch: g[r-1][c+1] = rch
        if r < r_len-1 and c > 0            and g[r+1][c-1] == ch: g[r+1][c-1] = rch
        if r < r_len-1 and c < c_len-1      and g[r+1][c+1] == ch: g[r+1][c+1] = rch        
