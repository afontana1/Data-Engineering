def select_sort(arr):
    # loop through n times
    for i in range(len(arr)):
        pos = i
        # check if the j+1th element is smaller
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[pos]:
                # if it is, make that the ith position
                pos = j
        # swap the elements
        arr[pos], arr[i] = arr[i], arr[pos]

    return arr


def recurse_selectSort(arr, srted=[]):
    if len(arr) < 1:
        return srted
    else:
        srted.append(min(arr))
        arr.remove(min(arr))
        return recurse_selectSort(arr, srted)


if __name__ == "__main__":
    import random

    x = [random.randrange(0, 200, 1) for i in range(0, 100)]
    print(select_sort(x))
