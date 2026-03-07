# python3
from sys import stdin
import itertools

EPS = 1e-3
PRECISION = 20


class Equation:  # see energy_values.py
    def __init__(self, a_, b_):
        self.a_ = a_.copy()
        self.b_ = b_.copy()


class Position:  # see energy_values.py
    def __init__(self, column, row):
        self.column = column
        self.row = row


def SelectPivotElement(a_, b_, used_rows, used_columns):  # see energy_values.py
    pivot_element = Position(0, 0)
    while used_rows[pivot_element.row]:
        pivot_element.row += 1
    while used_columns[pivot_element.column]:
        pivot_element.column += 1

    max_row = pivot_element.row
    if a_[pivot_element.row][pivot_element.column] == 0:
        for below_row in range(pivot_element.row + 1, len(a_)):
            if abs(a_[below_row][pivot_element.column]) > abs(
                a_[max_row][pivot_element.column]
            ):
                max_row = below_row
        a_[pivot_element.row], a_[max_row] = a_[max_row], a_[pivot_element.row]
        b_[pivot_element.row], b_[max_row] = b_[max_row], b_[pivot_element.row]
    return pivot_element


def ProcessPivotElement(a_, b_, pivot_element):  # see energy_values.py
    scaling_factor = a_[pivot_element.row][pivot_element.column]
    a_[pivot_element.row] = list(
        map(lambda x: x / scaling_factor, a_[pivot_element.row])
    )
    b_[pivot_element.row] /= scaling_factor

    size = len(a_)
    if pivot_element.row + 1 < size:
        for non_pivot in range(pivot_element.row + 1, size):
            multiple = a_[non_pivot][pivot_element.column]
            for column in range(pivot_element.column, len(a_[0])):
                a_[non_pivot][column] -= multiple * a_[pivot_element.row][column]
            b_[non_pivot] -= multiple * b_[pivot_element.row]
    if pivot_element.row > 0:
        for above_pivot in range(0, pivot_element.row):
            multiple = a_[above_pivot][pivot_element.column]
            for column in range(pivot_element.column, len(a_[0])):
                a_[above_pivot][column] -= multiple * a_[pivot_element.row][column]
            b_[above_pivot] -= multiple * b_[pivot_element.row]
    pass


def MarkPivotElementUsed(
    pivot_element, used_rows, used_columns
):  # see energy_values.py
    used_rows[pivot_element.row] = True
    used_columns[pivot_element.column] = True


def SolveEquation(equation):  # see energy_values.py
    a_ = equation.a_.copy()
    b_ = equation.b_.copy()
    size = len(a_)
    used_columns = [False] * size
    used_rows = [False] * size
    for step in range(size):
        pivot_element = SelectPivotElement(a_, b_, used_rows, used_columns)
        if a_[pivot_element.row][pivot_element.column] == 0:
            return False
        ProcessPivotElement(a_, b_, pivot_element)
        MarkPivotElementUsed(pivot_element, used_rows, used_columns)
    return b_


def Evaluate(
    n, m, c, x
):  # evaluate the objective function of the linear program given solution and coefficients
    opt_val = 0
    for c_i, x_i in zip(c, x):
        opt_val += c_i * x_i
    return opt_val


def AppendEquations(n, m, A, b):  # Append extra constrains to Ax <= b
    # the following for-loop constraints: x[i] > 0 or amount[i] > 0 because we cannot consume negative amounts of diet
    for i in range(m):
        temp_equation = [0] * m
        temp_equation[i] = -1
        A.append(temp_equation)
        b.append(0)
    # the following 4 lines of code constraint: sum of amount < 10 ** 9 to avoid unbounded solution
    max_cap = 10**9
    temp_equation = [1] * m
    A.append(temp_equation)
    b.append(max_cap)
    # new A and b are returned and ready to solve
    return A, b


def CreateSubset(n, m, A, b):
    collection = []
    # select m inequalities out of n + k inequalities and add them to collection list
    for equations in itertools.combinations(zip(A, b), m):
        temp_a = [x[0].copy() for x in equations]
        temp_b = [x[1] for x in equations]
        collection.append(Equation(temp_a, temp_b))
    return collection


def ChangeDataType(A, b):  # change data type for a and b to float
    return [list(map(float, a)) for a in A], list(map(float, b))


def CheckInequality(
    n, m, A, b, solution
):  # check if the solution indeed satisfies all the constraints given in the linear program
    status = True
    for lhs, rhs in zip(A[:-1], b[:-1]):
        status = status & (Evaluate(n, m, lhs, solution) < (rhs + EPS))
    return status


def CheckInfinity(n, m, equations):  # check if the solution if unbounded
    max_cap = 10**9
    max_cap = float(max_cap)
    for (
        j
    ) in (
        equations.b_
    ):  # If the solution is bounded, one element in solution will goes to infinity (i.e. max_cap)
        if j == max_cap:
            return True
    return False


def solve_diet_problem(n, m, A, b, c):
    A, b = AppendEquations(
        n, m, A, b
    )  # Append constraints to Ax <= b to avoid unwanted solution which also yields the maximum
    A, b = ChangeDataType(A, b)  # Change data type for A and b
    collection = CreateSubset(
        n, m, A, b
    )  # Consider different combinations of m inequalities out of all and solve for the optimal solution one by one
    solutions, opt_vals, store_equations = [], [], []

    for equations in collection:
        solution = SolveEquation(
            equations
        )  # Solve tight equations for those m inequalities using Gaussian elimination
        if (
            solution == False
        ):  # if there is no solution, proceed to the next set of tight inequalities
            continue

        status = CheckInequality(
            n, m, A, b, solution
        )  # If there is solution, check if the solution is feasible. Ignore non feasible solution
        if (
            status == True
        ):  # If the solution lies in constraints, evaluate the optimal value and store the solutions, corresponding inequalities and the optimal values to three lists
            opt_val = Evaluate(n, m, c, solution)
            store_equations.append(equations)
            solutions.append(solution)
            opt_vals.append(opt_val)

    # The following for-loop find the best solution among all feasible solutions
    max_index, max_value = 0, float(-(10**9))
    for index, value in enumerate(opt_vals):
        if value > max_value:
            max_value = value
            max_index = index
    zero_solution = [
        0
    ] * m  # we also consider a trivial solution, that is no consumption of any diets
    status = CheckInequality(
        n, m, A, b, zero_solution
    )  # check if zero solution is feasible
    # Case 1: No feasible solutions are found. Return zero solutions if feasible.
    if len(solutions) == 0:
        if status == True:
            return 0, zero_solution
        return -1, []
    # Case 2: Feasible solutions are found, check if the solution is unbounded
    elif CheckInfinity(n, m, store_equations[max_index]):
        return 1, []
    # Case 3: Feasible solution and not unbounded, compare zero solutions vs optimal solution found and return the appropriate
    else:
        if (status == True) & (Evaluate(n, m, c, zero_solution) > opt_vals[max_index]):
            return 0, zero_solution
        return 0, solutions[max_index]


n, m = list(
    map(int, stdin.readline().split())
)  # n = number of equations, m = number of state variables
A = []
for i in range(
    n
):  # from row 1 to row n in given input, they are coefficients for the constraint
    A += [list(map(int, stdin.readline().split()))]
b = list(
    map(int, stdin.readline().split())
)  # the second last line is a constant vector for the constraint s.t. Ax <= b
c = list(
    map(int, stdin.readline().split())
)  # the last line is a vector for the linear problem such that max c*x
anst, ansx = solve_diet_problem(n, m, A, b, c)
if anst == -1:
    print("No solution")
if anst == 0:
    print("Bounded solution")
    print(" ".join(list(map(lambda x: "%.18f" % x, ansx))))
if anst == 1:
    print("Infinity")
