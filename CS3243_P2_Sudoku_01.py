# CS3243 Introduction to Artificial Intelligence
# Project 2

import sys
import copy
import time

# Running script: given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt

class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists
        self.inference = {} #(row, col) : [unallowed values]

    def solve(self):
        # TODO: Write your code here
        start = time.time()
        for i in range(0, 9):
            for j in range(0, 9):
                var = (i, j)
                self.inference[var] = []
        
        for i in range(0, 9):
            for j in range(0, 9):
                if self.puzzle[i][j] != 0:
                    var = (i, j)
                    self.forward_check(self.puzzle, var)

        self.backtrack_search(self.puzzle)
        
        # self.ans is a list of lists
        print(time.time() - start)
        return self.puzzle

    # you may add more classes/functions if you think is useful
    # However, ensure all the classes/functions are in this file ONLY
    # Note that our evaluation scripts only call the solve method.
    # Any other methods that you write should be used within the solve() method.

    def check_if_all_exists(self, list):
        for i in range(1, 10):
            if i not in list:
                return False
        return True

    def computeDomain(self, puzzle, var):
        domain = []
        for i in range(1, 10):
            if i not in self.inference[var]:
                domain.append(i)
        return domain

    def forward_check(self, puzzle, var):
        x = var[0]
        y = var[1]
        curr = puzzle[x][y]

        # row and column
        for i in range(0, 9):
            if i != x:
                self.inference[(i, y)].append(curr)
            if i != y:
                self.inference[(x, i)].append(curr)

        # grid
        translate_x = x // 3 * 3
        translate_y = y // 3 * 3
        for i in range(0, 3):
            for j in range(0, 3):
                if (translate_x + i) != x and (translate_y + j) != y:
                    self.inference[(translate_x + i, translate_y + j)].append(curr)


        
        if self.check_if_all_exists(self.inference[var]):
            return False
        else:
            return True
    
    def remove_false_infer(self, puzzle, var):
        x = var[0]
        y = var[1]
        curr = puzzle[x][y]

        # row and column
        for i in range(0, 9):
            if i != x:
                self.inference[(i, y)].remove(curr)
            if i != y:
                self.inference[(x, i)].remove(curr)

        # grid
        translate_x = x // 3 * 3
        translate_y = y // 3 * 3
        for i in range(0, 3):
            for j in range(0, 3):
                if (translate_x + i) != x and (translate_y + j) != y:
                    self.inference[(translate_x + i, translate_y + j)].remove(curr)


    def backtrack_search(self, puzzle):
        var = ()
        found = False
        for i in range(0, 9):
            for j in range(0, 9):
                if puzzle[i][j] == 0:
                    var = (i, j)
                    found = True
                    break
            if found:
                break

        if not found:
            return self.check_valid(puzzle)
        
        for i in range(1, 10):
            if i not in self.inference[var]:
                puzzle[var[0]][var[1]] = i
                inference = self.forward_check(puzzle, var)
                if inference != False:
                    result = self.backtrack_search(puzzle)
                    if result != False:
                        return result
                self.remove_false_infer(puzzle, var)
                puzzle[var[0]][var[1]] = 0

        return False              
    
    def check_valid(self, puzzle):
        for i in range(0, 9):
            visited = set()
            row = puzzle[i]
            for j in row:
                if j in visited:
                    return False
                else:
                    visited.add(j)
        
        for i in range(0, 9):
            visited = set()
            for j in range(0, 9):
                current = puzzle[j][i]
                if current in visited:
                    return False
                else:
                    visited.add(current)

        for k in range(0, 3):
            for l in range(0, 3):
                visited = set()
                for i in range(3 * k, 3 * k + 3):
                    for j in range(3 * l, 3 * l + 3):
                        current = puzzle[i][j]
                        if current in visited:
                            return False
                        else:
                            visited.add(current)
        
        return True

if __name__ == "__main__":
    # STRICTLY do NOT modify the code in the main function here
    if len(sys.argv) != 3:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise IOError("Input file not found!")

    puzzle = [[0 for i in range(9)] for j in range(9)]
    lines = f.readlines()

    i, j = 0, 0
    for line in lines:
        for number in line:
            if '0' <= number <= '9':
                puzzle[i][j] = int(number)
                j += 1
                if j == 9:
                    i += 1
                    j = 0

    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()

    with open(sys.argv[2], 'a') as f:
        for i in range(9):
            for j in range(9):
                f.write(str(ans[i][j]) + " ")
            f.write("\n")
