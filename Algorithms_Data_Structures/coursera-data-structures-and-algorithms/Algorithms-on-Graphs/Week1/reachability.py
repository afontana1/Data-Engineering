# Uses python3
import sys

# Task. Given an undirected graph and two distinct vertices u and v, check if there is a path between u and v.
# Input Format. An undirected graph with n vertices and m edges. The next line contains two vertices u
# and v of the graph.
# Output Format. Output 1 if there is a path between u and v and 0 otherwise.


def explore(v, adj, visit):  # Do a depth first search from vertex v
    visit[v] = 1  # If we explore the neighborhood of v, we must have visited v
    for w in adj[v]:  # Explore the unvisited neighborhoods of vertex v
        if visit[w] == 0:
            explore(w, adj, visit)


def reach(adj, x, y):
    visit = len(adj) * [0]  # At the beginning, all vertices are not visited
    explore(
        x, adj, visit
    )  # Now, we start at vertex x, and explore the adjacent vertices of x
    if (
        visit[y] > 0
    ):  # if the target node, y, is visited in depth first search started at x, it is reachable by definition and we return 1
        return 1
    return 0  # Otherwise, it's not reachable and return 0


if __name__ == "__main__":
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0 : (2 * m) : 2], data[1 : (2 * m) : 2]))
    x, y = data[2 * m :]
    adj = [[] for _ in range(n)]
    x, y = x - 1, y - 1
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
        adj[b - 1].append(a - 1)
    print(reach(adj, x, y))
