# Uses python3
import sys

# Task. Given an undirected graph with n vertices and m edges, compute the number of connected components in it.
# Input Format. A graph is given in the standard format.
# Output Format. Output the number of connected components.


def explore(v, adj, visit):  # See reachability.py
    visit[v] = 1
    for w in adj[v]:
        if visit[w] == 0:
            explore(w, adj, visit)


def number_of_components(adj):
    result = 0  # The number of connected components
    visit = len(adj) * [0]
    for v in range(len(adj)):
        if visit[v] == 0:
            explore(v, adj, visit)
            result += (
                1  # After a depth first search, increase the connected components by 1
            )
    return result


if __name__ == "__main__":
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0 : (2 * m) : 2], data[1 : (2 * m) : 2]))
    adj = [[] for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
        adj[b - 1].append(a - 1)
    print(number_of_components(adj))
