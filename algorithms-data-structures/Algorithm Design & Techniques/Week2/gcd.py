# Uses python3
import sys

# Task. Given two integers a and b, find their greatest common divisor.
# Input Format. The two integers a, b are given in the same line separated by space.
# Constraints. 1 <= a, b <= 2 · 109.
# Output Format. Output GCD(a, b).


def gcd_naive(a, b):
    if a == 0:
        # Trivial case: a = 0 implies a (mod b) = 0
        return b
    elif b == 0:
        # Trivial case: b = 0 implies b (mod a) = 0
        return a
    else:
        # Euclid algorithm: if c | d, then d % c = 0 and b = 0 which implies c is gcd.
        # If c does not divide d, then d % c = remainder from d divided by c. Repeat this process until c | d.
        # The worst case is c = 1. In this case, d % c = 0 and the algorithm returns 1.
        c, d = min(a, b), max(a, b)
        a, b = c, d % c
        return gcd_naive(a, b)


if __name__ == "__main__":
    input = sys.stdin.read()
    a, b = map(int, input.split())
    print(gcd_naive(a, b))
