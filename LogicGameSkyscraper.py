import random
import itertools
from functools import reduce

g_len = 4
rc_product = 4*3*2*1
n = [0, 2, 3, 0]
e = [3, 0, 3, 0]
s = [0, 0, 0, 0]
w = [0, 3, 0, 0]
nsum = reduce(lambda x,y: x+y, n)
esum = reduce(lambda x,y: x+y, e)
ssum = reduce(lambda x,y: x+y, s)
wsum = reduce(lambda x,y: x+y, w)

def generateCombination(no):
    result = []
    arr = []
    for i in range(1, g_len+1):
        arr.append(i)
    for l in list(itertools.permutations(arr, g_len)):
        max_no = 0
        max_cnt = 0
        for k in l:
            if k > max_no:
                max_no = k
                max_cnt += 1
        if max_cnt == no:
            result.append(l)
    return result

def generateAllCombination():
    comb = []
    for i in range(g_len):
        c = generateCombination(i+1)
        comb.append(c)
    return comb

def isMatching(g):
    # ensure no of skysraper seen from each direction matches skyscraper lengths in the grid
    for i in range(g_len):
        n_cnt = 0
        n_max_no = 0
        s_cnt = 0
        s_max_no = 0
        e_cnt = 0
        e_max_no = 0
        w_cnt = 0
        w_max_no = 0
        for j in range(g_len):
            if g[j][i] > n_max_no:
                n_max_no = g[j][i]
                n_cnt += 1
            if g[g_len-j-1][i] > s_max_no:
                s_max_no = g[g_len-j-1][i]
                s_cnt += 1
            if g[i][j] > w_max_no:
                w_max_no = g[i][j]
                w_cnt += 1
            if g[i][g_len-j-1] > e_max_no:
                e_max_no = g[i][g_len-j-1]
                e_cnt += 1
        if n[i] != 0:
            if n_cnt != n[i]:
                return False
        if s[i] != 0:
            if s_cnt != s[i]:
                return False
        if e[i] != 0:
            if e_cnt != e[i]:
                return False
        if w[i] != 0:
            if w_cnt != w[i]:
                return False
    # if all conditions passed, then it's a matching grid
    return True

def isValid(g):
    # ensure each row and column is composed of unique nos.. 1..n
    for i in range(g_len):
        r_prdct = 1
        c_prdct = 1
        for j in range(g_len):
            r_prdct *= g[i][j]
            c_prdct *= g[j][i]
        if r_prdct != rc_product or c_prdct != rc_product:
            return False
    return True

def generateRandomGrid(g, comb):
    # reset the grid to all 0
    for i in range(g_len):
        for j in range(g_len):
            g[i][j] = 0
            g[j][i] = 0
    
    # generate random grid
    for i in range(g_len):
        if e[i] == 0:
            if w[i] == 0:
                for j in range(g_len):
                    while True:
                        loc = random.randrange(0, g_len)
                        if g[i][loc] == 0:
                            g[i][loc] = j+1
                            break
            else:
                c = comb[w[i]-1]
                sc = c[random.randrange(0, len(c))]
                #print(sc)
                for j in range(g_len):
                    g[i][j] = sc[j]
        else:
            c = comb[e[i]-1]
            sc = c[random.randrange(0, len(c))]
            #print(sc)
            for j in range(g_len):
                g[i][g_len-j-1] = sc[j]
    return g

# initialize the grid
g = [0]*g_len
for i in range(g_len):
    g[i] = [0]*g_len

# initialize all combinations
comb = generateAllCombination()

# iterate through the loop to find solution
cnt = 0
while cnt < 100000:
    g = generateRandomGrid(g, comb)
    #print(g)
    if isValid(g):
        print('Valid')
        if isMatching(g):
            print(cnt)
            print(g)
            break
    cnt += 1
    if cnt % 100 == 0:
        print(cnt)

