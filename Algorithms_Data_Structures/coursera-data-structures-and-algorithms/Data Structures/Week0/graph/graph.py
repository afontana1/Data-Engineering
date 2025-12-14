from .edge import Edge
from .vertex import Vertex


class Graph:
    def __init__(self, directed=True):
        self.__vertices = {}
        self.__edges = set()
        self.__directed = directed

    def __str__(self):
        graph_str = ""

        for key in self.__vertices:
            graph_str += str(self.__vertices[key]) + "\n"

        return graph_str

    def add_vertex(self, label):
        if label not in self.__vertices:
            self.__vertices[label] = Vertex(label, self.__directed)

    def add_edge(self, start_label, end_label, weight=1):
        start_vertex = self.get_vertex(start_label)
        end_vertex = self.get_vertex(end_label)

        if (start_vertex or end_vertex) is None:
            raise ValueError("Can not find start or end vertex in graph")

        edge = Edge(start_vertex, end_vertex, weight, self.__directed)

        start_vertex.add_edge(edge)
        if start_vertex != end_vertex:
            end_vertex.add_edge(edge)

        self.__edges.add(edge)

    def remove_edge(self, start_label, end_label, weight=1):
        start_vertex = self.get_vertex(start_label)
        end_vertex = self.get_vertex(end_label)

        if (start_vertex or end_vertex) is None:
            raise ValueError("Can not find start or end vertex in graph")

        edge = Edge(start_vertex, end_vertex, weight, self.__directed)

        if edge not in self.__edges:
            raise ValueError("Can not find edge {0} in graph".format(str(edge)))

        start_vertex.remove_edge(edge)
        end_vertex.remove_edge(edge)
        self.__edges.remove(edge)

    def remove_vertex(self, vertex_label):
        if vertex_label not in self.__vertices:
            raise ValueError("Can not find vertex {0} in graph".format(vertex_label))

        vertex = self.__vertices[vertex_label]

        # remove outbound edges to this vertex for all adjacent vertices
        # make copy of edges in order to avoid RuntimeError : Set changed size during iteration
        inbound_edges_copy = vertex.get_inbound_edges().copy()
        for edge in inbound_edges_copy:
            adjacent_vertex = edge.get_start_vertex()
            adjacent_vertex.remove_edge(edge)

            if edge in self.__edges:
                self.__edges.remove(edge)

        # remove inbound edges from this vertex to all adjacent vertices
        # make copy of edges in order to avoid RuntimeError : Set changed size during iteration
        outbound_edges_copy = vertex.get_outbound_edges().copy()
        for edge in outbound_edges_copy:
            adjacent_vertex = edge.get_end_vertex()
            adjacent_vertex.remove_edge(edge)

            if edge in self.__edges:
                self.__edges.remove(edge)

        # remove vertex from graph
        self.__vertices.pop(vertex_label)

    def get_vertex(self, label):
        return self.__vertices.get(label)

    def get_vertices(self):
        return self.__vertices

    def get_edges(self):
        return self.__edges

    def get_indegree(self, label):
        return len(self.get_vertex(label).get_inbound_edges())

    def get_outdegree(self, label):
        return len(self.get_vertex(label).get_outbound_edges())

    def get_degree(self, label):
        if self.is_directed():
            degree = len(self.get_vertex(label).get_inbound_edges()) + len(
                self.get_vertex(label).get_outbound_edges()
            )
        else:
            degree = len(self.get_vertex(label).get_outbound_edges())
        return degree

    def is_directed(self):
        return self.__directed


if __name__ == "__main__":
    test_graph = Graph()

    test_graph.add_vertex("a")
    test_graph.add_vertex("b")
    test_graph.add_vertex("c")

    test_graph.add_edge("a", "b", 2)
    test_graph.add_edge("a", "c", 7)
    test_graph.add_edge("c", "b", 1)
    test_graph.add_edge("b", "c", 3)

    print(test_graph)
