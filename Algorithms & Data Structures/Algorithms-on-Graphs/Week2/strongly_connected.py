# Uses python3
import sys

sys.setrecursionlimit(200000)
# Task. Task. Compute the number of strongly connected components of a given directed graph with n vertices and m edges.
# Input Format. A graph is given in the standard format.
# Output Format. Output the number of strongly connected components.


def previsit(v, pre, clock):  # update previsit order
    pre[v] = clock
    clock += 1
    return clock


def postvisit(v, post, clock):  # update postvisit order
    post[v] = clock
    clock += 1
    return clock


def explore(
    v, visit, radj, pre, post, clock, stack
):  # The explore algorithm associated with depth first search of the reversed graph
    visit[v] = 1  # update the visit status of node v
    clock = previsit(v, pre, clock)  # calculate the previsit order of node v
    for w in radj[v]:  # explore neighborhoods of v
        if visit[w] == 0:
            clock = explore(w, visit, radj, pre, post, clock, stack)
    stack.append(v)  # append v in ascending order of postvisit in the reversed graph
    clock = postvisit(v, post, clock)  # calculate the postvisit order of node v
    return clock


def simple_explore(
    v, visit, adj
):  # The explore algorithm associated with depth first search of strongly connected components
    visit[v] = 1
    for w in adj[v]:
        if visit[w] == 0:
            simple_explore(w, visit, adj)


def dfs(radj):  # A depth first search for reversed graph
    n = len(radj)
    visit = [
        0
    ] * n  # visit: if each vertex in the reversed graph is visited (1 if yes, 0 if no)
    clock = 0  # Initialize the clock
    pre, post = [0] * n, [0] * n  # preorder and postorder visits for vertices
    stack = (
        []
    )  # a LIFO queue to store the nodes in ascending postvisit order in the reversed graph
    for v in range(n):  # Do a depth first search to explore unvisited vertices
        if visit[v] == 0:
            clock = explore(v, visit, radj, pre, post, clock, stack)
    return stack


def number_of_strongly_connected_components(adj, radj):
    result = 0
    stack = dfs(radj)
    n = len(stack)  # number of nodes in graphs, same as len(adj)
    visit = [0] * n
    for i in range(n):
        v = (
            stack.pop()
        )  # start with the largest postorder node in the reversed graph (rmb: LIFO queue)
        if visit[v] == 0:
            simple_explore(
                v, visit, adj
            )  # explore all nodes reachable from the largest postorder node. These nodes form a strongly connected component
            result += 1
    return result


if __name__ == "__main__":
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0 : (2 * m) : 2], data[1 : (2 * m) : 2]))
    adj = [[] for _ in range(n)]
    radj = [[] for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
        radj[b - 1].append(a - 1)
    print(number_of_strongly_connected_components(adj, radj))
