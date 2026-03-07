# Uses python3
import sys
import math

# Task. Given n points on a plane, connect them with segments of minimum total length such that there is a
# path between any two points. Recall that the length of a segment with endpoints (x1, y1) and (x2, y2)
# is equal to sqrt((x1 - x2)^2 + (y1 - y2)^2)
# Input Format. The first line contains the number n of points. Each of the following n lines defines a point (x[i], y[i]).
# Output Format. Output the minimum total length of segments. The absolute value of the difference
# between the answer of your program and the optimal value should be at most 10^−6. To ensure this,
# output your answer with at least seven digits after the decimal point (otherwise your answer, while
# being computed correctly, can turn out to be wrong because of rounding issues).


class Heap:  # Standard implementation of binary heap: see dijkstra.py
    def __init__(self):
        self.arr = []
        self.track = dict()

    def Put(self, item):
        self.arr.append(item)
        node, index = item[1], len(self.arr) - 1
        self.track.update({node: index})

    def LeftChild(i):
        return 2 * i + 1

    def RightChild(i):
        return 2 * i + 2

    def Parent(i):
        return abs(i - 1) // 2

    def SiftUp(self, i):
        while (i > 0) & (self.arr[Heap.Parent(i)][0] > self.arr[i][0]):
            node_1, node_2 = self.arr[Heap.Parent(i)][1], self.arr[i][1]
            index_node_1, index_node_2 = self.track.get(node_1), self.track.get(node_2)
            self.track[node_1], self.track[node_2] = index_node_2, index_node_1
            self.arr[Heap.Parent(i)], self.arr[i] = (
                self.arr[i],
                self.arr[Heap.Parent(i)],
            )
            i = Heap.Parent(i)

    def SiftDown(self, i):
        minIndex = i
        l = Heap.LeftChild(i)
        if l < len(self.arr):
            if self.arr[l][0] < self.arr[minIndex][0]:
                minIndex = l
        r = Heap.RightChild(i)
        if r < len(self.arr):
            if self.arr[r][0] < self.arr[minIndex][0]:
                minIndex = r
        if i != minIndex:
            node_1, node_2 = self.arr[i][1], self.arr[minIndex][1]
            index_node_1, index_node_2 = self.track.get(node_1), self.track.get(node_2)
            self.track[node_1], self.track[node_2] = index_node_2, index_node_1
            self.arr[i], self.arr[minIndex] = self.arr[minIndex], self.arr[i]
            Heap.SiftDown(self, minIndex)

    def Pop(self):
        result = None
        if len(self.arr) > 1:
            result = self.arr[0]
            self.arr[0] = self.arr[-1]
            del self.arr[-1]
            node = self.arr[0][1]
            self.track[node] = 0
            self.track.pop(result[1])
            Heap.SiftDown(self, 0)

        elif len(self.arr) == 1:
            result = self.arr[0]
            self.arr.pop()
            self.track.pop(result[1])
        return result

    def ChangePriority(self, item):
        key, node = item
        node_index = self.track[node]
        old_key = self.arr[node_index][0]
        self.arr[node_index] = item
        if key >= old_key:
            Heap.SiftDown(self, node_index)
        else:
            Heap.SiftUp(self, node_index)

    def Empty(self):
        return len(self.arr) == 0


def compute_distance(x_0, y_0, x_1, y_1):
    return math.sqrt((x_0 - x_1) ** 2 + (y_0 - y_1) ** 2)


def minimum_distance(x, y):  # standard implementation of Prim's algorithm
    result = 0  # intialize the length of MST be 0
    n = len(x)  # number of nodes given
    adj = [[0] * n for i in range(n)]  # List of distance

    for i in range(
        n
    ):  # O(n^2) algorithm to compute distance between points (i.e. edges)
        for j in range(n):
            if i == j:
                adj[i][j] = 0.0
            elif i > j:
                dist = compute_distance(x[i], y[i], x[j], y[j])
                adj[i][j] = dist
                adj[j][i] = dist

    inf = float("inf")  # a big number
    cost = [inf] * n  # Initialize to cost of adding new vertices as infinity
    cost[0] = 0  # cost to add a starting point is 0

    H = Heap()
    for i in range(n):
        H.Put((cost[i], i))

    while not H.Empty():
        (
            weight,
            u,
        ) = (
            H.Pop()
        )  # H pops out the vertex with the smallest cost to add to MST. The first iteration is the first node as cost[0] = 0
        result += weight  # add this vertex to MST
        for z in range(len(adj[u])):
            if (z in H.track) and (
                cost[z] > adj[u][z]
            ):  # search its neighborhood and update its cost using information from edges
                cost[z] = adj[u][z]
                H.ChangePriority(
                    (cost[z], z)
                )  # update priority and the next iteration will pop out the second lowest cost to add node to vertex u
    return result


if __name__ == "__main__":
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n = data[0]
    x = data[1::2]
    y = data[2::2]
    print("{0:.9f}".format(minimum_distance(x, y)))
