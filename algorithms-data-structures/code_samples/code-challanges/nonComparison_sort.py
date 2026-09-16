def countSort(arr):
    """
    Count the number of occurences for each element
    in the array

    The index position is the number, the value
    is the count

    Add the number to an output array the number of times
    it appears in array
    """

    # initialize counts array
    counts = [0] * (max(arr) + 1)
    for num in arr:
        counts[num] += 1

    # get number index(number) and counts associated with it
    temp = []
    for idx, count in enumerate(counts):
        if count != 0:
            temp.append((idx, count))

    # initialize output array
    out = []
    for tup in temp:
        # get the count
        count_ = tup[1]
        # add it to the output array n times
        while count_ > 0:
            out.append(tup[0])
            count_ -= 1
    return out


arr = [13, 7, 4, 0, 2, 45, 6, 2, 2, 2]


def lessEfficient(arr):

    # initialize counts array
    counts = [0] * (max(arr) + 1)
    for num in arr:
        counts[num] += 1

    # get number index(number) and counts associated with it
    temp = []
    for idx, count in enumerate(counts):
        if count != 0:
            temp.append((idx, count))

    # create list of lists, where each list is length == num of occurences
    out = []
    for tup in temp:
        out.append([tup[0]] * tup[1])

    # requires nested list comp to unpack the tuples
    return [num for lst in out for num in lst]
