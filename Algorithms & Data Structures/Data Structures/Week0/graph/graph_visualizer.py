from .graph import Graph
from PIL import Image
import pydot
import tempfile


def display_graph(graph, graph_name=None):
    """
    Generate graph image by using pydot and Graphviz
    Display graph image by using PIL (Python Image Library)
    """
    graph_type = "digraph" if graph.is_directed() else "graph"
    pydot_graph = pydot.Dot(graph_type=graph_type)

    if graph_name:
        pydot_graph.set_label(graph_name)

    # draw vertices
    for vertex in graph.get_vertices().values():
        node = pydot.Node(vertex.get_label())
        node.set_style("filled")
        node.set_fillcolor("#a1eacd")
        pydot_graph.add_node(node)

    # draw edges
    for edge in graph.get_edges():
        start_vertex_label = edge.get_start_vertex().get_label()
        end_vertex_label = edge.get_end_vertex().get_label()
        weight = str(edge.get_weight())

        pydot_edge = pydot.Edge(start_vertex_label, end_vertex_label)
        pydot_edge.set_label(weight)
        pydot_graph.add_edge(pydot_edge)

    temp = tempfile.NamedTemporaryFile()
    pydot_graph.write_png(temp.name)

    image = Image.open(temp.name)
    temp.close()

    image.show()
