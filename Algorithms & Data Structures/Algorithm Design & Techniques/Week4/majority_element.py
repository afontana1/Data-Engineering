# Uses python3
import sys

# Task. The goal in this code problem is to check whether an input sequence contains a majority element.
# Input Format. The first line contains an integer n, the next one contains a sequence of n non-negative
# integers a[0], a[1], . . . , a[n-1].
# Output Format. Output 1 if the sequence contains an element that appears strictly more than n/2 times,
# and 0 otherwise.
# Note: As n can grow to 10^9, I've tried many methods e.g. merge sort and only this method works.


def get_majority_element(a, left, right):
    if (
        left + 1 == right
    ):  # Base case: a[left:right] has length 1; return a[left] i.e. a single number
        return a[left]
    m = (left + right) // 2  # mid point
    b = get_majority_element(a, left, m)
    c = get_majority_element(a, m, right)

    get_maj_list = [
        element for element in (b, c) if element != -1
    ]  # Remove -1 and get_maj_list contains a list of possible major elements

    for maj_element in get_maj_list:
        count = 0
        for i in range(left, right):
            if (
                a[i] == maj_element
            ):  # If any element in a[left:right] belongs to major element, count it
                count += 1
        if (
            count > (right - left) / 2
        ):  # If the count is already > n/2, return the major element as it's the definition
            return maj_element
    return -1  # Otherwise, there is no major element in the list and return -1


if __name__ == "__main__":
    input = sys.stdin.read()
    n, *a = list(map(int, input.split()))
    if get_majority_element(a, 0, n) != -1:
        print(1)
    else:
        print(0)
