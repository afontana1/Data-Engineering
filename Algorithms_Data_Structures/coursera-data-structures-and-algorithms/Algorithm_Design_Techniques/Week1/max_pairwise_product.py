# python3
# Week 1 - Maximum Pairwise Product Problem
# Find the maximum product of two distinct numbers in a sequence of non-negative integers.
# Input: A sequence of non-negative integers.
# Output: The maximum value that can be obtained by multiplying two different elements from the sequence.


def max_pairwise_product(numbers):
    n = len(numbers)
    numbers_copy = numbers.copy()

    # A linear search for the first largest number in a list
    index = 0
    for i in range(1, n):
        if numbers_copy[i] > numbers_copy[index]:
            index = i

    # If the first element is the largest, then we start to search the next largest number starting from the second element
    # If not, we start to search the next largest number starting from the first element
    # Otherwise, numbers_copy[i] < numbers_copy[index_new] at i == 1 and index_new == 0
    index_new = 0
    if index == 0:
        index_new = 1

    for i in range(0, n):
        if (i != index) and (numbers_copy[i] > numbers_copy[index_new]):
            # First condition (i != index): Ensure distinct elements
            # Second condition (numbers_copy[i] > numbers_copy[index_new]): A linear searach for the largest element
            index_new = i
    max_product = (
        numbers_copy[index] * numbers_copy[index_new]
    )  # Return the product of two elements

    return max_product


if __name__ == "__main__":
    input_n = int(input())
    input_numbers = [int(x) for x in input().split()]
    print(max_pairwise_product(input_numbers))
