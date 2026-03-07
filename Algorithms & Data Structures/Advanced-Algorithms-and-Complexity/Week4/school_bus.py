# python3
from itertools import combinations, product

INF = 10**9


def read_data():
    n, m = map(int, input().split())
    graph = [[INF] * n for _ in range(n)]
    for _ in range(m):
        u, v, weight = map(int, input().split())
        u -= 1
        v -= 1
        graph[u][v] = graph[v][u] = weight
    return graph


def print_answer(path_weight, path):
    print(path_weight)
    if path_weight == -1:
        return
    print(" ".join(map(str, path)))


def map_set2num(set):
    return sum(map(lambda x: 1 << x, set + (0,)))


def tsp_solver(graph):
    n = len(graph)  # Number of vertices
    best_ans, last_vertex = INF, None  # Optimal value, terminal vertex
    best_path = []  # Optimal path

    C = [[INF] * n for _ in range(1 << n)]  # DP table
    path_table = [[(None, None)] * n for _ in range(1 << n)]  # Backtracking

    C[1][0] = 0  # C({1}, 1) = 0
    remaining_vertices = range(1, n)  # from 2,..., n

    # Consider every combination of vertices (from 2 to n) at every possible size
    for s in remaining_vertices:
        for S in combinations(remaining_vertices, s):
            k = map_set2num(S)  # set of vertices -> {i: i-th bit of k is 1} -> k

            for i, j in product(
                S, S + (0,)
            ):  # Shortest path from vertex 1 to vertex j + 1
                if i != j:
                    current_sol = (
                        C[k ^ (1 << i)][j] + graph[j][i]
                    )  # C(S - {i}, j) + d_{ji}, the path from 1 to i through j
                    if (
                        current_sol < C[k][i]
                    ):  # Check improvement by comparing previous solution C[k][i]
                        C[k][i] = current_sol
                        path_table[k][i] = (k ^ (1 << i), j)

    # Find the optimal value by connecting every possible ending vertices with the beginning vertex
    for i in range(n):
        if C[(1 << n) - 1][i] + graph[i][0] <= best_ans:
            best_ans = C[(1 << n) - 1][i] + graph[i][0]
            last_vertex = i

    # Case when no solution
    if best_ans >= INF:
        return -1, []
    else:
        # Backtrack the shortest path from the full set 1...n
        optimal_set = (1 << n) - 1
        while optimal_set != None:
            best_path.append(last_vertex + 1)  # Add 1 to get back the original index
            optimal_set, last_vertex = path_table[optimal_set][
                last_vertex
            ]  # gives us the previous vertex and solution
        return best_ans, reversed(best_path)


if __name__ == "__main__":
    print_answer(*tsp_solver(read_data()))
