# Uses python3
import sys

# Task. Given two integers a and b, find their least common multiple.
# Input Format. The two integers a and b are given in the same line separated by space.
# Constraints. 1 <= a, b <= 107.
# Output Format. Output the least common multiple of a and b.


def gcd_naive(a, b):
    # Standard implementation of the Euclid algorithm
    if a == 0:
        return b
    elif b == 0:
        return a
    else:
        c, d = min(a, b), max(a, b)
        a, b = c, d % c
        return gcd_naive(a, b)


def lcm_naive(a, b):
    if (a != 0) or (b != 0):
        # If not both are 0, gcd != 0 and we can return a quotient.
        # Let gcd(a, b) = g. Then, a = g*m and b = g*n where gcd(m, n) = 1.
        # Otherwise, we can find g' > g and reject g is gcd.
        # So, by definition of least common multiple, lcm = g*n*m = (g*m)*(g*n)/g = (a*b)/g.
        gcd = gcd_naive(a, b)
        return int((a * b) / gcd)
    else:
        # If a and b are 0, then we cannot do division and return 0
        return 0


if __name__ == "__main__":
    input = sys.stdin.read()
    a, b = map(int, input.split())
    print(lcm_naive(a, b))
