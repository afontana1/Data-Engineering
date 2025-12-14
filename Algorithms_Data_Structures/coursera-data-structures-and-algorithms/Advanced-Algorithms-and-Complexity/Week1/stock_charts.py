# python3
from queue import Queue

# Task. You’re in the middle of writing your newspaper’s end-of-year economics summary, and you’ve decided
# that you want to show a number of charts to demonstrate how different stocks have performed over the
# course of the last year. You’ve already decided that you want to show the price of n different stocks,
# all at the same k points of the year.
# A simple chart of one stock’s price would draw lines between the points (0, price[0]), (1, price[1]), . . . , (k−
# 1, price[k - 1]), where price[i] is the price of the stock at the i-th point in time.
# Input Format. The first line of the input contains two integers n and k — the number of stocks and the
# number of points in the year which are common for all of them. Each of the next n lines contains k
# integers. The i-th of those n lines contains the prices of the i-th stock at the corresponding k points
# in the year.
# Output Format. Output a single integer — the minimum number of overlaid charts to visualize all the
# stock price data you have.


class DirectedGraph:  # a directed graph object, use adjacency matrix to store the relation
    def __init__(self, stock_data):
        self.data = stock_data
        self.n = len(
            stock_data
        )  # n <= 100 in this problem, using adjacency matrix costs little memory!
        self.adj_list = [[0] * self.n for _ in range(self.n)]

    def compare(
        self, i, j
    ):  # a function to compare two stocks, i and j. If all elements of stock i are strictly smaller than those of stock j, return True
        stock_1, stock_2 = self.data[i], self.data[j]
        for (p_1, p_2) in zip(stock_1, stock_2):
            if p_1 >= p_2:
                return False
        return True

    def build_graph(self):  # a function to fill the adjacency matrix
        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    if self.compare(i, j):
                        self.adj_list[i][j] = 1


class Edge:  # an edge object, see airline.py
    def __init__(self, u, v, capacity):
        self.u = u
        self.v = v
        self.capacity = capacity
        self.flow = 0


class FlowGraph:  # a network object, see airline.py
    def __init__(self, n):
        self.edges = []
        self.graph = [[] for _ in range(n)]

    def add_edge(self, from_, to, capacity):
        forward_edge = Edge(from_, to, capacity)
        backward_edge = Edge(to, from_, 0)
        self.graph[from_].append(len(self.edges))
        self.edges.append(forward_edge)
        self.graph[to].append(len(self.edges))
        self.edges.append(backward_edge)

    def size(self):
        return len(self.graph)

    def get_ids(self, from_):
        return self.graph[from_]

    def get_edge(self, id):
        return self.edges[id]

    def add_flow(self, id, flow):
        self.edges[id].flow += flow
        self.edges[id ^ 1].flow -= flow


def update_residual_graph(graph, X, edges, prev, from_, to):
    while to != from_:
        graph.add_flow(edges[to], X)
        to = prev[to]
    return graph


def reconstruct_path(graph, from_, to, prev, edges):  # see airline.py
    result = []
    X = 10000 + 1
    while to != from_:
        result.append(to)
        X = min(X, graph.get_edge(edges[to]).capacity - graph.get_edge(edges[to]).flow)
        to = prev[to]
    return [from_] + [u for u in reversed(result)], X, edges, prev


def find_a_path(graph, from_, to):  # see airline.py
    dist = [False] * graph.size()
    dist[from_] = True
    prev = [None] * graph.size()
    edges = [None] * graph.size()
    q = Queue()
    q.put(from_)

    while not q.empty():
        u = q.get()
        for id in graph.get_ids(u):
            to_edge_v = graph.get_edge(id)
            v = to_edge_v.v
            flow = to_edge_v.flow
            capacity = to_edge_v.capacity

            if (dist[v] == False) and (flow < capacity):
                q.put(v)
                dist[v] = True
                prev[v] = u
                edges[v] = id

    if dist[to] == True:
        return reconstruct_path(graph, from_, to, prev, edges)
    else:
        return [], 0, [], []


def max_flow(
    graph, from_, to
):  # Standard implementation of Edmonds-Karp algorithm, see airline.py
    flow = 0
    while True:
        path, X, edges, prev = find_a_path(graph, from_, to)
        if len(path) == 0:
            return flow
        flow += X
        graph = update_residual_graph(graph, X, edges, prev, from_, to)
    return flow


class StockCharts:
    def read_data(self):  # read input
        n, k = map(int, input().split())
        stock_data = [list(map(int, input().split())) for i in range(n)]
        return stock_data

    def write_response(self, result):  # write output
        print(result)

    def min_charts(self, stock_data):
        # Idea: If stock[i] > stock[j] for all elements, then these two stocks can be put together in the same chart
        # Let there be a bipartite graph of two set of vertices of size n.
        # We can draw a line to connect a pair of vertices only if stock[i] in left hand side > stock[j] in right hand side
        # Simple cases:
        # If stock[i] > stock[j] and stock[j] > stock[k] (which automatically implies stock[i] > stock[k] , then there are three matches and all of them can be put into a single chart
        # If stock[i] > stock[j] and stock[k] > stock[j] but stock[k] !> stock[i], then there are two matches in the bipartite graph
        # So, n - number of matches = number of chart needed
        n = len(stock_data)  # n = number of stocks in total
        dag = DirectedGraph(stock_data)  # Initialize the directed graph
        dag.build_graph()  # Build adjacency matrix
        network = FlowGraph(2 * (n + 1))  # Initialize the network
        source, sink, capacity = (
            0,
            2 * n + 1,
            1,
        )  # Let source has index 0, sink has index 2*n + 1, capacity is 1 for each edge

        for i in range(1, n + 1):
            network.add_edge(source, i, 1)  # add edges from source to stock[i]
            for j in range(n + 1, 2 * n + 1):
                if (
                    dag.adj_list[i - 1][j - (n + 1)] == 1
                ):  # if stock[i] > stock[j] at all time point, add edges from stock[i] to stock[j]
                    network.add_edge(i, j, 1)
        for j in range(n + 1, 2 * (n + 1)):  # add edges from stock[j] to sink
            network.add_edge(j, sink, 1)
        return n - max_flow(
            network, source, sink
        )  # the maxflow is the maximum number of stocks

    def solve(self):
        stock_data = self.read_data()
        result = self.min_charts(stock_data)
        self.write_response(result)


if __name__ == "__main__":
    stock_charts = StockCharts()
    stock_charts.solve()
