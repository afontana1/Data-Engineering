# Uses python3

import sys

# Task. Given two sequences a[1], a[2], . . . , a[n] (a[i] is the profit per click of the i-th ad) and b[1], b[2], . . . , b[n] (b[i] is
# the average number of clicks per day of the i-th slot), we need to partition them into n pairs (a[i], b[i])
# such that the sum of their products is maximized.
# Input Format. The first line contains an integer n, the second one contains a sequence of integers
# a[1], a[2], . . . , a[n], the third one contains a sequence of integers b[1], b[2], . . . , b[n].
# Output Format. Output the maximum value of sum(a[i]*c[i]) for i from 1 to n, where c[1], c[2], . . . , c[n] is a permutation of
# b[1], b[2], ..., b[n]

# Greedy algorithm: Let i = argmax{a[i]} and j = argmax{b[j]}. We associate a[i] with b[j] and find i' and j' in the next iteration until no more ads.
# Let consider two pairs, a[i], b[j] and a[i'], b[j'] with a[i] > a[i'] and b[j], b[j'].
# Since (a[i] - a[i'])*(b[j] - b[j']) > 0
# a[i]*b[j] - a[i']*b[j] - a[i]*b[j'] + a[i']*b[j'] > 0
# So, a[i]*b[j] + a[i']*b[j'] > a[i']*b[j] + a[i]*b[j'] which shows that picking maximum a[i] and b[j] among all and add up iteratively is a safe move.


def search_max(
    a,
):  # Linear search for the index corresponding to the maximum value in a list
    index = 0
    for i in range(len(a)):
        if a[i] > a[index] and i != index:
            index = i
    return index


def max_dot_product(a, b):
    a_copy = a.copy()  # Copy array avoid changing the original one
    b_copy = b.copy()  # Copy array avoid changing the original one
    res = 0  # revenues from ads, initialized with 0
    n = len(a_copy)  # The number of ads
    for i in range(
        n
    ):  # For loop costs O(n) and search_max() costs 2*O(n). In total, running complexity is O(n^2).
        a_index = search_max(a_copy)
        b_index = search_max(b_copy)
        res += a_copy[a_index] * b_copy[b_index]
        del a_copy[a_index]  # Remove the maximum for the next search
        del b_copy[b_index]  # Remove the maximum for the next search
    return res


if __name__ == "__main__":
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n = data[0]
    a = data[1 : (n + 1)]
    b = data[(n + 1) :]
    print(max_dot_product(a, b))
