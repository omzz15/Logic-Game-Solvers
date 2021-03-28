class SudokuCell:
    def __init__(self):
        self.value = None
        self.evaluate_groups = False
        self.groups = []
        self.possible_values = []
        for i in range(1, 10):
            self.possible_values.append(i)
    
    def setValue(self, value):
        self.value = value
        self.possible_values = []
        self.evaluate_groups = True

    def addGroup(self, group):
        self.groups.append(group)

class SudokuCellGroup:
    def __init__(self):
        self.group = []

class Sudoku:
    def __init__(self):
        self.cells = [None]*10
        for i in range(1, 10):
            self.cells[i] = [None]*10
            for j in range(1, 10):
                self.cells[i][j] = SudokuCell()
        self.groups = []
        for r in range(1, 10):
            rg = SudokuCellGroup()
            cg = SudokuCellGroup()
            for c in range(1, 10):
                self.cells[r][c].addGroup(rg)
                self.cells[c][r].addGroup(cg)
            self.groups.append(rg)
            self.groups.append(cg)
        for i in range(1, 10):
            g = SudokuCellGroup()
            r_inc = 0
            c_inc = 0
            for r in range(1, 4):
                for c in range(1, 4):
                    self.cells[r+r_inc][c+c_inc].addGroup(g)
            self.groups.append(g)
            c_inc += 3
            if c_inc > 6:
                r_inc += 3
                c_inc = 0

s = Sudoku()
print(s)

                
        