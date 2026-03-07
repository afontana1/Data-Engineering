class Edge:
    def __init__(self, start_vertex, end_vertex, weight=1, directed=True):
        self.__start_vertex = start_vertex
        self.__end_vertex = end_vertex
        self.__weight = weight
        self.__directed = directed

    def __str__(self):
        if self.__directed:
            print_pattern = "{0} -{1}-> {2}"
        else:
            print_pattern = "{0} <-{1}-> {2}"
        return print_pattern.format(
            self.__start_vertex.get_label(),
            self.__weight,
            self.__end_vertex.get_label(),
        )

    def get_start_vertex(self):
        return self.__start_vertex

    def get_end_vertex(self):
        return self.__end_vertex

    def get_weight(self):
        return self.__weight

    def __lt__(self, other):
        return self.__weight < other.get_weight()

    def __eq__(self, other):
        weight_equal = self.__weight == other.get_weight()
        start_vertex_equal = self.__start_vertex == other.get_start_vertex()
        end_vertex_equal = self.__end_vertex == other.get_end_vertex()

        return weight_equal == start_vertex_equal == end_vertex_equal == True

    def __hash__(self):
        return hash(
            self.__start_vertex.get_label()
            + self.__end_vertex.get_label()
            + str(self.__weight)
        )
