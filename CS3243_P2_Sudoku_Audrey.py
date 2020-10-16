# CS3243 Introduction to Artificial Intelligence
# Project 2 Group 23
# Audrey Felicio Anwar & Wang Jun Hao

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
        self.domain = [[set(i for i in range(1,10)) for _ in range(9)] for _ in range(9)]

    def solve(self):
        # TODO: Write your code here
        start = time.time()
        assignment = {}
        self.preprocess(assignment)
        self.backtrack_search(assignment)
        self.assign_the_assignment(assignment)
        print(time.time() - start)
        return self.puzzle

    # you may add more classes/functions if you think is useful
    # However, ensure all the classes/functions are in this file ONLY
    # Note that our evaluation scripts only call the solve method.
    # Any other methods that you write should be used within the solve() method.

    def assign_the_assignment(self, assignment):
        for i in range(0, 9):
            for j in range(0, 9):
                if self.puzzle[i][j] == 0:
                    self.puzzle[i][j] = assignment[(i, j)]


    def preprocess(self, assignment):
        for i in range(0, 9):
            for j in range(0, 9):
                curr = self.puzzle[i][j]
                assignment[(i, j)] = curr
                if curr != 0:
                    self.domain[i][j] = set([curr])
                    for k in range(0, 9):
                        if k != i:
                            self.domain[k][j].discard(curr)
                        if k != j:
                            self.domain[i][k].discard(curr)
                    translated_i = i // 3 * 3
                    translated_j = j // 3 * 3
                    for x in range(0, 3):
                        for y in range(0, 3):
                            if x + translated_i != i and y + translated_j != j:
                                self.domain[x + translated_i][y + translated_j].discard(curr)

    def pick_unassigned_var(self, assignment):
        # with MRV heuristic
        length = 9
        var = ()
        for i in range(0, 9):
            for j in range(0, 9):
                if assignment[(i, j)] == 0:
                    curr_length = len(self.domain[i][j])
                    if curr_length <= length:
                        length = curr_length
                        var = (i, j)
        return var

    def is_complete(self, assignment):
        for i in range(0, 9):
            for j in range(0, 9):
                if assignment[(i, j)] == 0:
                    return False
        return True

    def is_consistent(self, value, x, y, assignment):
        for k in range(0, 9):
            if k != x and value == assignment[(k, y)]:
                return False
            if k != y and value == assignment[(x, k)]:
                return False
        
        translated_x = x // 3 * 3
        translated_y = y // 3 * 3
        for i in range(0, 3):
            for j in range(0, 3):
                new_x = i + translated_x
                new_y = j + translated_y
                if new_x != x and new_y != y and value == assignment[(new_x, new_y)]:
                    return False
        
        return True

    def backtrack_search(self, assignment):
        if self.is_complete(assignment):
            return True
        x, y = self.pick_unassigned_var(assignment)
        for value in self.domain[x][y]:
            if self.is_consistent(value, x, y, assignment):
                assignment[(x, y)] = value
                result = self.backtrack_search(assignment)
                if result != False:
                    return result
                assignment[(x, y)] = 0
        
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
