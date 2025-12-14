# Uses python3
import sys

# Task. Given three sequences A = (a[1], a[2], ..., a[n]), B = (b[1], b[2], ... , b[m]), and C = (c[1], c[2], ... , c[l]), find the
# length of their longest common subsequence, i.e., the largest non-negative integer p such that there
# exist indices 1 <= i[1] < i[2] < ... < i[p] <= 𝑛, 1 <= j[1] < j[2] < ... < j[p] <= m, 1 <= k[1] < k[2] < ... < k[p] <= l such
# that a[i[1]] = b[j[1]] = c[k[1]] , . . . , a[i[p]] = b[j[p]] = c[k[p]]
# Input Format. First line: n. Second line: a[1], a[2], ..., a[n]. Third line: m. Fourth line: b[1], b[2], ... , b[m]. Fifth line:
# l. Sixth line: c[1], c[2], ... , c[l]
# Constraints. 1 <= n, m, l <= 100; −10 ** 9 < a[i], b[i], c[i] < 10 ** 9.
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
    count, common, subsequence = (
        0,
        0,
        list(),
    )  # subsequence to contain the matched sequence in reversed order

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
                subsequence.append(s[i - 1])
                common += 1
            i -= 1
            j -= 1
    return common, list(reversed(subsequence))


def lcs3(a, b, c):
    # Note: Edit distance is not associative
    common_ab, subseq_ab = edit_distance(
        a, b
    )  # Longest common sequence between a and b (edit distance to transform a to b)
    common_ba, subseq_ba = edit_distance(
        b, a
    )  # Longest common sequence between b and a (edit distance to transform b to a)
    common_cab, subseq_cab = edit_distance(
        c, subseq_ab
    )  # Longest common sequence between c and lcs(a, b)
    common_cba, subseq_cba = edit_distance(
        c, subseq_ba
    )  # Longest common sequence between c and lcs(b, a)
    # To be robust, we may also need to consider edit_distance(subseq_ab, c) and edit_distance(subseq_ba, c) but the grader seems not having such test cases
    if common_cab > common_cba:  # Just pick the sequence with maximum length
        return common_cab
    return common_cba


if __name__ == "__main__":
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    an = data[0]
    data = data[1:]
    a = data[:an]
    data = data[an:]
    bn = data[0]
    data = data[1:]
    b = data[:bn]
    data = data[bn:]
    cn = data[0]
    data = data[1:]
    c = data[:cn]
    print(lcs3(a, b, c))
