# python3
import sys

# Reuse trie building code in trie.py
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
    return tree


# Prefix matching using trie
def prefix_trie_matching(text, trie):
    text += "$"  # Append dollar sign which indicates the end of text
    i, v = 0, 0
    symbol = text[i]  # Start from the first character of text

    while True:
        if (
            symbol in trie[v]
        ):  # If the character is found in the trie, go to the next layer of the trie
            v = trie[v][symbol]
            if (
                len(trie[v]) == 0
            ):  # There is a match if it reaches the bottom of the trie, return True
                return True
            i += 1  # Update and match the next word in text against the trie
            symbol = text[i]
        else:  # If some character in text is not found in the corresponding layer of the trie, mismatch, return False
            return False


def solve(text, n, patterns):
    trie = build_trie(patterns)  # Build a trie for the patterns
    # Pattern matching by "moving" the trie on substring of text, text[j:]
    result = []
    j = 0
    while len(text) > j:
        if prefix_trie_matching(text[j:], trie) == True:
            result.append(j)  # If there is a match, store the starting index
        j += 1  # Update the moving index

    return result


text = sys.stdin.readline().strip()
n = int(sys.stdin.readline().strip())
patterns = []

for i in range(n):
    patterns += [sys.stdin.readline().strip()]

ans = solve(text, n, patterns)
sys.stdout.write(" ".join(map(str, ans)) + "\n")
