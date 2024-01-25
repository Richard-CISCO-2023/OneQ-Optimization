from matplotlib import pyplot as plt
import networkx as nx

def reduce_redundancy(graph):
    for nnode in graph.nodes():
        if graph.nodes[nnode]['phase'] == 0:
            succ_nodes = list(graph.successors(nnode)).copy()
            for snode in succ_nodes:
                if graph[nnode][snode]['dependency'] == 'x':
                    graph.remove_edge(nnode, snode)
        elif graph.nodes[nnode]['phase'] == 2:
            for snode in graph.successors(nnode):
                if graph[nnode][snode]['dependency'] == 'x':
                    graph[nnode][snode]['dependency'] = 'z'       
    return graph.copy()

def signal_shift(graph):

    input_nodes = []
    output_nodes = []

    for nnode in graph.nodes():
        if len(list(graph.predecessors(nnode))) == 0:
            input_nodes.append(nnode)
        if len(list(graph.successors(nnode))) == 0:
            output_nodes.append(nnode)

    zgraph = nx.DiGraph()
    for nnode in graph.nodes():
        zgraph.add_node(nnode, pos = graph.nodes[nnode]['pos'])
    
    for edge in graph.edges():
        if graph[edge[0]][edge[1]]['dependency'] == 'z':
            zgraph.add_edge(edge[0], edge[1])   
    
    while 1:
        shift_z_edges = []
        for zedge in zgraph.edges():
            if len(list(zgraph.predecessors(zedge[0]))) == 0 and len(list(graph.successors(zedge[1]))) != 0:
                shift_z_edges.append(zedge)
        
        if len(shift_z_edges) == 0:
            break

        for sze in shift_z_edges:
            head_node = sze[0]
            tail_node = sze[1]
            neigh_tail_nodes = list(graph.successors(tail_node)).copy()
            for ntn in neigh_tail_nodes:
                if graph[tail_node][ntn]['dependency'] == 'z':
                    if not (graph.has_edge(head_node, ntn) and graph[head_node][ntn]['dependency'] == 'z'):
                        graph.add_edge(head_node, ntn)
                        graph[head_node][ntn]['dependency'] = 'z'
                        zgraph.add_edge(head_node, ntn )

                elif graph[tail_node][ntn]['dependency'] == 'x':
                    if not (graph.has_edge(head_node, ntn) and graph[head_node][ntn]['dependency'] == 'x'):
                        graph.add_edge(head_node, ntn)
                        graph[head_node][ntn]['dependency'] = 'x'
            graph.remove_edge(sze[0], sze[1])
            zgraph.remove_edge(sze[0], sze[1])
    print ("shift signal finished")    
    return graph

def draw_graph(graph, title = "Graph" , colours=None, labels = None):
    #pos = nx.get_node_attributes(graph, 'pos')
    #node_colours = nx.get_node_attributes(graph, '')
    #pos = nx.spring_layout(graph)
    pos = nx.kamada_kawai_layout(graph, scale = 2)
    pos = nx.shell_layout(graph)
    plt.figure()
    nx.draw_networkx_nodes(graph, pos=pos, node_color= colours,  node_size=30)
    nx.draw_networkx_labels(graph, pos=pos, labels = labels , font_size= 6)
    # Separate edges by dependency
    edges_x = [(u, v) for u, v, d in graph.edges(data=True) if d.get('dependency') == 'x']
    edges_z = [(u, v) for u, v, d in graph.edges(data=True) if d.get('dependency') == 'z']
    
    # Draw 'dependency x' edges as dotted lines
    nx.draw_networkx_edges(graph, pos, edgelist=edges_x, style='solid', edge_color= 'red')
    
    # Draw 'dependency z' edges as solid lines (default)
    nx.draw_networkx_edges(graph, pos, edgelist=edges_z, style='dotted', edge_color= 'green')
    
    edge_labels = nx.get_edge_attributes(graph, 'dependency')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    plt.title(title)
    plt.show()

def determine_dependency(graph, colours, labels):
    determined_graph = nx.DiGraph()
    for nnode in graph.nodes():
        determined_graph.add_node(nnode, pos = graph.nodes[nnode]['pos'], phase = graph.nodes[nnode]['phase'])
        graph.nodes[nnode]['depend_list_x'] = []
        graph.nodes[nnode]['depend_list_z'] = []
    
    for nnode in graph.nodes():
        for snode in graph.successors(nnode):
            if snode not in graph.predecessors(nnode):
                determined_graph.add_edge(nnode, snode)
                determined_graph[nnode][snode]['dependency'] = 'x'
                for ssnode in graph.successors(snode):
                    determined_graph.add_edge(nnode, ssnode)
                    determined_graph[nnode][ssnode]['dependency'] = 'z'
                    print("Added X dependency")
    pos = nx.get_node_attributes(determined_graph, 'pos')

    print('-------------- \nBelow is determine_dependency result \n-------------- ')
    
    print('-------------- \nStep 1.) determined_graph\n-------------- ')
    draw_graph(determined_graph, colours = colours, labels= labels , title = "determine_dependency graph" )
    #plt.figure()
    #nx.draw(determined_graph, pos = pos, node_size = 30)
    #plt.title("Determine Dependency graph")

    print('-------------- \nStep 2.) reduce_redudancy\n-------------- ')
    determined_graph = reduce_redundancy(determined_graph)
    draw_graph(determined_graph, title = "reduced redundancy determine dependency graph",colours = colours,  labels= labels)
    #pos = nx.get_node_attributes(determined_graph, 'pos')
    #plt.figure()
    #nx.draw(determined_graph, pos = pos, node_size = 30)
    
    print('-------------- \nStep 3.) signal shifted determine dependency graph\n-------------- ')
    determined_graph = signal_shift(determined_graph)
    draw_graph(determined_graph, title = "Signal shifted Determine Dependency graph", colours = colours,  labels= labels)
    
    return determined_graph

