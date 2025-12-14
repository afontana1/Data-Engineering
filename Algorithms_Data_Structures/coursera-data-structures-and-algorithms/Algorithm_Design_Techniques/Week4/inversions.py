# Uses python3
import sys

# Task. The goal in this problem is to count the number of inversions of a given sequence.
# Input Format. The first line contains an integer n, the next one contains a sequence of integers
# a[0], a[1], . . . , a[n-1].
# Output Format. Output the number of inversions in the sequence.


def get_number_of_inversions(
    a, b, left, right
):  # Array b is given in the problem but I don't use it.
    number_of_inversions = 0  # Initialize the number of inversions
    if right - left <= 1:
        return number_of_inversions  # If there is only one element in a[left:right], nothing to inverse
    ave = (left + right) // 2  # mid point
    number_of_inversions += get_number_of_inversions(
        a, b, left, ave
    )  # Accumulate the number of inversions
    number_of_inversions += get_number_of_inversions(
        a, b, ave, right
    )  # Accumulate the number of inversions
    # For more than one element in the array
    left_list, right_list = a[left:ave].copy(), a[ave:right].copy()
    d = []
    while (left_list != []) & (right_list != []):
        left_first, right_first = (
            left_list[0],
            right_list[0],
        )  # Standard merge sort procedure
        if left_first <= right_first:
            d.append(left_first)
            del left_list[0]
        else:
            d.append(right_first)
            del right_list[0]
            number_of_inversions += len(
                left_list
            )  # If we append something on the right, it implies an inversion.
    # Note that any element in left_list and the first element in right_list can cause an inversion. So, len(left_list) is the total number of inversion
    if left_list == []:
        d += right_list
    elif right_list == []:
        d += left_list
    a[left:right] = d  # Update sorted subarrays
    return number_of_inversions  # Return back the number of inversions


if __name__ == "__main__":
    input = sys.stdin.read()
    n, *a = list(map(int, input.split()))
    b = n * [0]
    print(get_number_of_inversions(a, b, 0, len(a)))
