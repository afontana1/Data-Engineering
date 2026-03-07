# Uses python3
import sys

# Task. Given an directed graph with positive edge weights and with n vertices and m edges as well as two
# vertices u and v, compute the weight of a shortest path between u and v (that is, the minimum total
# weight of a path from u to v).
# Input Format. A graph is given in the standard format. The next line contains two vertices u and v.
# Output Format. Output the minimum weight of a path from u to v, or −1 if there is no path.


class Heap:
    # Default implementation of heapq in python does not support change priority of element in O(log n) time
    # Here is an implementation of binary min-heap with priority changing function
    def __init__(self):
        self.arr = (
            []
        )  # data list, contains node index and its priority key, O(1) access time
        self.track = (
            dict()
        )  # dictionary, contains node number as key and node index in the heap as value, O(m) access time

    def Put(
        self, item
    ):  # read data, item: (node priority value, node number), which is a tuple object
        self.arr.append(item)
        node, index = (
            item[1],
            len(self.arr) - 1,
        )  # node stores the node number in the graph (its value won't change), index stores the node index in heap (its value will change during relaxation)
        self.track.update({node: index})  # initialization: node number = node index

    def LeftChild(i):  # return the index of left child for 0-based index
        return 2 * i + 1

    def RightChild(i):  # return the index of right child for 0-based index
        return 2 * i + 2

    def Parent(i):  # return the index of parent for 0-based index
        return abs(i - 1) // 2

    def SiftUp(self, i):  # sift the node with index i up in an iterative way
        while (i > 0) & (
            self.arr[Heap.Parent(i)][0] > self.arr[i][0]
        ):  # if the node is not root (i > 0) and it has a smaller key than its parent, need to sift up
            node_1, node_2 = (
                self.arr[Heap.Parent(i)][1],
                self.arr[i][1],
            )  # node_1 and node_2 are indices of nodes in the heap
            index_node_1, index_node_2 = self.track.get(node_1), self.track.get(
                node_2
            )  # swap the indices because node 1 and node 2 are swapped in the heap
            self.track[node_1], self.track[node_2] = index_node_2, index_node_1
            self.arr[Heap.Parent(i)], self.arr[i] = (
                self.arr[i],
                self.arr[Heap.Parent(i)],
            )  # swap the position between the node and its parent
            i = Heap.Parent(i)  # update the index

    def SiftDown(self, i):  # sift the node with index i down in a recursive way
        minIndex = i
        l = Heap.LeftChild(i)
        if l < len(
            self.arr
        ):  # if left index is valid and left child has a smaller key than node i, node i should sift down with its left child
            if self.arr[l][0] < self.arr[minIndex][0]:
                minIndex = l
        r = Heap.RightChild(i)
        if r < len(
            self.arr
        ):  # similar reasoning, sift node i down with the child with the smallest key (in case both left and right children have keys smaller than that of node i)
            if self.arr[r][0] < self.arr[minIndex][0]:
                minIndex = r
        if (
            i != minIndex
        ):  # If there is a swapping, swap the actual positions in heap as well as the indices in the heap
            node_1, node_2 = self.arr[i][1], self.arr[minIndex][1]
            index_node_1, index_node_2 = self.track.get(node_1), self.track.get(node_2)
            self.track[node_1], self.track[node_2] = index_node_2, index_node_1
            self.arr[i], self.arr[minIndex] = self.arr[minIndex], self.arr[i]
            Heap.SiftDown(self, minIndex)

    def Pop(self):  # pop out the root (which has the smallest key in the heap)
        result = None  # if data array has no element, return None
        if (
            len(self.arr) > 1
        ):  # When there is more than 1 element in data array, need to do swapping
            result = self.arr[
                0
            ]  # Otherwise, result = first element in heap (root in heap)
            self.arr[0] = self.arr[
                -1
            ]  # Replace the root with the largest elmeent in heap and reduce the size of heap by 1
            del self.arr[-1]
            node = self.arr[0][
                1
            ]  # Also update the index in heap of the largest element
            self.track[node] = 0
            self.track.pop(
                result[1]
            )  # remove the key of the smallest element from dictionary
            Heap.SiftDown(
                self, 0
            )  # sift down the root (which is now the largest element) to appropriate position in the heap

        elif (
            len(self.arr) == 1
        ):  # Trivial case if the data array has only 1 element, just pop it out
            result = self.arr[0]
            self.arr.pop()
            self.track.pop(result[1])
        return result

    def ChangePriority(
        self, item
    ):  # This function changes the priority of item (index update)
        key, node = item
        node_index = self.track[
            node
        ]  # get the node index in the heap given the node number
        old_key = self.arr[node_index][0]
        self.arr[node_index] = item  # update the data array with new key
        if (
            key >= old_key
        ):  # Determine if sift up or down by comparing old key value with new key value
            Heap.SiftDown(self, node_index)
        else:
            Heap.SiftUp(self, node_index)

    def Empty(self):  # Check if the heap is empty i.e. self.arr has length 0
        return len(self.arr) == 0


def distance(adj, cost, s, t):
    # Dijkstra's Algorithm standard implementation
    n = len(adj)  # Number of nodes in the given graph
    inf = (10**3) * n + 1  # Inreachable distance, just a large number
    node = range(n)  # a series of node numbers
    dist = [inf] * n  # all distance from s are infinity before edge relaxation

    # Initialize starting point and priority queue
    dist[s] = 0  # distance to itself is 0
    H = Heap()  # H is a binary min-heap

    # Build heap
    for node_num, priority in zip(node, dist):
        H.Put((priority, node_num))
    H.SiftUp(s)  # dist[s] = 0, should be the root of min heap

    # Edge relaxation
    while not H.Empty():
        _, u = H.Pop()  # u is the node with minimum distance to s
        if (
            len(adj[u]) > 0
        ):  # If u has neighbor nodes, do relaxation. Otherwise, it is isolated to which no edges are connected.
            for i in range(len(adj[u])):
                v = adj[u][i]
                if (
                    dist[v] > dist[u] + cost[u][i]
                ):  # Replace old d(s,v) with d(s,u) + cost(u, v)
                    dist[v] = dist[u] + cost[u][i]
                    H.ChangePriority(
                        (dist[v], v)
                    )  # d(s,v) changed -> its position in heap is also changed
    if (
        dist[t] != inf
    ):  # if the destination node is reachable, it should not be infinity after dijkstra's algorithm
        return dist[t]
    return -1  # Otherwise, return -1


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
    s, t = data[0] - 1, data[1] - 1
    print(distance(adj, cost, s, t))
