# Uses python3
import sys

# Task. Compose the largest number out of a set of integers.
# Input Format. The first line of the input contains an integer n. The second line contains integers
# a[1], a[2], . . . , a[n].
# Output Format. Output the largest number that can be composed out of a[1], a[2], . . . , a[n].

# Greedy algorithm: We pick number a[j] such that a[j]a[i] > a[i]a[j] over the list, and r = a[k[1]]...a[k[l]]a[j]
# We need show that: if a[j]a[i] > a[i]a[j] where i != j, then a[k[s]]...a[j]a[i].....a[k[l]] > a[k[s]]....a[i]a[j]....a[k[l]]
# If a[j]a[i] > a[i]a[j], then (a[j]a[i])*10^d > (a[i]a[j])^10^d, and adding constant does not change optimality
# So, it's a safe move


def greater(a, b):
    is_greater = int(str(a) + str(b)) >= int(str(b) + str(a))  # a[j]a[i] > a[i]a[j]
    return is_greater


def insertion_sort(a):
    # An insertion sort: every element in list are sorted in order defined by greater(). It takes O(n^2).
    i = 0
    while i < len(a):
        j = i
        while j > 0 and greater(a[j], a[j - 1]):
            a[j - 1], a[j] = (
                a[j],
                a[j - 1],
            )  # If a[j]a[j - 1] > a[j - 1]a[j], then swap a[j] to left
            j -= 1
        i += 1


def largest_number(a):
    insertion_sort(a)  # Apply a sort
    num = "".join(
        list(map(str, a))
    )  # Join integers together to form the largest number (in string)
    return num


if __name__ == "__main__":
    input = sys.stdin.read()
    data = input.split()
    a = data[1:]
    print(largest_number(a))
