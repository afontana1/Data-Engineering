# Uses python3
# Task. Given an integer n, find the 𝑛th Fibonacci number F[n].
# Input Format. The input consists of a single integer n.
# Constraints. 0 <= n <= 45.
# Output Format. Output F[n].


def calc_fib(n):
    F = []  # Initialize for an empty list
    for i in range(n + 1):  # Up to n
        if i == 0:
            F.append(0)  # Base case for recurrence relation
        elif i == 1:
            F.append(1)  # Base case for recurrence relation
        else:
            F.append(
                F[i - 1] + F[i - 2]
            )  # Recurrence relation F[n] = F[n-1] + F[n-2] with F[0] = 0 and F[1] = 1
    return F[-1]  # Return the last element using -1 index


n = int(input())
print(calc_fib(n))
