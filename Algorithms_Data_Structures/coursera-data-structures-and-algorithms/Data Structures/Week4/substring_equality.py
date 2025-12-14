# python3
import sys
from random import randint

# Input Format. The first line contains a string s consisting of small Latin letters. The second line contains
# the number of queries q. Each of the next q lines specifies a query by three integers a, b, and l.
# Output Format. For each query, output “Yes” if s[a]s[a+1]...s[a+l-1] = s[b]s[b+1]...s[b+l-1] are equal, and “No” otherwise.


def poly_hash(
    S: str, p: int, x: int
) -> int:  # Standard implementation of polynomial hashing
    hash_num = [0]
    x_mod_p = [1]
    for i in range(len(S)):
        x_mod_p.append(
            (x * x_mod_p[-1]) % p
        )  # x_mod_p stores a sequence of hashing functions from S[0] to S[len(S) - 1]
    for i in range(len(S)):
        hash_num.append(
            (ord(S[i]) + x * hash_num[-1]) % p
        )  # hash_num stores a sequence of hashes from H(S[0]) to H(S[0]...S[len(S) - 1])
    return hash_num, x_mod_p


class Solver:
    def __init__(self, s):
        self.s = s  # input string
        self.p1, self.p2 = (
            10**9 + 17,
            10**9 + 37,
        )  # Two distinct big prime number for hashing
        self.x1, self.x2 = randint(1, self.p1 - 1), randint(
            1, self.p2 - 1
        )  # Two randomly chosen integers for hashing
        self.hash_num_1, self.x_mod_p_1 = poly_hash(
            s, self.p1, self.x1
        )  # Compute two different hashes to reduce collision probability
        self.hash_num_2, self.x_mod_p_2 = poly_hash(
            s, self.p2, self.x2
        )  # Compute two different hashes to reduce collision probability

    def ask(self, a, b, l):
        s1_h1 = (
            self.hash_num_1[a + l] - self.x_mod_p_1[l] * self.hash_num_1[a]
        ) % self.p1  # First hash for string 1
        s2_h1 = (
            self.hash_num_1[b + l] - self.x_mod_p_1[l] * self.hash_num_1[b]
        ) % self.p1  # First hash for string 2
        s1_h2 = (
            self.hash_num_2[a + l] - self.x_mod_p_2[l] * self.hash_num_2[a]
        ) % self.p2  # Second hash for string 1
        s2_h2 = (
            self.hash_num_2[b + l] - self.x_mod_p_2[l] * self.hash_num_2[b]
        ) % self.p2  # Second hash for string 2
        return (s1_h1 == s2_h1) & (
            s1_h2 == s2_h2
        )  # Return True (strings are equal) only if two hashed strings are equal to each other for two chosen hashed functions


s = sys.stdin.readline()
q = int(sys.stdin.readline())
solver = Solver(s)
for i in range(q):
    a, b, l = map(int, sys.stdin.readline().split())
    print("Yes" if solver.ask(a, b, l) else "No")
