# python3

import sys
import threading
import queue

# Set recursion limits for the grader
sys.setrecursionlimit(10**7)
threading.stack_size(2**26)

# Reuse code from circuit_design.py
# A class for finding the topological sort of strongly connected components
class strongly_connected_components:
    def __init__(self, adj, radj):
        self.adj = adj  # Adjacency list
        self.radj = radj  # Reversed adjacency list
        self.n = len(radj)  # n = total number of literals, including the negations

        self.lifo_q = queue.LifoQueue()  # For storing literals in postvisit order

        self.count = 0  # Count the strongly connected components (SCCs)
        self.scc = list()  # For strong the sorted SCCs
        self.num2scc = [
            None
        ] * self.n  # A look-up table to check literal-SCC relationship

    def explore(self, v, visit):
        visit[v] = 1

        for w in self.radj[v]:
            if visit[w] == 0:
                self.explore(w, visit)

        # Store the literal in a LIFO queue, so that the last visited literal being popped first
        # The source vertex in the reversed graph is the sink in the original graph
        self.lifo_q.put(v)

    def dfs(self):
        visit = [0] * self.n

        # Perform a depth-first search based on reversed adjacency list
        # Record the postvisit order
        for u in range(self.n):
            if visit[u] == 0:
                self.explore(u, visit)

    def find_scc_members(self, v, visit, order):
        # Update
        visit[v] = 1
        order.append(v)
        self.num2scc[v] = self.count

        # Explore the neighborhood using DFS
        for w in self.adj[v]:
            if visit[w] == 0:
                self.find_scc_members(w, visit, order)

    def assign(self):
        visit = [0] * self.n

        # Traverse the literals in reversed post order with the original graph
        while self.lifo_q.qsize() > 0:
            u = self.lifo_q.get()

            if visit[u] == 0:
                member = list()  # Contains all members of a SCC
                self.find_scc_members(u, visit, member)
                self.scc.append(member)
                self.count += 1  # Go to the next SCC after exploration


# A class for building an implication graph
class implication_graph:
    def __init__(self, n, clauses):
        self.n = n
        self.adj = [
            set() for _ in range(2 * n)
        ]  # Adjacency list, we use set() to avoid duplicaed edges
        self.radj = [
            set() for _ in range(2 * n)
        ]  # Reversed adjacency list, we use set() to avoid duplicaed edges
        self.clauses = clauses

    # Convert indices [-n,..., -1, 1,...., n] to [0, ..., 2n - 1]
    @staticmethod
    def get_node_index(left, right, n):
        # For positive index i, return i - 1. For negative index i, return n - 1 - i
        if left > 0:
            # x[i] and x[j]
            if right > 0:
                return left - 1, right - 1
            # x[i] and -x[j]
            else:
                return left - 1, n - 1 - right
        else:
            # -x[i] and x[j]
            if right > 0:
                return n - 1 - left, right - 1
            # -x[i] and -x[j]
            else:
                return n - 1 - left, n - 1 - right

    # Add edges to the implication graphs
    def add_edges(self):
        left, right = None, None

        # Loop through each clauses
        for clause in self.clauses:
            # If the clause contains 2 literals, assign the literals respectively
            if len(clause) > 1:
                left, right = clause

            # If the clause has only 1 literal, assign left and right the same literal
            else:
                left, right = clause[0], clause[0]

            # Add the edge: ~l[1] -> l[2]
            _from, _to = self.get_node_index(-left, right, self.n)
            self.adj[_from].add(_to)
            self.radj[_to].add(_from)

            # If the clause contains 2 literals, we also need to do the opposite
            if left != right:
                # Add another edge: ~l[2] -> l[1]
                _from, _to = self.get_node_index(-right, left, self.n)
                self.adj[_from].add(_to)
                self.radj[_to].add(_from)


def check_satisfiability(n, clauses):
    # Build the implication graph based on clauses
    # https://en.wikipedia.org/wiki/Implication_graph
    imgraph = implication_graph(n, clauses)
    imgraph.add_edges()

    # Find strongly connected components using depth first search and perform topological sort
    scc = strongly_connected_components(imgraph.adj, imgraph.radj)
    scc.dfs()
    scc.assign()

    # Check for unsatisfied conditions for literals from x[0] to x[n - 1]
    for i in range(n):
        # Get literal x[i] and ~x[i]
        left, right = imgraph.get_node_index(i + 1, -(i + 1), n)

        # If x[i] and ~x[i] are lying in the same SCC: return None because the clauses are unsatisfiable
        if scc.num2scc[left] == scc.num2scc[right]:
            return None

    # Otherwise, the clauses are satisfiable
    # Create a container for the boolean assignment
    assign_literal = [None for _ in range(2 * n)]

    for group in scc.scc:
        for u in group:
            if assign_literal[u] == None:
                assign_literal[u] = True
                if u >= n:
                    assign_literal[u - n] = False
                else:
                    assign_literal[u + n] = False

    return assign_literal


# Convert vertex and color to an literal
def get_literal(i, color_code):
    if color_code == "R":
        return 3 * (i + 1) - 2
    elif color_code == "G":
        return 3 * (i + 1) - 1
    elif color_code == "B":
        return 3 * (i + 1)


def assign_new_colors(n, edges, colors):
    clauses = list()
    color_set = set(["R", "G", "B"])  # A set of all colors

    for i in range(n):
        color1, color2 = color_set - set(
            colors[i]
        )  # Set difference, consider the remaining colors
        clauses.append(
            (get_literal(i, color1), get_literal(i, color2))
        )  # x[i][c1] v x[i][c2]
        clauses.append(
            (-get_literal(i, color1), -get_literal(i, color2))
        )  # ~x[i][c1] v ~x[i][c2] -> Either c1 or c2 but not both

    for left, right in edges:
        for color in color_set:
            clauses.append(
                (-get_literal(left - 1, color), -get_literal(right - 1, color))
            )  # If x and y are two vertices connected by an edge, they cannot have the same colors for R, B and G

    return check_satisfiability(
        3 * n, clauses
    )  # Reuse the code from the first assignment


# Get color code given literal
def get_color(i):
    if (i + 1) % 3 == 1:
        return "R"
    elif (i + 1) % 3 == 2:
        return "G"
    elif (i + 1) % 3 == 0:
        return "B"


def main():
    n, m = map(int, input().split())
    colors = input()
    colors = [
        char for char in colors
    ]  # Original code: colors = input().split() has a bug, use list comphrension intead
    edges = []

    for i in range(m):
        u, v = map(int, input().split())
        edges.append((u, v))

    new_colors = assign_new_colors(n, edges, colors)

    if new_colors is None:
        print("Impossible")
    else:
        print("".join(get_color(i) if new_colors[i] else "" for i in range(3 * n)))


threading.Thread(target=main).start()
