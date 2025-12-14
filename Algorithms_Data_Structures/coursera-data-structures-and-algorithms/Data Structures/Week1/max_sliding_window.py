# python3
from collections import deque

# Input Format. The first line contains an integer n, the second line contains n integers a[1], ..., a[n] separated
# by spaces, the third line contains an integer m.
# Output Format. Output max{a[0], . . . , a[i+m-1]} for every 1 <= i <= n ??m + 1.


def max_sliding_window_naive(sequence, m):
    window, max_seq = (
        deque(),
        list(),
    )  # window stores indices of array element in the window, max_seq stores output
    temp_val = sequence[0]
    if (
        len(sequence) == 1 or m == 1
    ):  # Trivial case: if there is one number or window size of 1, results = input
        return sequence
    for i, current_val in enumerate(
        sequence
    ):  # Otherwise, if all elements are the same, results = input[1:size(results)].
        if i > 0:
            if current_val != temp_val:
                break
            continue
        if i == len(sequence) - 1:
            return sequence[: len(sequence) - m + 1]
    for j, current_val in enumerate(sequence):  # Otherwise, we apply standard procedure
        if j == 0:  # Append the index of the first element of input array and proceed
            window.append(j)
            continue
        else:
            while (
                current_val > sequence[window[-1]]
            ):  # If the deque is not empty, and the new coming value is greater than previous max value
                # When j == 1: compare sequence[0] and sequence[1]. Let sequence[0] > sequence[1]
                # When j == 2: compare sequence[2] and sequence[1] if m == 2. Let sequence[1] < sequence[2]. Then, window = deque([0])
                window.pop()
                if len(window) == 0:
                    break
            window.append(
                j
            )  # Append the index of the current element of input array and proceed. Now window = deque([0, 2])
            if (
                window[0] < j - m + 1
            ):  # The index of the maximum element is out of range, pop it
                window.popleft()  # Now window = deque([2])
            if (
                j + 1 >= m
            ):  # Start to append maximum value when index + 1 goes beyond window size
                max_seq.append(sequence[window[0]])
    return max_seq


if __name__ == "__main__":
    n = int(input())
    input_sequence = [int(i) for i in input().split()]
    assert len(input_sequence) == n
    window_size = int(input())

    print(*max_sliding_window_naive(input_sequence, window_size))

# Problem confusing me:
# If we consider data = [1, 1, 1, 1, 1, 1, 1, 1, ...., 1, 5]
# We need a while loop to compare sequence[j] and sequence[window[-1]] until 1) window is empty or 2) sequence[window[-1]] < sequence[j].
# There should be at most O(m) comparison. Why isn't such algorithm O(m*n) but O(n)? I am a bit confusing about it and nonetheless it works much faster than naive solution.
