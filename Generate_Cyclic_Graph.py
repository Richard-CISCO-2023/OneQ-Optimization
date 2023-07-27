import random
import networkx as nx
import matplotlib.pyplot as plt
from Generate_Tree import *

MAX_EDGES_ADD = 6

def generate_cyclic_graph(node_number):
    graph = create_tree(node_number)
    add_edges_number = random.randint(1, MAX_EDGES_ADD)
    for i in range(add_edges_number):
        node1 = 0
        node2 = 0
        for node in graph.nodes():
            if len(list(graph.neighbors(node))) == 1 and node1 == 0:   
                node1 = node
            elif len(list(graph.neighbors(node))) == 1 and node2 == 0:
                node2 = node
            elif node1 != 0 and node2 != 0:
                break
        if node1 == 0 or node2 == 0:
            break
        graph.add_edge(node1, node2)
    return graph

def show_cyclic_graph(graph):
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, node_size=10, node_color='red', arrowsize=20)
    plt.show()