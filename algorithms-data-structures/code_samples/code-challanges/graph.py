class Graph:
    def __init__(self, directed=False):
        self._outgoing = {}

        # If the graph is undirected, 'self._outgoing'
        # is the universal storage.
        self._incoming = {} if directed else self._outgoing

    # If the graph is directed, the 'self._incoming'
    # dictionary differs from the 'self._outgoing'.
    def is_directed(self):
        return self._incoming is not self._outgoing

    # The function returns a generator of incoming
    # or outgoing (default) edges of a vertex.
    def adjacent_edges(self, vertex, outgoing=True):
        # References the corresponding outer dictionary
        # (dictionary of dictionaries)
        adj_edges = self._outgoing if outgoing else self._incoming

        # Access each of the edges for this endpoint vertex.
        for edge in adj_edges[vertex].values():
            yield edge

    def add_vertex(self, entity=None):
        # Constructs a new vertex from the entity.
        vertex = self.Vertex(entity)

        # The vertex becomes a key in the outer dictionary,
        # but the value is an internal dictionary (as we model
        # both dimensions for each edge: origin and destination).
        # e.g. {vertex_1a:{vertex_b:edge_a_b}, vertex_b:{vertex_c:edge_b_c}}.
        self._outgoing[vertex] = {}
        if self.is_directed():
            self._incoming[vertex] = {}

    def add_edge(self, origin, destination):
        # Constructs a new edge from the vertices.
        edge = self.Edge(origin, destination)

        # Adds the edge to the dictionary (dictionaries are
        # the same if the graph is undirected). The outer key
        # represents the origin, i.e. the component 'a' of
        # the edge-defining pair (a, b). The inner key stands
        # for the component 'b' of the edge-defining pair (a, b).
        self._outgoing[origin][destination] = edge

        # Even if the graph is undirected, each edge has to
        # be added twice, i.e. once for each of its endpoints.
        self._incoming[destination][origin] = edge

    def vertices(self):
        return self._outgoing.keys()

    def edges(self):
        # All the edges are collected into a set.
        result = set()
        for inner_dict in self._outgoing.values():
            result.update(inner_dict.values())
        return result

    class Vertex:
        __slots__ = "_entity"

        def __init__(self, entity):
            self._entity = entity

        # The real-world entity is represented by the Vertex object.
        def entity(self):
            return self._entity

        # We have to implement __hash__ to use
        # the object as a dictionary key.
        def __hash__(self):
            return hash(id(self))

    class Edge:
        __slots__ = "_origin", "_destination"

        def __init__(self, origin, destination):
            self._origin = origin
            self._destination = destination

        def endpoints(self):
            return (self._origin, self._destination)

        # Returns the other component of the edge-defining pair (a, b)
        # for a given component a or b, respectively.
        def opposite(self, vertex):
            return self._destination if self._origin is vertex else self._origin

        def __hash__(self):
            return hash((self._origin, self._destination))


def BFS(graph, start, visited, target=None):
    # First-level searh includes only the 'start' vertex.
    level = [start]
    # The starting vertex is visited first and has no leading edges.
    # If we did not put it into 'visited' in the first iteration,
    # it would end up here during the second iteration, pointed to
    # by one of its children vertices as a previously unvisited vertex.
    visited[start] = None

    # Trivial check #1: searches for None are immediately terminated.
    if target is None:
        return target
    # Trivial check #2: if the entity is in the starting vertex.
    elif target == start.entity():
        return start

    # Propagates the search until all the vertices are visited.
    while len(level) > 0:
        # Candidates to be searched next (children of the vertex).
        next_level = []
        for v in level:
            # Explores every edge leaving the vertex 'v'.
            print(f"Searching from vertex: {v.entity()}...")
            for edge in graph.adjacent_edges(v):
                # Gets the second endpoint.
                v_2nd_endpoint = edge.opposite(v)

                # Examines the second endpoint.
                if v_2nd_endpoint not in visited:
                    # Adds the second endpoint to 'visited'
                    # and maps the leading edge for the
                    # search path reconstruction.
                    visited[v_2nd_endpoint] = edge

                    # If the entity is found, terminates the search.
                    if v_2nd_endpoint.entity() == target:
                        return v_2nd_endpoint

                    # Otherwise, queues the second
                    # endpoint for the search.
                    next_level.append(v_2nd_endpoint)
                    print(
                        "  Vertex added for the next-level search: "
                        f"{v_2nd_endpoint.entity()}"
                    )
        # Refocuses on the next search candidates.
        level = next_level
    # If the search fails...
    return None


if __name__ == "__main__":
    ##########################################################################
    # Initializes an empty graph (object).
    g = Graph()

    # Loads the graph with the first ten vertices.
    for i in range(10):
        g.add_vertex(i)

    # Constructs the 'vertices' dictionary for a more
    # convenient access during the graph construction.
    vertices = {k.entity(): k for k in g.vertices()}

    # Constructs an arbitrary graph from
    # the existing vertices and edgs.
    g.add_edge(vertices[0], vertices[1])
    g.add_edge(vertices[0], vertices[2])
    g.add_edge(vertices[0], vertices[4])
    g.add_edge(vertices[4], vertices[3])
    g.add_edge(vertices[3], vertices[5])
    g.add_edge(vertices[0], vertices[5])
    g.add_edge(vertices[2], vertices[6])

    # Initializes the visited dictionary
    # and the search path.
    visited = {}
    path = []

    # Starts the search.
    result = BFS(g, vertices[5], visited, 6)

    # If the entity is found...
    if result is not None:
        # The search path ends with the found vertex
        # (entity). Each vertex is a container for
        # its real-world entity.
        path_vertex = result

        # The entity is added to the 'path'.
        path.append(path_vertex.entity())

        # Constructs the rest of the search path
        # (if it exists)...
        while True:
            # Gets a discovery edge
            # leading to the vertex.
            path_edge = visited.get(path_vertex)

            # If the path vertex is the root,
            # it has no discovery edge...
            if path_edge is None:
                break

            # Otherwise, gets the second
            # (parent vertex) endpoint.
            path_vertex = path_edge.opposite(path_vertex)

            # The entity is added to the 'path'.
            path.append(path_vertex.entity())
        print("Search path found:", end=" ")
        # The path is reversed and starts
        # with the root vertex.
        print(*reversed(path), sep=" -> ")

    # Otherwise...
    else:
        print("\nEntity is not found")
