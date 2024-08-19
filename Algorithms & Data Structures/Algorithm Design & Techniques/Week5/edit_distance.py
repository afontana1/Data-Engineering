# Uses python3
# Task. The goal of this problem is to implement the algorithm for computing the edit distance between two strings.
# Input Format. Each of the two lines of the input contains a string consisting of lower case latin letters.
# Constraints. The length of both strings is at least 1 and at most 100.
# Output Format. Output the edit distance between the given two strings.


def edit_distance(s, t):
    common = 0  # Initialize the output, edit distance between s and t, with 0
    D = [
        (len(t) + 1) * [0] for i in range(len(s) + 1)
    ]  # D[i][j] stores the edit distance between s[1....i] and t[1...j]

    for i in range(
        1, len(s) + 1
    ):  # The case if t is empty, needs i deletions for s[1...i] to align with t[0]
        D[i][0] = i
    for i in range(
        1, len(t) + 1
    ):  # The case if s is empty, needs i insertions for s[0] to align wtih t[1...i]
        D[0][i] = i
    for j in range(1, len(t) + 1):  # Otherwise, both t and s are not empty
        for i in range(
            1, len(s) + 1
        ):  # Fill the grid with insertion, deletion, match or mismatch assuming indel and mismatch have the same cost, 1.
            insertion = D[i][j - 1] + 1
            deletion = D[i - 1][j] + 1
            match = D[i - 1][j - 1]
            mismatch = D[i - 1][j - 1] + 1
            if s[i - 1] == t[j - 1]:
                D[i][j] = min(insertion, deletion, match)
            else:
                D[i][j] = min(insertion, deletion, mismatch)

    i, j = len(s), len(t)  # Backtracking the solution, start at the end
    count = 0

    while (i != 0) | (j != 0):
        if (i > 0) & (
            D[i][j] == D[i - 1][j] + 1
        ):  # If it's coming from deletion, shift a unit upward in the grid
            count += 1
            i -= 1
        elif (j > 0) & (
            D[i][j] == D[i][j - 1] + 1
        ):  # If it's coming from insertion, shift a unit leftward in the grid
            count += 1
            j -= 1
        else:
            if (
                s[i - 1] != t[j - 1]
            ):  # Otherwise, if it's unmatch or match, shift a unit upward and leftward in the grid
                count += 1
            else:
                common += 1  # If two letters are common in s[i] and t[j], increase the edit distance by 1
            i -= 1
            j -= 1
    return common


if __name__ == "__main__":
    print(edit_distance(input(), input()))
