# Uses python3
import sys

# Task. Compute a topological ordering of a given directed acyclic graph (DAG) with 𝑛 vertices and 𝑚 edges.
# Input Format. A graph is given in the standard format.
# Output Format. Output any topological ordering of its vertices. (Many DAGs have more than just one
# topological ordering. You may output any of them.)


def previsit(v, pre, clock):  # update previsit order of node v
    pre[v] = clock
    clock += 1
    return clock


def postvisit(v, post, clock):  # update postvisit order of node v
    post[v] = clock
    clock += 1
    return clock


def explore(v, visit, adj, pre, post, clock, stack):
    visit[v] = 1  # node v is visited
    clock = previsit(v, pre, clock)
    for w in adj[v]:  # neighborhood of node v will be visited in depth first search
        if visit[w] == 0:
            clock = explore(w, visit, adj, pre, post, clock, stack)
    stack.append(
        v
    )  # every visited node is appended to a LIFO queue in ascending order of postvisit (largest postvisit order at the end of queue)
    clock = postvisit(v, post, clock)
    return clock


def dfs(adj):
    n, clock = len(adj), 0
    pre, post, visit, stack = [0] * n, [0] * n, [0] * n, []
    for v in range(n):  # depth first search for unvisited nodes
        if visit[v] == 0:
            clock = explore(v, visit, adj, pre, post, clock, stack)
    return stack


def toposort(adj):
    stack = dfs(adj)
    sorted_list = []  # store nodes in an ascending order of postvisit
    n = len(stack)
    for i in range(
        n
    ):  # same as reversed(stack) because topological sort put node in descending order of postvisit
        sorted_list.append(stack.pop())
    return sorted_list


if __name__ == "__main__":
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0 : (2 * m) : 2], data[1 : (2 * m) : 2]))
    adj = [[] for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
    order = toposort(adj)
    for x in order:
        print(x + 1, end=" ")
