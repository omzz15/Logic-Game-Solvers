# -*- coding: utf-8 -*-
"""
@author: gautam
"""
import random
import game_common

tree_cnt = 2
park_lay = [[1, 2, 2, 2, 2, 3, 3, 3],
            [1, 2, 2, 3, 3, 3, 3, 3],
            [1, 2, 2, 3, 4, 3, 3, 3],
            [1, 1, 4, 4, 4, 5, 5, 5],
            [1, 4, 4, 4, 6, 5, 7, 5],
            [1, 8, 4, 6, 6, 5, 7, 5],
            [8, 8, 8, 6, 6, 6, 7, 7],
            [8, 8, 7, 7, 7, 7, 7, 7]]

def get_park_content():
    tl = [[EMPTY_CHAR]*park_col_cnt for i in park_row_r]
    return tl

class park_game(game_common.logicGame):
    
    def __init__(self):
        counters = [
            game_common.CountInARow(),
            game_common.CountInAColumn(),
            game_common.CountInANeighbor(),
            game_common.CountInArea()
        ]
        fillers = [
            game_common.FillInARow(),
            game_common.FillInAColumn(),
            game_common.FillInArea(),
            game_common.FillInANeighbor()
            ]
        super().__init__(fillers, counters)
        
    def validate(self, g, r, c, locs):
        args = {'grid': g, 'row': r, 'column': c, 'match_to': TREE_CHAR, 'locations': locs, 'count': tree_cnt}
        return super().validate(**args)
    
    def fill(self, g, r, c, locs):
        args = {'grid': g, 'row': r, 'column': c, 'locations': locs,
                'match_to': EMPTY_CHAR, 'replace_to': UNAVAILABLE_CHAR}
        super().fill(**args)
    
    def init_park_info(self):
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
    
    def print(self, g):
        if g == None: return
        for r in park_col_r:
            print(g[r])

pg = park_game()

park_row_cnt = len(park_lay)
park_col_cnt = len(park_lay[0])
park_row_r = range(park_row_cnt)
park_col_r = range(park_col_cnt)

EMPTY_CHAR = ' '
UNAVAILABLE_CHAR = '.'
TREE_CHAR = 't'

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
        if not pg.validate(tl, r, c, self.park_loc):
            return False
        self.tree_loc.append((r, c))
        tl[r][c] = TREE_CHAR
        pg.fill(tl, r, c, self.park_loc)
        return True
        

class solution:
    
    def __init__(self):
        self.iterations = 5000
        pass
    
    def solve_random(self):
        self.iterations -= 1
        if self.iterations == 0: return (False, None)
        #input('move to next random?')
        park_info_d, park_info_l = pg.init_park_info()
        tl = get_park_content()
        for pds in park_info_l:
            solved, tl = self.solve_random_park(tl, pds)
            if not solved:
                return self.solve_random()
        if self.is_solved(tl, park_info_l):
            return (True, tl)
        return self.solve_random()
        
    def solve_random_park(self, tl, pds):
        mvs = pds.get_all_available_loc(tl)
        #print(f'{pds.id} - {mvs}')
        if len(mvs) == 0:
            return (False, tl)
        idx = random.randint(0, len(mvs)-1)
        is_success = False
        if pds.add_tree(mvs[idx][0], mvs[idx][1], tl):
            is_success = True
        #pg.print(tl)
        #input('move to next park?')
        return (is_success, tl)

    def is_solved(self, tl, park_info_l):
        if not self.validate_row_col(tl): return False
        for pds in park_info_l:
            if not pds.is_solved():
                return False
        return True
        
    def validate_row_col(self, tl):
        for i in park_row_r:
            row_tree_found = col_tree_found = False
            for j in park_col_r:
                if tl[i][j] == TREE_CHAR:
                    if row_tree_found: return False
                    row_tree_found = True
                if tl[j][i] == TREE_CHAR:
                    if col_tree_found: return False
                    col_tree_found = True
            if not(row_tree_found and col_tree_found): return False
        return True

sol = solution().solve_random()
pg.print(sol[1])
