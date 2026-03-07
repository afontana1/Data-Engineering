# Uses python3
import sys

# Task. Given two non-negative integers m and n, where m <= n, find the last digit of the sum F[m] + F[m + 1] + ... + F[n].
# Input Format. The input consists of two non-negative integers m and n separated by a space.
# Constraints. 0 <= m <= n <= 10^14.
# Output Format. Output the last digit of F[m] + F[m + 1] + ... + F[n].


def get_fibonacci_huge_naive(n, m):
    # Return F[n] mod m
    if n <= 1:
        return n
    F = [0, 1]
    for i in range(2, n + 1):
        F.append((F[i - 1] + F[i - 2]) % m)
        if F[i - 1] == 0 and F[i] == 1:
            return F[n % len(F[: (i - 1)])]
    return F[-1]


def fibonacci_sum_naive(n):
    # Return (F[0] + ... + F[n]) mod 10
    last_digit = get_fibonacci_huge_naive(n + 2, 10) - 1
    if last_digit < 0:
        last_digit += 10
    return last_digit


def fibonacci_partial_sum_naive(from_fib, to_fib):
    # Return (F[m] + F[m + 1] + ... + F[n]) mod 10
    # By basic modular arithmetic, ((F[0] + ... + F[n]) - (F[0] + ... + F[m - 1])) mod 10 =
    # ((F[0] + ... + F[n]) mod 10 - (F[0] + ... + F[m - 1]) mod 10) mod 10
    # We need to express difference in partial sums in this way to avoid overflowing problem of integer.
    sum_fib = (fibonacci_sum_naive(to_fib) - fibonacci_sum_naive(from_fib - 1)) % 10
    return sum_fib


if __name__ == "__main__":
    input = sys.stdin.read()
    from_, to = map(int, input.split())
    print(fibonacci_partial_sum_naive(from_, to))
