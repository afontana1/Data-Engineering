# Uses python3
import sys

# Task. Given two integers n and m, output F[n] mod n (that is, the remainder of F[n] when divided by m).
# Input Format. The input consists of two integers n and m given on the same line (separated by a space).
# Constraints. 1 <= n <= 1014, 2 <= m <= 103.
# Output Format. Output F[n] mod m.

# This is true in general: for any integer m >= 2, the sequence F[n] mod m is periodic. The period always
# starts with 01 and is known as Pisano period.


def get_fibonacci_huge_naive(n, m):
    if n <= 1:
        # If n == 1, then it's trivial as n (mod m) = n for all m >= 2
        return n

    F = []
    for i in range(n + 1):
        if i == 0:
            F.append(0)  # Base case: F[0] = 0
        elif i == 1:
            F.append(1)  # Base case: F[1] = 1
        else:
            F.append(
                (F[i - 1] + F[i - 2]) % m
            )  # We append F[n] mod m at each iteration
        if F[i - 1] == 0 and F[i] == 1 and i > 1:
            # When Pisano period is observed, we delete F[i] and F[i - 1] and get F as a list of Pisano period.
            # F  = [0, 1, x1, x2, x3, x4...] where x1, x2, x3, x4,... cannot contain pattern 0, 1.
            # This period will keep repeating itself until the n-th iteration.
            del F[i]
            del F[i - 1]
            # F[n] (mod m) = k * period length + remainder
            # So, n (mod period length) = remainder, at which n-th iteration stops with value F[n] mod m.
            index = n % len(F)
            return F[index]
    # In case the cycle haven't ended, we can output the last index directly at which the n-th iteration stops.
    return F[-1]


# Short version of above code
# def get_fibonacci_huge_naive(n, m):
#     if n <= 1:
#         return n
#     F = [0, 1]
#     for i in range(2, n + 1):
#         F.append((F[i - 1] + F[i - 2]) % m)
#         if F[i - 1] == 0 and F[i] == 1:
#             return(F[n % len(F[:(i - 1)])])
#     return F[-1]

if __name__ == "__main__":
    input = sys.stdin.read()
    n, m = map(int, input.split())
    print(get_fibonacci_huge_naive(n, m))
