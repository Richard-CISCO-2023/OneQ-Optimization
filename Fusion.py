import networkx as nx
import matplotlib.pyplot as plt

# def generate_special_graph_with_nodes(num_nodes):
#     G = nx.random_geometric_graph(num_nodes, 0.4)  # Adjust the second parameter for desired distance
#     return G

def show_graph(graph, added_nodes):
    pos = nx.spring_layout(graph)
    colors = []
    for nnode in graph.nodes():
        if nnode in added_nodes:
            colors.append('green')
        else:
            colors.append('red')
    nx.draw(graph, pos, node_size=10, node_color=colors, arrowsize=20)
    plt.show()    

def fusion_graph(graph, max_degree):
    added_nodes =  []
    all_nodes = list(graph.nodes()).copy()
    nodes_size = len(all_nodes)
    for nnode in all_nodes:
        neigh_nnodes = list(graph.neighbors(nnode))
        nnode_degree = len(neigh_nnodes)
        if nnode_degree > max_degree:
            for neigh_nnode in neigh_nnodes:
                graph.remove_edge(nnode, neigh_nnode)
            for i in range(max_degree - 1):
                neigh_nnode = neigh_nnodes[0]
                graph.add_edge(nnode, neigh_nnode)
                neigh_nnodes.remove(neigh_nnode)
            pre_node = nodes_size
            added_nodes.append(nodes_size)
            graph.add_node(nodes_size)
            graph.nodes[nodes_size]['layer'] = graph.nodes[nnode]['layer']
            graph.add_edge(nnode, nodes_size)
            nodes_size += 1
            # show_graph(graph, added_nodes)
            while len(neigh_nnodes):
                if len(neigh_nnodes) > max_degree - 1:
                    for i in range(max_degree - 2):
                        if len(neigh_nnodes) == 0:
                            break
                        neigh_nnode = neigh_nnodes[0]
                        neigh_nnodes.remove(neigh_nnode)
                        graph.add_edge(pre_node, neigh_nnode)
                    added_nodes.append(nodes_size)
                    graph.add_node(nodes_size)
                    graph.nodes[nodes_size]['layer'] = graph.nodes[pre_node]['layer']
                    graph.add_edge(pre_node, nodes_size)
                    pre_node = nodes_size
                    nodes_size += 1
                else:
                    for i in range(max_degree - 1):
                        if len(neigh_nnodes) == 0:
                            break
                        neigh_nnode = neigh_nnodes[0]
                        neigh_nnodes.remove(neigh_nnode)
                        graph.add_edge(pre_node, neigh_nnode)                    
                # show_graph(graph, added_nodes)
        
    return graph, added_nodes
