# python3
# coding: utf-8
from queue import Queue

# Input Format. The first line of the input contains integers n and m — the number of cities and the number
# of roads respectively. Each of the next m lines contains three integers u, v and c describing a particular
# road — start of the road, end of the road and the number of people that can be transported through
# this road in one hour. u and v are the 1-based indices of the corresponding cities.
# The city from which people are evacuating is the city number 1, and the capital city is the city number n.
# Output Format. Output a single integer — the maximum number of people that can be evacuated from
# the city number 1 each hour.


class Edge:  # an edge object
    def __init__(self, u, v, capacity):
        self.u = u  # edge from u
        self.v = v  # edge to v
        self.capacity = capacity  # capacity of edge
        self.flow = 0  # current flow of edge


class FlowGraph:  # a network object
    def __init__(self, n):
        self.edges = []  # list of all edges (in both directions) in the graph
        self.graph = [
            [] for _ in range(n)
        ]  #  an adjacency list. index of the list is vertex. self.graph[index] contains the indices of edges in self.edge

    def add_edge(self, from_, to, capacity):
        # a method to add edge to graph
        forward_edge = Edge(from_, to, capacity)  # edge for the network
        backward_edge = Edge(to, from_, 0)  # edge for the residual network
        self.graph[from_].append(len(self.edges))  # even index for forward edges
        self.edges.append(forward_edge)  # add edge to graph
        self.graph[to].append(len(self.edges))  # odd index for backward edges
        self.edges.append(backward_edge)  # add edge to graph

    def size(self):
        # a method to calculate the size of graph in terms of vertices
        return len(self.graph)

    def get_ids(self, from_):
        # a method that returns indices in self.edges given with index vertex from_
        return self.graph[from_]

    def get_edge(self, id):
        # a method that returns the edge given the index in self.edges
        return self.edges[id]

    def add_flow(self, id, flow):
        # a method to add flow given indices in self.edges, and subtract the flow in the reversed edge
        self.edges[id].flow += flow
        self.edges[
            id ^ 1
        ].flow -= flow  # In python, id ^ 1 filps the last bit of binary representation of integer "id", e.g. 0001 ^ 1 = 0000 --> 0, 0100 ^ 1 = 0101 ---> 5


def read_data():  # read input data
    vertex_count, edge_count = map(int, input().split())
    graph = FlowGraph(vertex_count)
    for _ in range(edge_count):
        u, v, capacity = map(int, input().split())
        graph.add_edge(
            u - 1, v - 1, capacity
        )  # u, v are converted to 0-based index in python
    return graph


def update_residual_graph(
    graph, X, edges, prev, from_, to
):  # update the residual graph after adding flow
    while to != from_:
        graph.add_flow(edges[to], X)  # add the flow X to edges in residual graph
        to = prev[to]
    return graph


def reconstruct_path(
    graph, from_, to, prev, edges
):  # Standard implementation of the shortest path tree
    result = []
    X = 10000 + 1  # It is guaranteed that the capacity is at most 10000
    while to != from_:
        result.append(to)
        X = min(
            X, graph.get_edge(edges[to]).capacity - graph.get_edge(edges[to]).flow
        )  # find the minimum capacity in the s-t path
        to = prev[to]  # update index
    return [from_] + [u for u in reversed(result)], X, edges, prev


def find_a_path(
    graph, from_, to
):  # Standard algorithm to find source-sink (s-t) path using breadth first search
    dist = [
        False
    ] * graph.size()  # reachability of each node from the node with index "from_"
    dist[from_] = True  # of course the starting point is reachable to itself
    prev = [None] * graph.size()  # record the parent of each node
    edges = [
        None
    ] * graph.size()  # record the index of edge in self.edges to reach from u to v
    q = Queue()
    q.put(from_)

    while not q.empty():
        u = q.get()
        for id in graph.get_ids(u):
            to_edge_v = graph.get_edge(id)  # get edges from u to v
            v = to_edge_v.v
            flow = to_edge_v.flow
            capacity = to_edge_v.capacity

            if (dist[v] == False) and (
                flow < capacity
            ):  # consider unvisited node with flow < capacity as reachable node in BFS
                q.put(v)
                dist[v] = True
                prev[v] = u
                edges[v] = id

    if (
        dist[to] == True
    ):  # if sink is reachable, we reconstruct the path using shortest path tree
        return reconstruct_path(graph, from_, to, prev, edges)
    else:
        return [], 0, [], []


def max_flow(graph, from_, to):  # Standard implementation of Edmonds-Karp algorithm
    flow = 0  # initialize the flow with 0 at the beiginning
    while True:
        path, X, edges, prev = find_a_path(graph, from_, to)  # find a s-t path
        if len(path) == 0:  # If there is no path: return flow
            return flow
        flow += X  # otherwise, add the minimum capacity X in the s-t path to flow and update the residual graph
        graph = update_residual_graph(graph, X, edges, prev, from_, to)
    return flow


if __name__ == "__main__":
    graph = read_data()
    print(
        max_flow(graph, 0, graph.size() - 1)
    )  # evacuate from city with number 1 to city with number n
