def find_monotonically_decreasing_subsequences(lst):
    subsequences = []
    current_subsequence = [lst[0]]

    for i in range(1, len(lst)):
        if lst[i] <= current_subsequence[-1]:
            current_subsequence.append(lst[i])
        else:
            subsequences.append(current_subsequence)
            current_subsequence = [lst[i]]

    subsequences.append(current_subsequence)  # Append the last subsequence

    return [subseq for subseq in subsequences if len(subseq) > 1]

# Example usage:
numbers = [8, 7, 5, 6, 3, 4, 2, 1]
result = find_monotonically_decreasing_subsequences(numbers)
print("Monotonically decreasing subsequences:", result)

def find_monotonically_increasing_subsequences(lst):
    subsequences = []
    current_subsequence = [lst[0]]

    for i in range(1, len(lst)):
        if lst[i] > current_subsequence[-1]:
            current_subsequence.append(lst[i])
        else:
            if len(current_subsequence) > 1:
                subsequences.append(current_subsequence)
            current_subsequence = [lst[i]]

    if len(current_subsequence) > 1:
        subsequences.append(current_subsequence)

    return subsequences

# Example usage:
numbers = [1, 3, 2, 4, 6, 5, 7, 8]
result = find_monotonically_increasing_subsequences(numbers)
print("Monotonically increasing subsequences:", result)


def find_monotonically_increasing_subsequences(lst):
    subsequences = []
    current_subsequence = [0]  # Start index

    for i in range(1, len(lst)):
        if lst[i] > lst[current_subsequence[-1]]:
            current_subsequence.append(i)
        else:
            if len(current_subsequence) > 1:
                subsequences.append(current_subsequence)
            current_subsequence = [i]

    if len(current_subsequence) > 1:
        subsequences.append(current_subsequence)

    return subsequences

# Example usage:
numbers = [1, 3, 2, 4, 6, 5, 7, 8]
result = find_monotonically_increasing_subsequences(numbers)
print("Monotonically increasing subsequences:", result)


def find_monotonically_increasing_subsequences(lst, start=0, end=None):
    if end is None:
        end = len(lst)
    subsequences = []

    if end - start < 2:
        return []

    current_subsequence = [start]

    for i in range(start + 1, end):
        if lst[i] > lst[current_subsequence[-1]]:
            current_subsequence.append(i)
        else:
            if len(current_subsequence) > 1:
                subsequences.append(current_subsequence)
            current_subsequence = [i]

    if len(current_subsequence) > 1:
        subsequences.append(current_subsequence)

    subseq_indices = []
    for subseq in subsequences:
        subseq_indices.extend(subseq)

    return subsequences + find_monotonically_increasing_subsequences(lst, subseq_indices[-1], end)

# Example usage:
numbers = [1, 3, 2, 4, 6, 5, 7, 8]
result = find_monotonically_increasing_subsequences(numbers)
print("Monotonically increasing subsequences:", result)
