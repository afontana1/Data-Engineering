# Uses python3
import sys

# Task. Given an integer n, find the last digit of the sum F[0] + F[1] + · · · + F[n].
# Input Format. The input consists of a single integer n.
# Constraints. 0 <= n <= 10^14.
# Output Format. Output the last digit of F[0] + F[1] + ... + F[n].


def get_fibonacci_huge_naive(n, m):
    if n <= 1:
        return n
    F = [0, 1]
    for i in range(2, n + 1):
        F.append((F[i - 1] + F[i - 2]) % m)
        if F[i - 1] == 0 and F[i] == 1:
            return F[n % len(F[: (i - 1)])]
    return F[-1]


def fibonacci_sum_naive(n):
    # The last digit of F[0] + F[1] + ... + F[n] is (F[0] + F[1] + ... + F[n]) mod 10
    # Mathematical induction: F[0] mod 10 = 0 and F[2] (mod 10) - 1 = 0
    # (F[0] + F[1]) mod 10 = 1 mod 10 = 1  and F[3] (mod 10) - 1 = 1
    # Suppose it's true that (F[0] + ... + F[k - 1]) mod 10 = F[k + 1] (mod 10) - 1.
    # (F[0] + ... + F[k]) mod 10 = (F[k + 1] (mod 10) - 1) + F[k] (mod 10) = (F[k] + F[k + 1]) mod 10 - 1 = F[k + 2] (mod 10) - 1
    # By M.I., we proved that F[0] + F[1] + ... + F[n] = F[n + 2] (mod 10) - 1,
    # which can be computed using get_fibonacci_huge_naive(n + 2, 10) - 1
    last_digit = get_fibonacci_huge_naive(n + 2, 10) - 1
    # Special case: F[n + 2] mod 10 = 0. Then, last digit = -1 which does not make sense.
    # By basic modular arithmetic, we add back 10 to get 9.
    if last_digit < 0:
        last_digit += 10
    return last_digit


if __name__ == "__main__":
    input = sys.stdin.read()
    n = int(input)
    print(fibonacci_sum_naive(n))
