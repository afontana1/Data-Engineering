class Vertex:
    def __init__(self, label, directed=True):
        self.__label = label
        self.__directed = directed
        self.__edges = set()

    def __str__(self):
        outbound_edges_str = ""
        for edge in self.get_outbound_edges():
            outbound_edges_str += str(edge) + ", "

        inbound_edges_str = ""
        for edge in self.get_inbound_edges():
            inbound_edges_str += str(edge) + ", "

        return "Vertex : {0}, Outbound edges : {1}, Inbound edges : {2}".format(
            self.__label, outbound_edges_str, inbound_edges_str
        )

    def get_outbound_edges(self):
        if self.__directed == False:
            return self.__edges

        outbound_edges = []
        for edge in self.__edges:
            if edge.get_start_vertex() == self:
                outbound_edges.append(edge)

        return outbound_edges

    def get_inbound_edges(self):
        if self.__directed == False:
            return self.__edges

        inbound_edges = []
        for edge in self.__edges:
            if edge.get_end_vertex() == self:
                inbound_edges.append(edge)

        return inbound_edges

    def get_edges(self):
        return self.__edges

    def get_label(self):
        return self.__label

    def add_edge(self, edge):
        self.__edges.add(edge)

    def remove_edge(self, edge):
        if edge in self.__edges:
            self.__edges.remove(edge)
        else:
            raise ValueError(
                "Can not find edge {0} in vertex {1}".format(str(edge), str(self))
            )

    def __eq__(self, other):
        return self.__label == other.get_label()

    def __hash__(self):
        return hash(self.get_label())
