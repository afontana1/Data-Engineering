# python3
from sys import stdin
from itertools import product

# Integer linear programming Ax <= b
# At most 3 nonzero coefficients in matrix A
# Output CNF formula


class Clause:  # A standard class of clause
    def __init__(self, numvar):
        self.clause = list()  # initialize the clause with an empty list
        self.m = 0  # number of equations in CNF
        self.n = numvar  # number of variables used in CNF

    def update_count(self):
        self.m = len(self.clause)  # update the total number of equations in CNF

    def empty_clause(self):
        return len(self.clause) == 0  # A method to determine if the clause is empty

    def print_clause(self):
        print(
            str(self.m) + " " + str(self.n)
        )  # A method for printing clause to SAT solver, first line is number of variables and equations of CNF
        for clause in self.clause:  # print clauses line by line
            clause.append(0)
            print(" ".join(map(str, clause)))


def get_nonzero(
    arr,
):  # Find at most 3 nonzero coefficients in each inequality (arr is a row of matrix A)
    results = list()
    for i, coef in enumerate(arr):
        if coef != 0:
            results.append(
                (i, coef)
            )  # each element in results list is tuple(index of variable, coefficient)
    return len(results), results


def build_truthtable(
    arr, size, const, C
):  # Negate variables in CNF if they contribute to the violation of constraints (decline the proposals that exceed the budget)
    table = list(
        product([False, True], repeat=size)
    )  # build a truth table of T and F based on the number of nonzero integer in row i of matrix A, find out the combination of variables that violate the constraint
    for t in table:
        temp = list(
            zip(t, arr)
        )  # temp list is tuple(boolean, tuple(index, coefficient))
        s = sum([b * coef[1] for (b, coef) in temp])
        if s > const:  # the i-th constraint is violated if the sum of integer > budget
            c = [
                ((-1) ** b) * (coef[0] + 1) for (b, coef) in temp
            ]  # negate the variables that violates the constraint and are true in the truth table, and do not negate the variables that are false in truth table
            C.clause.append(c)


n, m = list(map(int, stdin.readline().split()))
A = []
for i in range(n):
    A += [list(map(int, stdin.readline().split()))]
b = list(map(int, stdin.readline().split()))
C = Clause(m)

for i, coef in enumerate(
    A
):  # for each row, find nonzero coefficients (if any), build a truth table and append clauses
    size, nonzero_coef = get_nonzero(coef)
    if size == 0:
        continue
    build_truthtable(nonzero_coef, size, b[i], C)

if C.empty_clause():  # case for empty clauses, output a trivial CNF formula
    C.clause.append([1, -1])
C.update_count()  # update the number of equations after all processing
C.print_clause()  # print CNF to SAT solver
