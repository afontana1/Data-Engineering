# Uses python3
import sys
import math

# Input Format. The first line contains an integer n. The second line contains integers v[1], v[2], ... , v[n] separated
# by spaces.
# Output Format. Output 1, if it possible to partition v[1], v[2], . . . , v[n] into three subsets with equal sums, and
# 0 otherwise.


def remove_by_val(A, item):  # Remove elements in item from A in place
    for p in item:
        A.remove(p)


def back_tracking(
    value, w_, n, w, picked_item
):  # A backtracking algorithm for dynamic programming of nonrepetitive knapsack problem.
    i, w_i = n, w_
    while i >= 0:
        if w[i - 1] <= w_i:
            if value[w_i][i - 1] >= value[w_i - w[i - 1]][i - 1] + w[i - 1]:
                i -= 1
                continue
            w_i -= w[i - 1]
            picked_item.append(w[i - 1])  # It updates the optimal solution in place
        i -= 1


def optimal_weight(
    W, w
):  # Standard implementation of nonrepetitive knapsack problem, see: knapsack.py for explanation
    n, picked_item = len(w), list()
    value = [(n + 1) * [0] for i in range(W + 1)]

    for i in range(1, n + 1):
        for w_ in range(1, W + 1):
            value[w_][i] = value[w_][i - 1]
            if w[i - 1] <= w_:
                val = value[w_ - w[i - 1]][i - 1] + w[i - 1]
                if value[w_][i] < val:
                    value[w_][i] = val

    back_tracking(value, w_, n, w, picked_item)
    return value[w_][n], picked_item  # Return 1 - optimal value, 2 - optimal solution


def partition3(A):
    A_temp, A_temp2 = (
        A.copy(),
        A.copy(),
    )  # Since test cases are small in size (at most 20), memory used for storage are trivial
    W_each_person = sum(A_temp) / 3  # Equally split
    val = [0] * 3  # Store optimal value for each person

    if (
        len(A) < 3
    ):  # Trivial case, if there are less than 3 items, we can never do partition. return 0.
        return 0
    if W_each_person != math.floor(
        W_each_person
    ):  # Trivial case, as items are not fractional, we cannot have non-integer split of A. return 0.
        return 0
    W_each_person = int(W_each_person)  # Convert float type to integer type

    val[0], item1 = optimal_weight(W_each_person, A_temp)  # First person
    remove_by_val(
        A_temp, item1
    )  # Remove items received by the first person from the array
    val[1], item2 = optimal_weight(W_each_person, A_temp)  # Second person
    remove_by_val(
        A_temp, item2
    )  # Remove items received by the second person from the array
    val[2] = sum(A_temp)  # The last person gets the remaining items
    if (
        val[0] == val[1] and val[1] == val[2]
    ):  # If they all have the same optimal values, there is equal partition. return 1.
        return 1

    # Note that previous DP cannot solve some problem like A = [1, 1, 1, 2, 2, 2]. Then, the first person will get [1, 1, 1] and it leads to unequal split of A
    val[0], item1 = optimal_weight(2 * W_each_person, A_temp2)  # Select 2/3 items of A
    if (
        val[0] != 2 * W_each_person
    ):  # If 2/3 items of A are not sum to 2*(equal split), there is unequal split. return 0.
        return 0
    val[1], item2 = optimal_weight(
        W_each_person, item1
    )  # Select 1/3 items of A from 2/3 items of A
    if val[1] != W_each_person:  # If no equal split, return 0.
        return 0
    remove_by_val(
        A_temp2, item1
    )  # Remove 2/3 items stored in item1 from A_temp2. Now, A_temp2 contains 1/3 items from A.
    remove_by_val(
        item1, item2
    )  # Remove items in item2 from items1. Now, item1 contains 1/3 items from A.
    val[0] = sum(A_temp2)
    val[1] = sum(item1)
    val[2] = sum(item2)
    if (
        val[0] == val[1] and val[1] == val[2]
    ):  # If they all have the same optimal values, there is equal partition. return 1.
        return 1
    return 0  # If not, return 0


if __name__ == "__main__":
    input = sys.stdin.read()
    n, *A = list(map(int, input.split()))
    print(partition3(A))
