# CS3243 Introduction to Artificial Intelligence
# Project 2

import sys
import copy


# Running script: given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt

class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle  # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle)  # self.ans is a list of lists
        self.originalDomain = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        self.variables = set()
        for x in range(0, 9):
            for y in range(0, 9):
                self.variables.add((x, y))
        self.assign = Assign()

    def solve(self):
        # TODO: Write your code here

        # self.ans is a list of lists
        return self.ans

    def infer(self, var):
        inference = {}
        varQueue = [var]

        while varQueue.length > 0:
            # while not empty
            y = varQueue.pop(0)

            # for same row constraint
            setOfVarsInConstraints = set()

            # add all vars in same row as y
            for i in range(0, 9):
                setOfVarsInConstraints.add((y[0], i))
            setOfVarsInConstraints.remove(y)

            for x in setOfVarsInConstraints:
                S = self.computeDomain(x)

                for v in S:
                    # rest of the variables in this binary constraint = y
                    yValidDomain = self.computeDomain(y)
                    if len(yValidDomain.difference({v})) == 0:
                        setOfDisallowedValueForX = inference[x]
                        setOfDisallowedValueForX |= {v}
                        inference[x] = setOfDisallowedValueForX

                T = self.computeDomain(x)
                if len(T) == 0:
                    return None
                if T != S:
                    varQueue.append(x)


            # for same col constraint
            setOfVarsInConstraints = set()

            # add all vars in same col as y
            for i in range(0, 9):
                setOfVarsInConstraints.add((i, y[1]))
            setOfVarsInConstraints.remove(y)

            for x in setOfVarsInConstraints:
                S = self.computeDomain(x)

                for v in S:
                    # rest of the variables in this binary constraint = y
                    yValidDomain = self.computeDomain(y)
                    if len(yValidDomain.difference({v})) == 0:
                        setOfDisallowedValueForX = inference[x]
                        setOfDisallowedValueForX |= {v}
                        inference[x] = setOfDisallowedValueForX

                T = self.computeDomain(x)
                if len(T) == 0:
                    return None
                if T != S:
                    varQueue.append(x)


            # for same 3x3 subgrid constraint
            setOfVarsInConstraints = set()

            # add all vars in same 3x3 subgrid as y
            subgridX = y[0] // 3
            subgridY = y[1] // 3

            for i in range(3 * subgridX, 3 * subgridX + 3):
                for j in range(3 * subgridY, 3 * subgridY + 3):
                    setOfVarsInConstraints.add((i, j))
            setOfVarsInConstraints.remove(y)

            for x in setOfVarsInConstraints:
                S = self.computeDomain(x)

                for v in S:
                    # rest of the variables in this binary constraint = y
                    yValidDomain = self.computeDomain(y)
                    if len(yValidDomain.difference({v})) == 0:
                        setOfDisallowedValueForX = inference[x]
                        setOfDisallowedValueForX |= {v}
                        inference[x] = setOfDisallowedValueForX

                T = self.computeDomain(x)
                if len(T) == 0:
                    return None
                if (T != S):
                    varQueue.append(x)

        return inference

    def allVarsAssigned(self):
        for var in self.variables:
            if var not in self.assign.assignment:
                return False

        return True

    def pickUnassignedVar(self):
        # now: pick 1st unassigned var in sequence (0,0), (0,1), (0,2) ...
        # future iteration: use MRV variable
        for var in self.variables:
            if var not in self.assign.assignment:
                return var

    def orderDomainValue(self, var):
        # now: list of values in increasing order
        # future iteration: use most likely to succeed value
        return self.computeDomain(var)

    def computeDomain(self, var):
        if var in self.assign.assignment:
            return {self.assign.assignment[var]}

        cumulativeInference = self.assign.cumulativeInference
        disallowedSetForVar = cumulativeInference[var]
        validDomainSet = self.originalDomain.difference(disallowedSetForVar)
        return validDomainSet

class Assign:
    def __init__(self):
        self.assignment = {}  # dictionary of (x,y) -> value it is assigned
        self.cumulativeInference = {}  # dictionary of (x,y) -> set of values that (x,y) cannot be assigned to (disallowed set)

    def addVarAssignment(self, var, value):
        x = var[0]
        y = var[1]

        self.assignement[(x, y)] = value


    def addNewInference(self, inference):
        # inference is a dictionary of (x,y) -> set of values that (x,y) cannot be assigned to (disallowed set)
        for var, newDisallowedSet in inference.items():
            if var not in self.cumulativeInference:
                self.cumulativeInference[var] = newDisallowedSet
            else:
                # var is already in, so merge set
                cumulativeDisallowedSet = self.cumulativeInference[var]
                cumulativeDisallowedSet |= newDisallowedSet
                # self.cumulativeInference[var] = cumulativeDisallowedSet

    def removeNewInference(self, inference):
        # inference is a dictionary of (x,y) -> set of values that (x,y) cannot be assigned to (disallowed set)
        for var, newDisallowedSet in inference.items():
                cumulativeDisallowedSet = self.cumulativeInference[var]
                newCumulativeDisallowedSet = cumulativeDisallowedSet.difference(newDisallowedSet)
                self.cumulativeInference[var] = newCumulativeDisallowedSet



    # you may add more classes/functions if you think is useful
    # However, ensure all the classes/functions are in this file ONLY
    # Note that our evaluation scripts only call the solve method.
    # Any other methods that you write should be used within the solve() method.


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
