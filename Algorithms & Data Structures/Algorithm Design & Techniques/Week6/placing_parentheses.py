# Uses python3
# Task. Find the maximum value of an arithmetic expression by specifying the order of applying its arithmetic
# operations using additional parentheses.
# Input Format. The only line of the input contains a string s of length 2*n + 1 for some n, with symbols
# s[0], s[1], . . . , s[2n]. Each symbol at an even position of s is a digit (that is, an integer from 0 to 9) while
# each symbol at an odd position is one of three operations from {+,-,*}.
# Output Format. Output the maximum possible value of the given arithmetic expression among different
# orders of applying arithmetic operations.


def evalt(a, b, op):  # It is a function to evaluate an operation with 2 digits
    if op == "+":
        return a + b
    elif op == "-":
        return a - b
    elif op == "*":
        return a * b
    else:
        assert False


def min_and_max(i, j, dataset, m, M):
    min_, max_ = 100, -100
    for k in range(i, j):
        # Consider a subexpression: d[i]op[i]....op[j-1]d[j],
        # op[k] from i to j - 1 evaluates the two subexpressions i.e. (d[i]op[i]....d[k]) op[k] (d[k+1]....op[j-1]op[j])
        # The base case is d[i] op[i] d[i+1]. The second case is (d[i] op[i] d[i+1]) op[i+1] (d[i+2] op[i+2] d[i+3])
        # For the second case, We let M[i, i+1], m[i, i+1] denote the maximum values and the minimum values evaluated from (d[i] op[i] d[i+1]), resp.
        # We let M[i+2, i+3], m[i+2, i+3] denote the maximum values and the minimum values evaluated from (d[i+2] op[i+2] d[i+3]), resp.
        # So, there 4 combinations of output: M[i, i+1]*M[i+2, i+3], M[i, i+1]*m[i+2, i+3], m[i, i+1]*M[i+2, i+3], m[i, i+1]*m[i+2, i+3]
        # Take the maximum and the minimum and return it
        op = dataset[2 * k + 1]
        a, b, c, d = (
            evalt(M[i][k], M[k + 1][j], op),
            evalt(M[i][k], m[k + 1][j], op),
            evalt(m[i][k], M[k + 1][j], op),
            evalt(m[i][k], m[k + 1][j], op),
        )
        min_, max_ = min(min_, a, b, c, d), max(max_, a, b, c, d)
    return (min_, max_)


def get_maximum_value(dataset):
    n = len(dataset) // 2 + 1  # Get the total number of digits
    m, M = [n * [0] for i in range(n)], [
        n * [0] for i in range(n)
    ]  # Let m, M be the minimum and the maximum value of subexpressions, resp

    for i in range(
        len(dataset)
    ):  # Let i denote the index of the input array, with digits and operators mixed together
        if i % 2 == 0:  # If i mod 2 == 0: dataset[i] contains a digit
            pos = i // 2
            m[pos][pos], M[pos][pos] = int(dataset[i]), int(
                dataset[i]
            )  # When the subexpression is a digit,
            # no operations can be carried out and minimum = maximum, save it in the diagonal

    for s in range(n - 1):  # Double for-loops to update the upper diagonal of m and M
        for i in range(n - s - 1):
            j = (
                i + s + 1
            )  # because j - i = s + 1 which ensures the upper diagonal elements of m and M are updated
            m[i][j], M[i][j] = min_and_max(i, j, dataset, m, M)
    return M[0][n - 1]


if __name__ == "__main__":
    print(get_maximum_value(input()))
