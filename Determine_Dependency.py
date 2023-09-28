import networkx as nx

def reduce_redundancy(graph, gs):
    for nnode in graph.nodes():
        if graph.nodes[nnode]['phase'] == 0:
            succ_nodes = list(graph.successors(nnode)).copy()
            for snode in succ_nodes:
                if graph[nnode][snode]['dependency'] == 'x':
                    graph.remove_edge(nnode, snode)
                    gs.nodes[snode]['depend_list_x'].remove(nnode)
        elif graph.nodes[nnode]['phase'] == 2:
            for snode in graph.successors(nnode):
                if graph[nnode][snode]['dependency'] == 'x':
                    graph[nnode][snode]['dependency'] = 'z'    
                    gs.nodes[snode]['depend_list_x'].remove(nnode)
                    gs.nodes[snode]['depend_list_z'].append(nnode)       
    return graph.copy(), gs

def signal_shift(graph, gs):
    zgraph = nx.DiGraph()
    for nnode in graph.nodes():
        zgraph.add_node(nnode, pos = graph.nodes[nnode]['pos'])
    
    begin_nodes = []
    end_nodes = []
    # print("hello")
    for nnode in graph.nodes():
        begin_flag = 1
        end_flag = 1
        for pre_node in graph.predecessors(nnode):
            if graph[pre_node][nnode]['dependency'] == 'z':
                begin_flag = 0
                break
        
        for suc_node in graph.successors(nnode):
            if graph[nnode][suc_node]['dependency'] == 'z':
                end_flag = 0
                break      
        
        if begin_flag == 1 and end_flag == 1:
            continue
        elif begin_flag == 1:
            begin_nodes.append(nnode)
        elif end_flag == 1:
            end_nodes.append(nnode)

    edges = list(graph.edges()).copy()
    for edge in edges:
        if graph[edge[0]][edge[1]]['dependency'] == 'z':
            zgraph.add_edge(edge[0], edge[1])
            graph.remove_edge(edge[0], edge[1])
            gs.nodes[edge[1]]['depend_list_z'].remove(edge[0])

    for begin_node in begin_nodes:
        for end_node in end_nodes:
            if nx.has_path(zgraph, source=begin_node, target=end_node):
                graph.add_edge(begin_node, end_node)
                graph[begin_node][end_node]['dependency'] = 'z'
                gs.nodes[end_node]['depend_list_z'].append(begin_node)
    return graph, gs

def determine_dependency(graph):
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
                graph.nodes[snode]['depend_list_x'].append(nnode)
                for ssnode in graph.successors(snode):
                    determined_graph.add_edge(nnode, ssnode)
                    determined_graph[nnode][ssnode]['dependency'] = 'z'
                    graph.nodes[ssnode]['depend_list_z'].append(nnode)
    # pos = nx.get_node_attributes(determined_graph, 'pos')
    # nx.draw(determined_graph, pos = pos, node_size = 30)
    determined_graph, graph = reduce_redundancy(determined_graph, graph)
    # pos = nx.get_node_attributes(determined_graph, 'pos')
    # nx.draw(determined_graph, pos = pos, node_size = 30)
    determined_graph, graph = signal_shift(determined_graph, graph)
    return determined_graph, graph