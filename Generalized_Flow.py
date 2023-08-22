# (X, Y) plane

def odd(graph, node_set):
    odd_nodes = set()
    for nnode in graph.nodes():
        neigh_nodes = set(graph.neighbors(nnode))
        if len(node_set & neigh_nodes) % 2 == 1:
            odd_nodes.add(nnode)
    return odd_nodes

def even(graph, node_set):
    even_nodes = set()
    for nnode in graph.nodes():
        neigh_nodes = set(graph.neighbors(nnode))
        if len(node_set & neigh_nodes) % 2 == 0:
            even_nodes.add(nnode)
    return even_nodes    

def is_measurable(graph, node, unmeasured_nodes):
    future_nodes = odd(graph, {node})
    past_nodes = even(graph, future_nodes)
    is_measurabled = True
    for pnode in past_nodes:
        if pnode in unmeasured_nodes:
            is_measurabled = False
            break
    return is_measurabled, past_nodes

def generaized_flow(graph):
    for nnode in graph.nodes():
        graph.nodes[nnode]['layer'] = 0
    unmeasured_nodes = []
    for nnode in graph.nodes():
        is_measurabled, past_nodes = is_measurable(graph, nnode, unmeasured_nodes)
        if is_measurabled:
            for pnode in past_nodes:
                graph.nodes[nnode]['layer'] = max(graph.nodes[nnode]['layer'], graph.nodes[pnode]['layer'] + 1)
    return graph