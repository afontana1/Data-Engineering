# python3
# -*- coding: utf-8 -*-
import itertools

# This can be reduced to a classic Hamiltonian Path problem: given a graph, determine whether there is
# a route visiting each vertex exactly once.

n, m = map(int, input().split())
edges = [list(map(int, input().split())) for i in range(m)]
# Number of vertices
vertex = range(1, n + 1)


def varnum(i, j):
    # Create a separate variable 𝑥𝑖𝑗 for each vertex 𝑖 and each position
    # the Hamiltonian path 𝑗
    # Note: i can be double digits
    return 100 * i + j


def reset_clause(k):
    return [list() for i in range(k)]


def empty_clause():
    return []


def print_clause(clause):
    for c in clause:
        c.append(0)
        print(" ".join(map(str, c)))


def create_adj_list(edges, n):
    adj_list = [set() for i in range(n)]  # Use a set to avoid repeated adding
    for e in edges:
        # Traverse through all edges to build an adjacency list
        # Remark: e can contain bidirectional edges
        adj_list[e[0] - 1].add(e[1] - 1)  # Index of vertex minus 1
        adj_list[e[1] - 1].add(e[0] - 1)  # Index of vertex minus 1
    return adj_list


def depth_first_search(adj_list, start, reachable):
    reachable[start] = True
    for adj_vertex in adj_list[start]:
        if reachable[adj_vertex] == False:
            depth_first_search(adj_list, adj_vertex, reachable)


def sat_formula():
    # Total clause containing all clauses
    total_clause = empty_clause()

    # Create an adjacency list for vertices
    adj_list = create_adj_list(edges, n)

    # Special case handling: isolated vertex, empty graph, single room
    unsat = 0  # Whether the problem is satisfiable or not
    for e in adj_list:
        # Unsatisfiable if there is any isolated node
        if len(e) == 0:
            unsat = 1
            break  # Exit node traverse process

    # Check if the graph is disconnected
    reachable = [False for i in range(n)]
    depth_first_search(adj_list, 0, reachable)

    for r in reachable:
        # Unsatisfiable if the graph is disconnected
        if r == False:
            unsat = 1
            break

    if n == 1:
        unsat = 2  # Special case when single node

    # Case if the graph is connected
    if unsat == 0:
        # Each vertex belongs to a path
        clause = reset_clause(n)
        for (v, w) in itertools.product(vertex, repeat=2):
            clause[v - 1].append(varnum(v, w))
        total_clause += clause  # print_clause(clause)

        # Each vertex appears just once in a path
        clause_temp = reset_clause(n)
        clause = empty_clause()
        for (v, w) in itertools.product(vertex, repeat=2):
            clause_temp[v - 1].append(varnum(v, w))
        for c in clause_temp:
            for pair_l, pair_r in itertools.combinations(c, 2):
                clause.append([-pair_l, -pair_r])
        total_clause += clause  # print_clause(clause)

        # Each position in a path is occupied by some vertex
        clause = reset_clause(n)
        for (v, w) in itertools.product(vertex, repeat=2):
            clause[w - 1].append(varnum(v, w))
        total_clause += clause  # print_clause(clause)

        # No two vertices occupy the same position of a path
        clause_temp = reset_clause(n)
        clause = empty_clause()
        for (v, w) in itertools.product(vertex, repeat=2):
            clause_temp[w - 1].append(varnum(v, w))
        for c in clause_temp:
            for pair_l, pair_r in itertools.combinations(c, 2):
                if str(pair_r)[1] == str(pair_r)[0]:
                    continue  # otherwise, same variable will appear twice on left and right
                clause.append([-pair_l, -pair_r])
        total_clause += clause  # print_clause(clause)

        # Two successive vertices on a path must be connected by an edge.
        clause = empty_clause()
        for w in range(1, n):
            for v in vertex:
                literal = []
                first_pair = -varnum(v, w)
                literal.append(first_pair)
                for adj_node in adj_list[v - 1]:
                    # For every adjacent node in the next path
                    next_pair = varnum(adj_node + 1, w + 1)
                    literal.append(next_pair)
                clause.append(literal)
        total_clause += clause  # print_clause(clause)

    # Case if there is some isolated node
    elif unsat == 1:
        total_clause.append([1])
        total_clause.append([-1])

    # Case if single node
    else:
        total_clause.append([1])

    # Print the output to console
    print("{} {}\n".format(len(total_clause), 100000))
    print_clause(total_clause)


sat_formula()
