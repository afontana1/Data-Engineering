# Uses python3
import sys
import math

# Task. You are given a set of points on a line and a set of segments on a line. The goal is to compute, for
# each point, the number of segments that contain this point.
# Input Format. The first line contains two non-negative integers s and p defining the number of segments
# and the number of points on a line, respectively. The next s lines contain two integers a[i], b[i] defining
# the i-th segment [a[i], b[i]]. The next line contains p integers defining points x[1], x[2], . . . , x[p].
# Output Format. Output p non-negative integers k[0], k[1], . . . , k[p-1] where k[i] is the number of segments which
# contain x[i].


def merge(subarray_1, subarray_2):
    # A part of merge sort algorithm costs O(n)
    array_sorted = list()
    while len(subarray_1) > 0 and len(subarray_2) > 0:
        if subarray_1[0] <= subarray_2[0]:
            array_sorted.append(subarray_1.pop(0))
        else:
            array_sorted.append(subarray_2.pop(0))
    if len(subarray_1) > 0:
        array_sorted += subarray_1
    elif len(subarray_2) > 0:
        array_sorted += subarray_2
    return array_sorted


def merge_sort(array):
    # A standard implementation of merge sort in O(nlogn)
    n = len(array)
    if n == 1:
        return array
    m = math.floor(n / 2)
    subarray_1 = merge_sort(array[:m])
    subarray_2 = merge_sort(array[m:])
    array_sorted = merge(subarray_1, subarray_2)
    return array_sorted


def modified_binary_search_inf(array, value, l, r):  # Time complexity: O(logn)
    # Input: sorted ending points of segments
    # Return: the index of the largest ending points < point
    m = math.floor((l + r) / 2)  # mid point
    if value == array[m]:  # If there is an exact match, do backward linear search
        while value == array[m]:
            m -= 1
            if (
                m < 0
            ):  # Case if given point is the minimum, then no largest ending points => return -1
                return -1
        return m  # Otherwise, return such point
    if l == r:
        if (
            array[l] < value
        ):  # If there is no exact match, check if the ending point found is smaller than the given point. If so, return it.
            return l
        return (
            l - 1
        )  # If not, it's possible that 1) array[m] < value < array[m + 1] or 2) value < array[m]. First case => set l := m+1 and r := r. When l == r, it's possible lower bound on a unit left. If original index is already 0, it will return -1.
    elif value < array[m]:
        return modified_binary_search_inf(array, value, l, m)
    else:
        return modified_binary_search_inf(array, value, m + 1, r)


def modified_binary_search_sup(array, value, l, r):  # Time complexity: O(logn)
    # Input: sorted starting points of segments
    # Return: the index of the smallest starting points > point
    m = math.floor((l + r) / 2)
    if value == array[m]:  # If there is an exact match, do forward linear search
        while value == array[m]:
            m += 1
            if (
                m > len(array) - 1
            ):  # Case if given point is the maximum, then no smallest starting points => return -1
                return -1
        return m  # Otherwise, return such point
    if l == r:
        if (
            array[l] > value
        ):  # If there is no exact match, check if the starting point found is greater than the given point. If so, return it.
            return l
        return (
            -1
        )  # If not, return not found. As value > array[m] will push l to m + 1 when array[m] < value < array[m + 1], such case must be value > array[len(array) - 1]
    elif value > array[m]:
        return modified_binary_search_sup(array, value, m + 1, r)
    else:
        return modified_binary_search_sup(array, value, l, m)


def fast_count_segments(starts, ends, points):
    cnt = list()
    index_begin, index_stop = 0, len(starts) - 1
    sort_starts = merge_sort(starts)  # Sort starting points of all segments
    sort_ends = merge_sort(ends)  # Sort ending points of all segments
    for p in points:
        p_sup = modified_binary_search_sup(
            sort_starts, p, index_begin, index_stop
        )  # For a point p, we find the smallest starting point above p.
        p_inf = modified_binary_search_inf(
            sort_ends, p, index_begin, index_stop
        )  # For a point p, we also find the largest ending point below p.
        num_segment_above, num_segment_below = (len(starts) - p_sup) * (p_sup > -1), (
            p_inf + 1
        ) * (
            p_inf > -1
        )  # The number of segment above p is total number of starting points - the index of the smallest starting point. The number of segment below p is the index of the largest ending point + 1 (python starts at index 0)
        num = len(starts) - (
            num_segment_above + num_segment_below
        )  # Boolean variables are introduced in case if no segment above/below a certain point, set to 0. So, total number of segments covering p = total number of segments - total number of excluded segments.
        cnt.append(num)
    return cnt


if __name__ == "__main__":
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n = data[0]
    m = data[1]
    starts = data[2 : 2 * n + 2 : 2]
    ends = data[3 : 2 * n + 2 : 2]
    points = data[2 * n + 2 :]
    cnt = fast_count_segments(starts, ends, points)
    for x in cnt:
        print(x, end=" ")
