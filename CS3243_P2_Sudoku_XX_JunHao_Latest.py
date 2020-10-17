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
        self.assign = Assign()
        self.constraintRow = [[], [], [], [], [], [], [], [], []]
        self.constraintCol = [[], [], [], [], [], [], [], [], []]
        self.constraintSubGrid = [[], [], [], [], [], [], [], [], []]
        # 0 1 2
        # 3 4 5
        # 6 7 8
        for row in range(0, 9):
            for col in range(0, 9):
                self.variables.add((row, col))
                if puzzle[row][col] != 0:
                    val = puzzle[row][col]
                    self.assign.addVarAssignment((row, col), val)
                    self.constraintRow[row].append(val)
                    self.constraintCol[col].append(val)
                    subgridRow = row // 3
                    subgridCol = col // 3
                    subGridIndex = subgridRow + 3 * subgridCol
                    self.constraintSubGrid[subGridIndex].append(val)

    def solve(self):
        # TODO: Write your code here
        resultingAssign = self.backtrackSearchWithInference()

        resultingAssignment = resultingAssign.assignment

        for var, value in resultingAssignment.items():
            row = var[0]
            col = var[1]
            self.ans[row][col] = value

        # self.ans is a list of lists
        return self.ans

    def backtrackSearchWithInference(self):
        if self.allVarsAssigned():
            return self.assign

        var = self.pickUnassignedVar()

        for value in self.orderDomainValue(var):
            # check if value is consistent with the assignment
            if self.isConsistent(var, value):
                self.assign.addVarAssignment(var, value)

                row = var[0]
                col = var[1]
                self.constraintRow[row].append(value)
                self.constraintCol[col].append(value)
                subgridRow = row // 3
                subgridCol = col // 3
                subGridIndex = subgridRow + 3 * subgridCol
                self.constraintSubGrid[subGridIndex].append(value)

                inference = self.infer(var)
                self.assign.addNewInference(inference)

                if inference is not None:
                    result = self.backtrackSearchWithInference()

                    if result is not None:
                        return result

                self.assign.removeVarAssignment(var)

                self.constraintRow[row].remove(value)
                self.constraintCol[col].remove(value)
                self.constraintSubGrid[subGridIndex].remove(value)

                self.assign.removeNewInference(inference)

        return None

    def isConsistent(self, newVar, newValue):
        row = newVar[0]
        col = newVar[1]
        if newValue in self.constraintRow[row]:
            return False
        if newValue in self.constraintCol[col]:
            return False

        subgridRow = row // 3
        subgridCol = col // 3
        subGridIndex = subgridRow + 3 * subgridCol
        if newValue in self.constraintSubGrid[subGridIndex]:
            return False

        return True



    def infer(self, var):
        inference = {}
        varQueue = [var]

        while len(varQueue) > 0:
            # while not empty
            y = varQueue.pop(0)

            # for same row constraint
            setOfVarsInConstraints = set()

            # add all vars in same row as y
            for i in range(0, 9):
                setOfVarsInConstraints.add((y[0], i))
            setOfVarsInConstraints.remove(y)

            for x in setOfVarsInConstraints:
                S = self.computeDomainForInfer(x, inference)

                for v in S:
                    # rest of the variables in this binary constraint = y
                    yValidDomain = self.computeDomainForInfer(y, inference)
                    if len(yValidDomain.difference({v})) == 0:
                        if x not in inference:
                            inference[x] = set()
                        setOfDisallowedValueForX = inference[x]
                        setOfDisallowedValueForX |= {v}
                        inference[x] = setOfDisallowedValueForX

                T = self.computeDomainForInfer(x, inference)
                if len(T) == 0:
                    return None
                #if T != S and len(T) == 1:
                #    if x not in varQueue:
                #        varQueue.append(x)


            # for same col constraint
            setOfVarsInConstraints = set()

            # add all vars in same col as y
            for i in range(0, 9):
                setOfVarsInConstraints.add((i, y[1]))
            setOfVarsInConstraints.remove(y)

            for x in setOfVarsInConstraints:
                S = self.computeDomainForInfer(x, inference)

                for v in S:
                    # rest of the variables in this binary constraint = y
                    yValidDomain = self.computeDomainForInfer(y, inference)
                    if len(yValidDomain.difference({v})) == 0:
                        if x not in inference:
                            inference[x] = set()
                        setOfDisallowedValueForX = inference[x]
                        setOfDisallowedValueForX |= {v}
                        inference[x] = setOfDisallowedValueForX

                T = self.computeDomainForInfer(x, inference)
                if len(T) == 0:
                    return None
                #if T != S and len(T) == 1:
                #    if x not in varQueue:
                #        varQueue.append(x)


            # for same 3x3 subgrid constraint
            setOfVarsInConstraints = set()

            # add all vars in same 3x3 subgrid as y
            subgridRow = y[0] // 3
            subgridCol = y[1] // 3

            for i in range(3 * subgridRow, 3 * subgridRow + 3):
                for j in range(3 * subgridCol, 3 * subgridCol + 3):
                    setOfVarsInConstraints.add((i, j))
            setOfVarsInConstraints.remove(y)

            for x in setOfVarsInConstraints:
                S = self.computeDomainForInfer(x, inference)

                for v in S:
                    # rest of the variables in this binary constraint = y
                    yValidDomain = self.computeDomainForInfer(y, inference)
                    if len(yValidDomain.difference({v})) == 0:
                        if x not in inference:
                            inference[x] = set()
                        setOfDisallowedValueForX = inference[x]
                        setOfDisallowedValueForX |= {v}
                        inference[x] = setOfDisallowedValueForX

                T = self.computeDomainForInfer(x, inference)
                if len(T) == 0:
                    return None
                #if T != S and len(T) == 1:
                #    if x not in varQueue:
                #        varQueue.append(x)

        return inference

    def allVarsAssigned(self):
        return len(self.assign.assignment) == 81


    def pickUnassignedVar(self):
        # now: pick 1st unassigned var in sequence (0,0), (0,1), (0,2) ...
        # future iteration: use MRV variable

        # minVar = None
        # MRV = 10
        # for i in range(0, 9):
        #     for j in range(0, 9):
        #         if (i, j) not in self.assign.assignment:
        #             if len(self.computeDomain((i, j))) < MRV:
        #                 minVar = (i, j)
        #
        # if minVar is None:
        #     print("fuck")
        # return minVar

        for i in range(0, 9):
            for j in range(0, 9):
                if (i, j) not in self.assign.assignment:
                    return (i, j)

    def orderDomainValue(self, var):
        # now: list of values in increasing order
        # future iteration: use most likely to succeed value
        list = []
        for val in range(1, 10):
            if val in self.computeDomain(var):
                list.append(val)
        return list
        #return self.computeDomain(var)

    def computeDomain(self, var):
        if var in self.assign.assignment:
            return {self.assign.assignment[var]}

        cumulativeInference = self.assign.cumulativeInference
        if var not in cumulativeInference:
            return self.originalDomain

        disallowedSetForVar = cumulativeInference[var]
        validDomainSet = self.originalDomain.difference(disallowedSetForVar)
        return validDomainSet

    def computeDomainForInfer(self, var, newInference):
        if var in self.assign.assignment:
            return {self.assign.assignment[var]}

        cumulativeInference = self.assign.cumulativeInference
        if var not in cumulativeInference:
            if var not in newInference:
                return self.originalDomain
            else:
                return self.originalDomain.difference(newInference[var])
        else:
            currentDomain = self.originalDomain.difference(cumulativeInference[var])
            if var not in newInference:
                return currentDomain
            else:
                return currentDomain.difference(newInference[var])

class Assign:
    def __init__(self):
        self.assignment = {}  # dictionary of (row, col) -> value it is assigned
        self.cumulativeInference = {}  # dictionary of (row, col) -> set of values that (row, col) cannot be assigned to (disallowed set)

    def addVarAssignment(self, var, value):
        self.assignment[var] = value

    def removeVarAssignment(self, var):
        self.assignment.pop(var, None)


    def addNewInference(self, inference):
        if inference is not None:
            # inference is a dictionary of (row, col) -> set of values that (row, col) cannot be assigned to (disallowed set)
            for var, newDisallowedSet in inference.items():
                if var not in self.cumulativeInference:
                    self.cumulativeInference[var] = newDisallowedSet
                else:
                    # var is already in, so merge set
                    cumulativeDisallowedSet = self.cumulativeInference[var]
                    cumulativeDisallowedSet |= newDisallowedSet
                    # self.cumulativeInference[var] = cumulativeDisallowedSet

    def removeNewInference(self, inference):
        if inference is not None:
            # inference is a dictionary of (row, col) -> set of values that (row, col) cannot be assigned to (disallowed set)
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
