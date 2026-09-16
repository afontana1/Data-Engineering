# python3
import sys

# Modify original trie building to account for overlapping patterns
def build_trie(patterns):
    tree = dict({0: dict()})
    node_idx = 0

    for pattern in patterns:
        currentNode = 0

        for i in range(len(pattern)):
            currentSymbol = pattern[i]

            if currentSymbol in tree[currentNode]:
                currentNode = tree[currentNode][currentSymbol]

            else:
                node_idx += 1
                tree.update({node_idx: dict()})
                tree[currentNode][currentSymbol] = node_idx
                currentNode = node_idx

            if (
                i == len(pattern) - 1
            ):  # If the current character is the last character of the pattern
                tree[currentNode][
                    "$"
                ] = -1  # Add '$' to the dictionary under the current node with value -1

    return tree


# Modify prefix matching algorithm to account for overlapping patterns
def prefix_trie_matching(text, trie):
    text += "$"
    i, v = 0, 0
    symbol = text[i]  # Start with the first character of the text

    while True:
        if symbol in trie[v]:
            v = trie[v][symbol]

            if (
                "$" in trie[v]
            ):  # Also return True (pattern is found) if '$' is found but not at the leaf
                return True

            elif len(trie[v]) == 0:  # Return True at the leaf
                return True

            # Update
            i += 1
            symbol = text[i]

        else:
            return False


# Reuse the code from trie_matching.py
def solve(text, n, patterns):
    trie = build_trie(patterns)
    result = []
    j = 0
    while len(text) > j:
        if prefix_trie_matching(text[j:], trie) == True:
            result.append(j)
        j += 1
    return result


text = sys.stdin.readline().strip()
n = int(sys.stdin.readline().strip())
patterns = []
for i in range(n):
    patterns += [sys.stdin.readline().strip()]

ans = solve(text, n, patterns)
sys.stdout.write(" ".join(map(str, ans)) + "\n")
