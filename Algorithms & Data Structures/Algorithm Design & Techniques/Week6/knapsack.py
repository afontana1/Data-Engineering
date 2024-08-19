# Uses python3
import sys

# Task. Given n gold bars, find the maximum weight of gold that fits into a bag of capacity W.
# Input Format. The first line of the input contains the capacity W of a knapsack and the number n of bars
# of gold. The next line contains n integers w[0], w[1], ... , w[n-1] defining the weights of the bars of gold.
# Output Format. Output the maximum weight of gold that fits into a knapsack of capacity W.


def optimal_weight(W, w):
    n = len(w)  # Total number of gold bars
    value = [
        (n + 1) * [0] for i in range(W + 1)
    ]  # Initialize the array of size (n + 1)*(W + 1) for dynamic programming, as 0 is included in both number of gold bars and capacity
    for i in range(1, n + 1):
        for w_ in range(1, W + 1):
            value[w_][i] = value[w_][
                i - 1
            ]  # Initialize with the previous value with capacity w_ and contains 1... i - 1 gold bars
            if (
                w[i - 1] <= w_
            ):  # If the capacity of knapsack allows us to put an extra gold bar
                val = (
                    value[w_ - w[i - 1]][i - 1] + w[i - 1]
                )  # Compute the value of including an extra gold bar
                if (
                    value[w_][i] < val
                ):  # Include it if it yields better value than before
                    value[w_][i] = val
    return value[w_][n]


if __name__ == "__main__":
    input = sys.stdin.read()
    W, n, *w = list(map(int, input.split()))
    print(optimal_weight(W, w))
