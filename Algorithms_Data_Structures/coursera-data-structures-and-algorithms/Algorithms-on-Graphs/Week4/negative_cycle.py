# Uses python3
import sys

# Task. Given an directed graph with possibly negative edge weights and with n vertices and m edges, check
# whether it contains a cycle of negative weight.
# Input Format. A graph is given in the standard format.
# Output Format. Output 1 if the graph contains a cycle of negative weight and 0 otherwise.


def negative_cycle(adj, cost):
    n = len(adj)
    inf = float("inf")
    dist = [inf] * n
    # a standard implementation of Bellman-Ford algorithm in O(|V||E|) time
    for j in range(n):  # Loop |V| times
        for u in range(n):  # Run all edges
            if len(adj[u]) != 0:
                for i in range(len(adj[u])):
                    v = adj[u][i]
                    if dist[v] > dist[u] + cost[u][i]:  # Edge relaxation
                        dist[v] = dist[u] + cost[u][i]
                        if (
                            j == n - 1
                        ):  # If there is edge relaxation in the |V|-th iteration, it imples a negative cycle
                            return 1
    return 0


if __name__ == "__main__":
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(
        zip(zip(data[0 : (3 * m) : 3], data[1 : (3 * m) : 3]), data[2 : (3 * m) : 3])
    )
    data = data[3 * m :]
    adj = [[] for _ in range(n)]
    cost = [[] for _ in range(n)]
    for ((a, b), w) in edges:
        adj[a - 1].append(b - 1)
        cost[a - 1].append(w)
    print(negative_cycle(adj, cost))
