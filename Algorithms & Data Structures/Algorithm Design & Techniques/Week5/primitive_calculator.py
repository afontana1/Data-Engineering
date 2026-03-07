# Uses python3
import sys

# Task. Given an integer n, compute the minimum number of operations needed to obtain the number 𝑛
# starting from the number 1.
# Input Format. The input consists of a single integer 1 <= n <= 106.
# Output Format. In the first line, output the minimum number k of operations needed to get n from 1.
# In the second line output a sequence of intermediate numbers. That is, the second line should contain
# positive integers a[0], a[1], . . . , a[k−1] such that a[0] = 1, a[k-1] = n and for all 0 <= i < k − 1, a[i+1] is equal to
# either a[i] + 1, 2*a[i], or 3*a[i]. If there are many such sequences, output any one of them.


def dp_optimal_sequence(n):
    MinOpt, rlist = [
        0
    ] * n, []  # MinOpt: Record minimum number of operations for each integer upto n, rlist: Record a sequence of number leading to n
    MinOpt[0] = 0  # No operation is needed for 1, so MinOpt[1 - 1] = 0
    for i in range(
        n
    ):  # Let i denote the index of MinOpt. Minopt[0] is the minimum number of operations for number 1. Similarly, Minopt[n - 1] is associated with number n
        next_list = [i + 1, 2 * (i + 1) - 1, 3 * (i + 1) - 1]
        # 1) Index increases by 1 when the number is added 1
        # Let k' = k + 1. index[k] = k - 1 and index[k'] = k' - 1 = k + 1 - 1 = k = index[k] + 1
        # So, i + 1 is the position of array when the number is added 1
        # 2) Index increases by 2*(old Index + 1) - 1 when the number is doubled
        # Let k' = 2*k. index[k'] = k' - 1 = 2*k - 1 = 2*(index[k] + 1) - 1
        # 3) Index increases by 3*(old Index + 1) - 1 when the number is triped
        # Let k' = 3*k. index[k'] = k' - 1 = 3*k - 1 = 3*(index[k] + 1) - 1
        # Hence, the above formulae are correct for index[k'] under 3 different operations on number k
        for next_pos in next_list:
            if (
                next_pos < n
            ):  # It's possible one of the calculation produce a number bigger than n. Just ignore it.
                if (
                    MinOpt[next_pos] == 0
                ):  # If the next position hasn't been filled, just filled with (the minimum operations of k) plus 1
                    MinOpt[next_pos] = MinOpt[i] + 1
                elif (
                    MinOpt[i] + 1 < MinOpt[next_pos]
                ):  # If the next posistion has been filled in previous DP process, compare if the current move requires fewer operations
                    MinOpt[next_pos] = MinOpt[i] + 1
    rlist.append(n)  # Backtracking technique
    count = (
        MinOpt[-1] - 1
    )  # It should take at most MinOpt[n - 1] steps (calculated from dynamic programming) to reduce n to 1. Minus 1 because we start from 0.
    while count >= 0:
        last_num = rlist[-1]  # Start from the end, integer n
        memo = []  # Contain three possible operations to reach n
        memo.append(
            last_num - 2
        )  # First, index[k] = index[k'] - 1 = k' - 1 - 1 = k' - 2
        if (
            last_num % 2 == 0
        ):  # If k' is divisible by 2, then index[k] = (index[k'] + 1) / 2 - 1 = k'/2 - 1
            memo.append(last_num // 2 - 1)
        if (
            last_num % 3 == 0
        ):  # If k' is divisible by 3, then index[k] = (index[k'] + 1) / 3 - 1 = k'/3 - 1
            memo.append(last_num // 3 - 1)
        min_index = 0
        for i in range(
            len(memo)
        ):  # Consider all possible operations to get k' from the primitive calculator, and find out the operation which is the minimum in total
            if (min_index != i) & (MinOpt[memo[min_index]] > MinOpt[memo[i]]):
                min_index = i
        rlist.append(memo[min_index] + 1)  # Record the number produced by the operation
        count -= 1
    return reversed(rlist)


input = sys.stdin.read()
n = int(input)
sequence = list(dp_optimal_sequence(n))
print(len(sequence) - 1)
for x in sequence:
    print(x, end=" ")
