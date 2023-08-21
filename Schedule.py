def schedule(gs, dgraph):
    unmeasured_nodes = []
    for nnode in dgraph.nodes():
        unmeasured_nodes.append(nnode)
        gs.nodes[nnode]['layer'] = 0
    
    while len(unmeasured_nodes):
        copy_unmeasured_nodes = unmeasured_nodes
        for nnode in copy_unmeasured_nodes:
            is_measureable_flag = 1
            for pre_node in dgraph.predecessors(nnode):
                if pre_node in unmeasured_nodes:
                    is_measureable_flag = 0
                    break
            if is_measureable_flag:
                unmeasured_nodes.remove(nnode)
                for pre_node in dgraph.predecessors(nnode):
                    gs.nodes[nnode]['layer'] = max(gs.nodes[nnode]['layer'], gs.nodes[pre_node]['layer'] + 1)
    return gs