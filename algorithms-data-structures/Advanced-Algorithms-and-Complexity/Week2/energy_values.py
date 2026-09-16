# python3
EPS = 1e-6
PRECISION = 20
# Task. You’re looking into a restaurant menu which shows for each dish the list of ingredients with amounts
# and the estimated total energy value in calories. You would like to find out the energy values of
# individual ingredients (then you will be able to estimate the total energy values of your favorite dishes).
# Input Format. The first line of the input contains an integer n — the number of dishes in the menu, and
# it happens so that the number of different ingredients is the same. Each of the next n lines contains
# description a[1], a[2], . . . , a[n], E of a single menu item. a[i] is the amount of i-th ingredient in the dish, and
# E is the estimated total energy value of the dish. If the ingredient is not used in the dish, the amount
# will be specified as a[i] = 0; beware that although the amount of any ingredient in any real
# menu would be positive, we will test that your algorithm works even for negative amounts a[i] < 0.
# Output Format. Output n real numbers — for each ingredient, what is its energy value. These numbers
# can be non-integer, so output them with at least 3 digits after the decimal point.


class Equation:  # an equation object with Ax = b
    def __init__(self, a, b):
        self.a = a
        self.b = b


class Position:
    def __init__(self, column, row):
        self.column = column
        self.row = row


def ReadEquation():  # read input data
    size = int(input())
    a = []
    b = []
    for row in range(size):
        line = list(map(float, input().split()))
        a.append(line[:size])  # First 'size' elements are coefficients
        b.append(line[size])  # the last element is constraint on total
    return Equation(a, b)


def SelectPivotElement(a, b, used_rows, used_columns):
    # Search for the pivot element from the left-top corner
    # Indices of previous pivot elements are recorded in used_rows and used_columns
    pivot_element = Position(
        0, 0
    )  # the first pivot element is the first element at the first row
    while used_rows[
        pivot_element.row
    ]:  # long as pivot_element.row has been used before in Gaussian elimination, go to next row
        pivot_element.row += 1
    while used_columns[
        pivot_element.column
    ]:  # long as pivot_element.column has been used before in Gaussian elimination, go to next column
        pivot_element.column += 1
    # Case 1: pivot element = 0
    max_row = pivot_element.row
    if (
        a[pivot_element.row][pivot_element.column] == 0
    ):  # If the pivot element is singular, we need to search for the largest element in row below pivot element within the same column
        for below_row in range(pivot_element.row + 1, len(a)):
            if (
                a[below_row][pivot_element.column] > a[max_row][pivot_element.column]
            ):  # If the element > previous found largest element, the row as max_row
                max_row = below_row
        # After the searching process, do swapping for both coefficient matrix A, and constant vector b
        a[pivot_element.row], a[max_row] = a[max_row], a[pivot_element.row]
        b[pivot_element.row], b[max_row] = b[max_row], b[pivot_element.row]
    # Case 2: pivot element != 0
    # the if condition will not be activated and return the found pivot element immediately in this case, no need for searching and swapping
    return pivot_element


def ProcessPivotElement(a, b, pivot_element):
    scaling_factor = a[pivot_element.row][
        pivot_element.column
    ]  # the pivot element is a scaling factor to subtract from other rows
    a[pivot_element.row] = list(
        map(lambda x: x / scaling_factor, a[pivot_element.row])
    )  # divide pivot row with scaling factor, the position of pivot element has value 1 now
    b[
        pivot_element.row
    ] /= scaling_factor  # also divide the constant vector as we work on [A|b] during Gaussian elimination
    size = len(a)
    if pivot_element.row + 1 < size:  # From pivot row + 1 to the bottom
        for non_pivot in range(pivot_element.row + 1, size):
            # To clear all elements below the pivot element in the pivot column
            multiple = a[non_pivot][
                pivot_element.column
            ]  # extract the element within the same column as pivot element for rows below pivot row
            for column in range(
                pivot_element.column, len(a[0])
            ):  # multiply this element with (each element in) pivot rows and subtract it from nonpivot row
                a[non_pivot][column] -= multiple * a[pivot_element.row][column]
            b[non_pivot] -= multiple * b[pivot_element.row]
    if pivot_element.row > 0:  # Similar process as above
        for above_pivot in range(0, pivot_element.row):
            # To clear all elements above the pivot element in the pivot column
            multiple = a[above_pivot][
                pivot_element.column
            ]  # extract the element within the same column as pivot element for rows above pivot row
            for column in range(pivot_element.column, len(a[0])):
                a[above_pivot][column] -= multiple * a[pivot_element.row][column]
            b[above_pivot] -= multiple * b[pivot_element.row]
    pass


def MarkPivotElementUsed(pivot_element, used_rows, used_columns):
    used_rows[pivot_element.row] = True
    used_columns[pivot_element.column] = True


def SolveEquation(equation):
    a = equation.a
    b = equation.b
    size = len(a)
    used_columns = [False] * size
    used_rows = [False] * size

    for step in range(size):
        pivot_element = SelectPivotElement(
            a, b, used_rows, used_columns
        )  # select the pivot element of each row, do swap line if necessary
        ProcessPivotElement(
            a, b, pivot_element
        )  # performs row operations to clear all elements ahove and below the pivot in the pivot column
        MarkPivotElementUsed(
            pivot_element, used_rows, used_columns
        )  # now, mark the pivot element as "used' and don't reuse it in the next iteration
    return b  # b after Gaussian elimination is the solution to the problem


def PrintColumn(column):
    size = len(column)
    for row in range(size):
        print("%.20lf" % column[row])


if __name__ == "__main__":
    equation = ReadEquation()
    solution = SolveEquation(equation)
    PrintColumn(solution)
