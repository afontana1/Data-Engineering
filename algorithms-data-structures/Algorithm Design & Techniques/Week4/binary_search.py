# Uses python3
import sys

# Task. The goal in this code problem is to implement the binary search algorithm.
# Input Format. The first line of the input contains an integer n and a sequence a[0] < a[1] <...< a[n-1]
# of n pairwise distinct positive integers in increasing order. The next line contains an integer k and k
# positive integers b[0], b[1], . . . , b[k-1].
# Output Format. For all i from 0 to k - 1, output an index 0 <= j <= n − 1 such that a[j] = b[i] or −1 if there
# is no such index.


def binary_search(a, x):  # a: sorted array
    left, right = 0, len(a) - 1
    while right >= left:
        mid = (left + right) // 2  # Mid point
        if a[mid] == x:  # If x is found at the mid point
            return mid
        elif (
            a[mid] < x
        ):  # If not found at mid point and target > a[mid], consider [mid + 1, r]
            left = mid + 1
        else:  # Otherwise, consider [l, mid - 1]
            right = mid - 1
    return -1  # No such value x


if __name__ == "__main__":
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n = data[0]
    m = data[n + 1]
    a = data[1 : n + 1]
    for x in data[n + 2 :]:
        print(binary_search(a, x), end=" ")
