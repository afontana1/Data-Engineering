# Uses python3
import sys
import queue

# Task. Given an directed graph with possibly negative edge weights and with n vertices and m edges as well
# as its vertex s, compute the length of shortest paths from s to all other vertices of the graph.
# Input Format. A graph is given in the standard format.
# Output Format. For all vertices 𝑖 from 1 to 𝑛 output the following on a separate line:
# “*”, if there is no path from s to u;
# “-”, if there is a path from s to u, but there is no shortest path from s to u (that is, the distance from s to u is -infinity);
# the length of a shortest path otherwise.


class NegWCycle:
    # A graph object which stores adjacency list, edge weights, starting point, distance to s, reachability and a boolean vector denotes whether the node is shortest path
    def __init__(self, adj, cost, s, distance, reachable, shortest):
        self.s = s
        self.dist = (
            distance.copy()
        )  # This is the distance array in BFS for negative cycle, not for Bellman-Ford algorithm in detecting negative cycle
        self.adj = adj
        self.cost = cost
        self.q = queue.Queue()

    # A method to detect negative cycle in the graph. Using Bellman-Ford algorithm, we can only calculate the distance from s to reachable nodes
    def negative_cycle(self):
        n = len(self.adj)  # number of node in the graph
        reachable[self.s] = 1  # starting point must be reachable to itself
        distance[self.s] = 0  # starting point has 0 distance to itself
        # a standard implementation of Bellman-Ford algorithm in O(|V||E|) time
        for j in range(n):  # Loop |V| times
            for u in range(n):  # Run all edges
                if len(self.adj[u]) != 0:
                    for i in range(len(self.adj[u])):
                        v = self.adj[u][i]
                        if (
                            distance[v] > distance[u] + self.cost[u][i]
                        ):  # Edge relaxation
                            distance[v] = (
                                distance[u] + self.cost[u][i]
                            )  # update the distance in edge relaxation
                            reachable[v] = 1  # update the reachability
                            if (
                                j == n - 1
                            ):  # If there is edge relaxation in the |V|-th iteration, it imples a negative cycle
                                self.q.put(v)  # We append those nodes in the queue

    # A method to apply standard BFS algorithm to find out all elements in that negative weight cycle
    def search_cycle(self):
        inf = float("inf")
        first = True  # whether it is the first element in the queue
        while not self.q.empty():
            u = (
                self.q.get()
            )  # dequeue an element, if it is the first element in the queue, let distance to itself is set to 0, and update the boolean
            if first == True:
                self.dist[u] = 0
                first = False
            shortest[
                u
            ] = 0  # Every such node dequeued is a part of negative weight cycle; hence it does not belong to the shortest path
            for v in self.adj[u]:  # search the neighborhood of u
                if (
                    self.dist[v] == inf
                ):  # if it's not visited before, enqueue it and d(v, s) = d(u, s) + 1 because each edge has the same weighting
                    self.q.put(
                        v
                    )  # enqueue all its unvisited neighborhood; update distance
                    self.dist[v] = self.dist[u] + 1


def shortet_paths(adj, cost, s, distance, reachable, shortest):
    nwc = NegWCycle(adj, cost, s, distance, reachable, shortest)
    nwc.negative_cycle()
    nwc.search_cycle()


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
    s = data[0]
    s -= 1
    distance = [float("inf")] * n
    reachable = [0] * n
    shortest = [1] * n
    shortet_paths(adj, cost, s, distance, reachable, shortest)
    for x in range(n):
        if reachable[x] == 0:
            print("*")
        elif shortest[x] == 0:
            print("-")
        else:
            print(distance[x])
