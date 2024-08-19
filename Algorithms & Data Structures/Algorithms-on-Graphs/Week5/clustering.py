# Uses python3
import sys
import math

# Task. Given n points on a plane and an integer k, compute the largest possible value of d such that the
# given points can be partitioned into k non-empty subsets in such a way that the distance between any
# two points from different subsets is at least d.
# Input Format. The first line contains the number n of points. Each of the following n lines defines a point
# (x[i], y[i]). The last line contains the number k of clusters.
# Output Format. Output the largest value of d. The absolute value of the difference between the answer of
# your program and the optimal value should be at most 10^−6. To ensure this, output your answer with
# at least seven digits after the decimal point (otherwise your answer, while being computed correctly,
# can turn out to be wrong because of rounding issues).


class disjoint_set:  # a disjoint set object. standard implementation of disjoint set: see merging_table.py
    def __init__(self, n):
        self.n = n
        self.parent = [0] * n
        self.rank = [0] * n

    def make_set(self, i):
        self.parent[i] = i
        self.rank[i] = 0

    def initialize(self):
        for i in range(self.n):
            self.make_set(i)

    def find(self, i):
        while i != self.parent[i]:
            i = self.parent[i]
        return i

    def union(self, i, j):
        i_id, j_id = self.find(i), self.find(j)
        if i_id == j_id:
            return
        if self.rank[i_id] > self.rank[j_id]:
            self.parent[j_id] = i_id
        else:
            self.parent[i_id] = self.parent[j_id]
            if self.rank[i_id] == self.rank[j_id]:
                self.rank[j_id] += 1


class edge:  # an edge object, which information about the indices of two ending vertices
    def __init__(self, i, j):
        self.fr = i
        self.to = j


def compute_distance(x, y):  # standard implementation of euclidean distance
    dist_sq = (x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2
    return math.sqrt(dist_sq)


def clustering(n, x, y, k):
    cluster = disjoint_set(n)
    mst = list()
    points = [(i, j) for (i, j) in zip(x, y)]
    edges = list()
    # initialize() treats every vertex given as a single disjoint set
    cluster.initialize()
    # an O(n^2) complexity to create edge: edges store edge as the following: (edge object, distance between two points)
    for i, p_1 in enumerate(points):
        for j, p_2 in enumerate(points):
            if i < j:
                edges.append((edge(i, j), compute_distance(p_1, p_2)))
    edges = sorted(edges, key=lambda e: e[1])  # sort edges by distance
    for (
        e
    ) in (
        edges
    ):  # standard implementation of Kruskal's algorithm to create a minimal spanning tree
        u, v = e[0].fr, e[0].to
        if cluster.find(u) != cluster.find(v):
            cluster.union(u, v)
            mst.append(e)

    return mst[n - k][
        1
    ]  # given k clusters, the minimal distance between any two points in two clusters must be the k-th longest edge in the MST


if __name__ == "__main__":
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n = data[0]
    data = data[1:]
    x = data[0 : 2 * n : 2]
    y = data[1 : 2 * n : 2]
    data = data[2 * n :]
    k = data[0]
    print("{0:.9f}".format(clustering(n, x, y, k)))
