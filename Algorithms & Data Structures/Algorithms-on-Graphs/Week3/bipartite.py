# Uses python3
import sys
import queue

# Task. Given an undirected graph with n vertices and m edges, check whether it is bipartite.
# Input Format. A graph is given in the standard format.
# Output Format. Output 1 if the graph is bipartite and 0 otherwise.


def bipartite(adj, n, m):
    is_bipartite = 1  # boolean variable: 1 if graph G is bipartite, otherwise 0.
    if m == 0:  # Trivial case: if G has no node, it must be bipartite
        return is_bipartite

    inf = n + 1  # distance between the origin and isolated points
    s = 0  # Start at node with key 1
    dist = [inf] * n  # distance matrix
    dist[s] = 0  # distance to itself must be 0
    q_vertex = queue.Queue()  # a FIFO queue to store nodes in breadth first search
    q_vertex.put(s)

    while (
        not q_vertex.empty()
    ):  # We color nodes in black and white (represented by numbers 1 and 0) in BFS
        u = q_vertex.get()
        for v in adj[u]:
            if (
                dist[v] == inf
            ):  # if v hasn't been visited, enqueue it and update its color with an opposite color
                q_vertex.put(v)
                dist[v] = 1 - dist[u]
            else:  # Otherwise, v has been visited and assigned a color. If the color of two adjacent nodes are the same, then G cannot be bipartite. Stop and return the results
                if dist[v] == dist[u]:
                    is_bipartite = 0
                    break
    return is_bipartite


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
    print(bipartite(adj, n, m))
