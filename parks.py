# -*- coding: utf-8 -*-
"""
@author: gautam
"""
import random

tree_cnt = 1
park_lay = [[1, 1, 1, 2, 2],
            [1, 2, 2, 2, 3],
            [1, 4, 4, 3, 3],
            [4, 4, 3, 3, 5],
            [4, 5, 5, 5, 5]]

park_row_cnt = len(park_lay)
park_col_cnt = len(park_lay[0])
park_row_r = range(park_row_cnt)
park_col_r = range(park_col_cnt)

EMPTY_CHAR = ' '
UNAVAILABLE_CHAR = '.'
TREE_CHAR = 't'

def init_park_info():
    t = {}
    l = []
    for i in park_row_r:
        for j in park_col_r:
            id = park_lay[i][j]
            if id not in t:
                t[id] = park_ds(id)
                l.append(t[id])
            t[id].add_loc(i, j)
    l.sort(key=lambda pds: pds.size)
    return (t, l)

class park_ds:
    
    def __init__(self, id):
        self.id = id
        self.park_loc = []
        self.tree_loc = []
        
    @property
    def size(self):
        return len(self.park_loc)
    
    def add_loc(self, i, j):
        self.park_loc.append((i, j))
        
    def get_all_available_loc(self, tl):
        if self.is_solved():
            return []
        return list(filter(lambda l: tl[l[0]][l[1]] == EMPTY_CHAR, self.park_loc))
        
    def is_solved(self):
        return len(self.tree_loc) == tree_cnt
        
    def add_tree(self, r, c, tl):
        if self.is_solved():
            raise Exception('Can not add tree at the location ({r}-{c}) in the park ({self.id}) as park is solved')
        if tl[r][c] == TREE_CHAR:
            raise Exception(f'tree already added to the location ({r}-{c}) in the park ({self.id})')
        if tl[r][c] == UNAVAILABLE_CHAR:
            raise Exception(f'can not add tree to the location ({r}-{c}) in the park ({self.id}), as it is marked unavailable')
        for i in park_col_cnt:
            if tl[r][i] == TREE_CHAR:
                return False
                #raise Exception(f'Can not add tree at the location ({r}-{c}) in park ({self.id}), as col ({i}) contains a tree')
        for i in park_row_cnt:
            if tl[i][c] == TREE_CHAR:
                return False
                #raise Exception(f'Can not add tree at the location ({r}-{c}) in park ({self.id}), as row ({i}) contains a tree')
        self.tree_loc.append((r, c))
        tl[r][c] = TREE_CHAR
        if len(self.tree_loc) == tree_cnt:
            for i, j in self.park_loc:
                if tl[i][j] == EMPTY_CHAR:
                    tl[i][j] = UNAVAILABLE_CHAR
            tl[r][i] = UNAVAILABLE_CHAR
        for i in park_col_cnt:
            tl[r][i] = UNAVAILABLE_CHAR
        for i in park_row_cnt:
            tl[i][c] = UNAVAILABLE_CHAR
        return True
        

class solution:
    
    def __init__(self):
        self.park_info_d, self.park_info_l = init_park_info()
        #self.park_content = [[EMPTY_CHAR]*park_col_cnt for i in park_row_r]
    
    def solve_random(self):
        tl = [[EMPTY_CHAR]*park_col_cnt for i in park_row_r]
        for pds in self.park_info_l:
            solved, tl = self.solve_random_park(tl, pds)
            if not solved:
                return self.solve_random()
        if self.is_solved(tl):
            return (True, tl)
        return self.solve_random()
        
    def solve_random_park(self, tl, pds):
        mvs = pds.get_all_available_loc(tl)
        if len(mvs) == 0:
            return (False, tl)
        idx = random.randint(0, len(mvs)-1)
        if pds.add_tree(mvs[idx][0], mvs[idx][1], tl):
            return (True, tl)
        return (False, tl)

    def is_solved(self, tl):
        if not self.validate_row_col(tl): return False
        for pds in self.park_info_l:
            if not pds.is_solved():
                return False
        return True
        
    def validate_row_col(self, tl):
        for i in park_row_r:
            row_tree_found = col_tree_found = False
            for j in park_col_r:
                if tl[i][j]:
                    if row_tree_found: return False
                    row_tree_found = True
                if tl[j][i]:
                    if col_tree_found: return False
                    col_tree_found = True
            if not(row_tree_found and col_tree_found): return False
        return True

sol = solution().solve_random()
print(sol)
