import random


def quickSort(arr):
    if len(arr) < 1:
        return arr
    small, equal, large = [], [], []
    point = arr[random.randint(0, len(arr) - 1)]
    for num in arr:
        if num < point:
            small.append(num)
        elif num > point:
            large.append(num)
        else:
            equal.append(num)
    return quickSort(small) + equal + quickSort(large)


x = [4, 5, 2, 8, 5, 6, 3, 5, 2]


def getList(length, size):
    return [random.randint(0, size) for i in range(length)]


for i in range(10):
    data = getList(20, 20)
    print(data)
    print(quickSort(data))
    print("-------")
