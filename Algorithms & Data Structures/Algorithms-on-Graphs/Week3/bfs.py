# Uses python3
import sys
import queue

# Task. Given an undirected graph with n vertices and m edges and two vertices u and v, compute the length
# of a shortest path between u and v (that is, the minimum number of edges in a path from u to v).
# Input Format. A graph is given in the standard format. The next line contains two vertices u and v.
# Output Format. Output the minimum number of edges in a path from u to v, or −1 if there is no path.


def distance(adj, s, t):
    n = len(adj)  # number of vertices
    inf = n + 1  # distance between the origin and isolated points
    dist = [inf] * n  # an initialized array containing distance of each vertex
    dist[s] = 0  # distance to itself is 0
    q_vertex = queue.Queue()  # a FIFO queue to store nodes in breadth first search
    q_vertex.put(s)

    while not q_vertex.empty():
        u = q_vertex.get()
        for v in adj[u]:  # search the neighborhood of u
            if (
                dist[v] == inf
            ):  # if it's not visited before, enqueue it and d(v, s) = d(u, s) + 1 because each edge has the same weighting
                q_vertex.put(v)
                dist[v] = dist[u] + 1

    if dist[t] != inf:  # if dist[t] != inf, t is reachable from s
        return dist[t]  # output the number edges
    else:
        return -1  # otherwise, it is unreachable from s, output -1


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
    s, t = data[2 * m] - 1, data[2 * m + 1] - 1
    print(distance(adj, s, t))
