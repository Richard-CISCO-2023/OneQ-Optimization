import random
import networkx as nx
import matplotlib.pyplot as plt

def generate_tree(left_bound, right_bound):
    tree_edges = []
    mid_number = random.randint(left_bound, right_bound)
    if mid_number - 1 >= left_bound:
        left_edges, left_root = generate_tree(left_bound, mid_number - 1)
    else:
        left_edges = []
        left_root = -1
    if mid_number + 1 <= right_bound:
        right_edges, right_root = generate_tree(mid_number + 1, right_bound)
    else:
        right_edges = []
        right_root = -1
    tree_edges = left_edges + right_edges
    if left_root >= 0:
        tree_edges.append((mid_number, left_root))
    if right_root >= 0:
        tree_edges.append((mid_number, right_root))
    return tree_edges, mid_number

def create_tree(node_number):
    graph = nx.Graph()
    edges, root = generate_tree(1, node_number)
    for i in range(node_number):
        graph.add_node(i + 1)
        # print (i + 1)
        # graph.add_node(i + 1)
    graph.add_edges_from(edges)
    return graph

def show_graph_tree(graph):
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, node_size=10, node_color='red', arrowsize=20)
    plt.show()
    return

