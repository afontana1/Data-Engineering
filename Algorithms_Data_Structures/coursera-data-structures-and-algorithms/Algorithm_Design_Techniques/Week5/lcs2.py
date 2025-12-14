# Uses python3
import sys

# Task. Given two sequences A = (a[1], a[2], ... , a[n]) and B = (b[1], b[2]], ,,, , b[m]), find the length of their longest
# common subsequence, i.e., the largest non-negative integer p such that there exist indices 1 <= i[1] <
# i[2] < ... < i[p] <= n and 1 <= j[1] < j[2] < ... < j[p] <= m, such that a[i[1]] = b[j[1]] , ... , a[i[p]] = b[j[p]].
# Input Format. First line: n. Second line: a[1], a[2], ... , a[n]. Third line: m. Fourth line: b[1], b[2], ... , b[m].
# Constraints. 1 <= n, m <= 100; −10 ** 9 < a[i], b[i] < 10 ** 9.
# Output Format. Output p.


def edit_distance(s, t):  # Please read edit_distance.py for explanation
    D = [(len(t) + 1) * [0] for i in range(len(s) + 1)]

    for i in range(1, len(s) + 1):
        D[i][0] = i
    for i in range(1, len(t) + 1):
        D[0][i] = i
    for j in range(1, len(t) + 1):
        for i in range(1, len(s) + 1):
            insertion = D[i][j - 1] + 1
            deletion = D[i - 1][j] + 1
            match = D[i - 1][j - 1]
            mismatch = (
                D[i - 1][j - 1] + 2
            )  # Same as the calculation of edit distance but change the penalty of mismatch to 2
            if s[i - 1] == t[j - 1]:
                D[i][j] = min(insertion, deletion, match)
            else:
                D[i][j] = min(insertion, deletion, mismatch)

    i, j = len(s), len(t)
    count, common = 0, 0

    while (i != 0) | (j != 0):
        if (i > 0) & (D[i][j] == D[i - 1][j] + 1):
            count += 1
            i -= 1
        elif (j > 0) & (D[i][j] == D[i][j - 1] + 1):
            count += 1
            j -= 1
        else:
            if s[i - 1] != t[j - 1]:
                count += 1
            else:
                common += 1
            i -= 1
            j -= 1
    return common


def lcs2(a, b):
    return edit_distance(a, b)


if __name__ == "__main__":
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n = data[0]
    data = data[1:]
    a = data[:n]

    data = data[n:]
    m = data[0]
    data = data[1:]
    b = data[:m]

    print(lcs2(a, b))
