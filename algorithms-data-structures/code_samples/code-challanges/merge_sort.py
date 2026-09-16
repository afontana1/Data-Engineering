def merge(left, right):
    out = []
    while len(left) != 0 and len(right) != 0:
        if left[0] < right[0]:
            out.append(left[0])
            left.remove(left[0])
        else:
            out.append(right[0])
            right.remove(right[0])
    if len(left) == 0:
        out.extend(right)
    else:
        out.extend(left)
    return out


def mergeSort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    return merge(mergeSort(arr[:mid]), mergeSort(arr[mid:]))


import random


def tests(select, max):
    return [random.randint(0, select) for _ in range(max)]


for _ in range(10):
    print(mergeSort(tests(10, 50)))
