# python3
import sys

# Task. For an integer parameter k and two strings t = t[0]t[1]...t[m-1] and p = p[0]p[1]...p[n-1], we say that
# p occurs in t at position i with at most k mismatches if the strings p and t[i:i+p) = t[i]t[i+1]...t[i+n-1] differ in at most k positions.
# Input Format. Every line of the input contains an integer k and two strings t and p consisting of lower case Latin letters.
# Output Format. For each triple (k, t, p), find all positions 0 <= i[1] < i[2] < ... < i[l] < |t| where p occurs in t
# with at most k mismatches. Output l and i[1], i[2], ... , i[l].


def poly_hash(S, p, x):  # Standard implementation of polynomial hashing
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


class hashed_string:
    def __init__(self, s):
        self.s = s  # input string
        self.p1, self.p2 = (
            263130836933693530167218012159999999,
            8683317618811886495518194401279999999,
        )  # Or 10 ** 12 + 37, 10** 12 + 19 to avoid time limit exceed problem
        self.x1, self.x2 = (
            17,
            37,
        )  # Use number with fewer digits to avoid memory limit exceed problem
        self.hash_num_1, self.x_mod_p_1 = poly_hash(
            s, self.p1, self.x1
        )  # Do polynomial hashing two times with different primes, it costs O(length(string))
        self.hash_num_2, self.x_mod_p_2 = poly_hash(s, self.p2, self.x2)

    def hashed_substring(
        self, start, end
    ):  # Return hash values for substring given start and end indices (both inclusively)
        length = end - start + 1
        h1 = (
            self.hash_num_1[start + length]
            - self.x_mod_p_1[length] * self.hash_num_1[start]
        ) % self.p1  # First hash for string 1
        h2 = (
            self.hash_num_2[start + length]
            - self.x_mod_p_2[length] * self.hash_num_2[start]
        ) % self.p2  # Second hash for string 1
        return (h1, h2)


def modified_bs(
    hashed_p, hashed_t, pattern, substr_text, i, mismatch_count, left, right, k
):
    # A modifed binary search for mismatch between substring of t and pattern
    if right >= left:
        mid = (left + right) // 2
        if (
            substr_text[mid] != pattern[mid]
        ):  # If mid characters are not the same for both string, there is a mismatch
            mismatch_count += 1

        if hashed_t.hashed_substring(
            i + left, i + mid - 1
        ) != hashed_p.hashed_substring(
            left, mid - 1
        ):  # Compare the hash values for string in [left, mid - 1]. Do no do recursion if hashes are mismatch
            mismatch_count = modified_bs(
                hashed_p,
                hashed_t,
                pattern,
                substr_text,
                i,
                mismatch_count,
                left,
                mid - 1,
                k,
            )

        if hashed_t.hashed_substring(
            i + mid + 1, i + right
        ) != hashed_p.hashed_substring(
            mid + 1, right
        ):  # Compare the hash values for string in [mid + 1, rigiht]. Do no do recursion if hashes are mismatch
            mismatch_count = modified_bs(
                hashed_p,
                hashed_t,
                pattern,
                substr_text,
                i,
                mismatch_count,
                mid + 1,
                right,
                k,
            )

        if (
            mismatch_count > k
        ):  # Early stoppling if total mismatch exceeds given bound, k
            return mismatch_count
    return mismatch_count  # Return the number of mismatch


def solve(k, text, pattern):
    len_p, len_t, results = (
        len(pattern),
        len(text),
        list(),
    )  # results list store the starting indices of match cases in text with tolerance level of k
    hashed_t, hashed_p = hashed_string(text), hashed_string(
        pattern
    )  # Hash both strings twice
    for i in range(
        0, len_t - len_p + 1
    ):  # Loop the starting index of text, we compare substrings t[0,...,len(p)], ..., t[len(t) - len(p) + 1, len(t) + 1] with pattern
        substr_text, mismatch_count = (
            text[i : (i + len_p)],
            0,
        )  # Update substring of text as substr_text and reset the number of mismatch to 0 for each new substring
        left, right = (
            0,
            len_p - 1,
        )  # Initialize left and right for modified binary search
        mismatch_count = modified_bs(
            hashed_p, hashed_t, pattern, substr_text, i, mismatch_count, left, right, k
        )
        if (
            mismatch_count <= k
        ):  # If mismatch total is less than or equal to k, append the index
            results.append(i)
    return results


for line in sys.stdin.readlines():
    k, t, p = line.split()
    ans = solve(int(k), t, p)
    print(len(ans), *ans)
