# Uses python3
import sys


def build_trie(patterns):
    # Initialize the root with index 0
    tree = dict({0: dict()})
    node_idx = 0

    # Loop each string in patterns
    for pattern in patterns:
        currentNode = 0  # Start from the root

        # Loop each character in string
        for i in range(len(pattern)):
            currentSymbol = pattern[i]  # currentSymbol = the current character

            # If the current character is found in the trie, go to its child node
            if currentSymbol in tree[currentNode]:
                currentNode = tree[currentNode][currentSymbol]

            # Otherwise, a new node should be created and go to the new node
            else:
                node_idx += 1
                tree.update({node_idx: dict()})
                tree[currentNode][currentSymbol] = node_idx
                currentNode = node_idx

    return tree


if __name__ == "__main__":
    patterns = sys.stdin.read().split()[1:]
    tree = build_trie(patterns)
    for node in tree:
        for c in tree[node]:
            print("{}->{}:{}".format(node, tree[node][c], c))
