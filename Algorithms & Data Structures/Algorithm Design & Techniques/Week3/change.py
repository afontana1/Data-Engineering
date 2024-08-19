# Uses python3
import sys

# Task. The goal in this problem is to find the minimum number of coins needed to change the input value
# (an integer) into coins with denominations 1, 5, and 10.
# Input Format. The input consists of a single integer m.
# Constraints. 1 <= m <= 103.
# Output Format. Output the minimum number of coins with denominations 1, 5, 10 that changes m.


def get_change(m):
    # Greedy algorithm: First change with coins with denomination 10
    # Then, change with coins with denomination 5.
    # At last, change with coins with denomination 1.
    # If we have K dollars. Either K >= 10, 5 <= K < 10 and 1 <= K < 5.
    # Case 1: Changing K into coins with denomination 10 is obviously better than changing K into coins with denominations 5 or 1.
    # Case 2: We cannot change K into coins with denomination 10. It is obvious that changing K into coins with denominations 5 yield less coins.
    # Case 3: Trivial.
    # In all three cases, the changing coins with the largest denomination available is a safe move.
    after_ten = m % 10  # Total amount after changing with coin 10
    ten_count = (m - after_ten) / 10  # How many coin 10 should be changed
    after_five = (
        after_ten % 5
    )  # Total amount after changing with coin 5, it can be changed with coin 1
    five_count = (after_ten - after_five) / 5  # How many coin 5 should be changed
    m = int(after_five + five_count + ten_count)
    return m


if __name__ == "__main__":
    m = int(sys.stdin.read())
    print(get_change(m))
