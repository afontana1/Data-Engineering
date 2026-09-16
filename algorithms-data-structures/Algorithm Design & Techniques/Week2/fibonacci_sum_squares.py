# Uses python3
from sys import stdin

# Task. Compute the last digit of F[0]^2 + F[1]^2 + ... + F[n]^2
# Input Format. Integer n.
# Constraints. 0 <= n <= 10^14.
# Output Format. The last digit of F[0]^2 + F[1]^2 + ... + F[n]^2


def get_fibonacci_huge_naive(n, m):
    if n <= 1:
        return n
    F = [0, 1]
    for i in range(2, n + 1):
        F.append((F[i - 1] + F[i - 2]) % m)
        if F[i - 1] == 0 and F[i] == 1:
            return F[n % len(F[: (i - 1)])]
    return F[-1]


def fibonacci_sum_squares_naive(n):
    # By Mathematical Induction, F[0]^2 + F[1]^2 = 1 and F[1]*F[2] = 1*1 = 1. So, F[0]^2 + F[1]^2 = F[1]*F[2].
    # F[k]*F[k + 1] = F[k]*F[k] + F[k]*F[k - 1] by recurrence relation
    # = F[0]^2 + ... + F[k - 1]^2 + F[k]^2 -- Proof is completed
    # Next, (F[0]^2 + F[1]^2 + ... + F[n]^2) mod 10 = (F[n]*F[n + 1]) mod 10 = (F[n] mod 10)*(F[n + 1] mod 10)
    fib_num_height = get_fibonacci_huge_naive(n, 10)
    fib_num_width = get_fibonacci_huge_naive(n + 1, 10)
    return (fib_num_height * fib_num_width) % 10


if __name__ == "__main__":
    n = int(stdin.read())
    print(fibonacci_sum_squares_naive(n))
