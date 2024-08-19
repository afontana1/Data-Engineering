# Uses python3
import sys

# Task. Check whether a given directed graph with n vertices and m edges contains a cycle.
# Input Format. A graph is given in the standard format.
# Output Format. Output 1 if the graph contains a cycle and 0 otherwise.


def explore(v, adj, visit):  # a depth first search
    visit[v] += 1  # as node v is visited, add 1
    for w in adj[v]:
        if (
            visit[w] < 2
        ):  # if visit of neighborhood is at most 1, we continue the depth first search. Otherwise, there is a cycle (visit[w] >= 2) and the recursion is infinite
            explore(w, adj, visit)
    return visit


def reach(adj, x, y):  # standard implmentation of reachable. see reachability.py
    visit = len(adj) * [0]
    result = explore(x, adj, visit)
    if result[y] > 1:  # if visit[i] >= 2, there is a cycle with node i
        return 1
    return 0


def acyclic(adj):
    for i in range(len(adj)):
        bool_cycle = reach(
            adj, i, i
        )  # If there is a cycle which consists of i-th node, it must be reachable to itself
        if bool_cycle == 1:
            return 1  # return 1 if there is a cycle, 0 if not.
    return 0


if __name__ == "__main__":
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0 : (2 * m) : 2], data[1 : (2 * m) : 2]))
    adj = [[] for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
    print(acyclic(adj))
