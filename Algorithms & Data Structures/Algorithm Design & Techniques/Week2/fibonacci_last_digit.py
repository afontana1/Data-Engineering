# Uses python3
# Task. Given an integer n, find the last digit of the n-th Fibonacci number F[n] (that is, F[n] mod 10).
# Input Format. The input consists of a single integer n.
# Constraints. 0 <= n <= 107.
# Output Format. Output the last digit of F[n].
import sys


def get_fibonacci_last_digit_naive(n):
    F = []
    for i in range(n + 1):  # Up to n
        if i == 0:
            F.append(0)  # Base case: F[0] = 0
        elif i == 1:
            F.append(1)  # Base case: F[1] = 1
        else:
            F.append(
                (F[i - 1] + F[i - 2]) % 10
            )  # Basic modular arithmetic: a (mod 10) + b (mod 10) = (a + b) (mod 10)
    return F[-1]  # Return the last element of a list by index -1


if __name__ == "__main__":
    input = sys.stdin.read()
    n = int(input)
    print(get_fibonacci_last_digit_naive(n))
