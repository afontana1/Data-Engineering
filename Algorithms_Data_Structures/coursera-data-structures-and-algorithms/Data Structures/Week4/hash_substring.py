# python3
from random import randint

# Task. In this problem your goal is to implement the Rabin–Karp’s algorithm for searching the given pattern in the given text.
# Input Format. There are two strings in the input: the pattern P and the text T.
# Output Format. Print all the positions of the occurrences of P in T in the ascending order. Use 0-based indexing of positions in the the text T.


def read_input():  # Read input
    return (input().rstrip(), input().rstrip())


def print_occurrences(output):  # Join output string list into a single string
    print(" ".join(map(str, output)))


def poly_hash(
    S: str, p: int, x: int
) -> int:  # Standard implementation of polynomial hashing
    """hash_num: int"""
    hash_num = 0
    for i in reversed(range(len(S))):
        hash_num = ((hash_num * x) + ord(S[i])) % p
    return hash_num


def precompute_hashes(
    T: str, P: int, p: int, x: int
) -> list:  # Precompute hashing for Rabin-Karp algorithm
    """H: list, y: int"""
    last_index = len(T) - P
    H, S, y = (last_index + 1) * [0], T[last_index : len(T)], 1
    H[last_index] = poly_hash(S, p, x)
    for i in range(P):
        y = (y * x) % p
    for i in reversed(range(len(T) - P)):
        H[i] = (
            x * H[i + 1] + ord(T[i]) - y * ord(T[i + P])
        ) % p  # Recurrence relation for hashing (https://en.wikipedia.org/wiki/Rolling_hash)
    return H


def rabin_karp(
    P: str, T: str
) -> list:  # Standard implementation of Rabin-Karp algorithm
    p = 10**9 + 19
    x, result = randint(1, p - 1), list()
    p_hash = poly_hash(P, p, x)  # Compute hash for pattern
    H = precompute_hashes(
        T, len(P), p, x
    )  # Precompute all hashes for text (T) with length equal to pattern (P)
    for i in range(
        len(T) - len(P) + 1
    ):  # Compare hashes, if same hashes, then compare string and append the matching results (starting index)
        if p_hash != H[i]:
            continue
        if T[i : (i + len(P))] == P:
            result.append(i)
    return result


if __name__ == "__main__":
    print_occurrences(rabin_karp(*read_input()))
