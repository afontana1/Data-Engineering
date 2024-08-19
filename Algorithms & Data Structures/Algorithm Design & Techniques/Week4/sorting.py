# Uses python3
import sys
import random

# Task. To force the given implementation of the quick sort algorithm to efficiently process sequences with
# few unique elements, your goal is replace a 2-way partition with a 3-way partition. That is, your new
# partition procedure should partition the array into three parts: < x part, = x part, and > x part.
# Input Format. The first line of the input contains an integer n. The next line contains a sequence of n
# integers a[0], a[1], . . . , a[n-1].
# Constraints. 1 <= n <= 105; 1 <= a[i] <= 109 for all 0 <= 𝑖 <= 𝑛.
# Output Format. Output this sequence sorted in non-decreasing order.


def partition3(a, l, r):
    # Short inplace: [integers smaller than x][integers same as x][integerrs greater than x]
    # Return two indices as upper and lower bound for next sorting
    less_than, greater_than = l, r
    i = l
    x = a[l]
    while i <= greater_than:
        if a[i] < x:  # Swap and make item smaller than the pivot on left hand side
            a[less_than], a[i] = a[i], a[less_than]
            less_than += 1  # Shift pivot
            i += 1  # Shift a unit to the right for the next comparison
        elif a[i] > x:  #
            a[i], a[greater_than] = (
                a[greater_than],
                a[i],
            )  # Swap the items at the end and i-th position
            greater_than -= (
                1  # Since item at the end must be greater than pivot, decrease it by 1
            )
        else:  # Same value then shift a unit to the right for next comparison
            i += 1
    return (
        less_than,
        greater_than,
    )  # It gives the smallest index and the largest index of same value in the array having value of a[l]


def randomized_quick_sort(a, l, r):
    if l >= r:  # if l >= r, only an integer
        return
    k = random.randint(l, r)  # randomized pivot
    a[l], a[k] = a[k], a[l]  # put this pivot at the beginning of array
    m1, m2 = partition3(a, l, r)
    randomized_quick_sort(a, l, m1 - 1)
    randomized_quick_sort(a, m2 + 1, r)


if __name__ == "__main__":
    input = sys.stdin.read()
    n, *a = list(map(int, input.split()))
    randomized_quick_sort(a, 0, n - 1)
    for x in a:
        print(x, end=" ")
