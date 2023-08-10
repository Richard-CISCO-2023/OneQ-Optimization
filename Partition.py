from Graph_State import *

def is_measurable(gs, measured_nodes, cur_node):
    for pre_node in gs.predecessors(cur_node):
        if pre_node in gs.successors(cur_node):
            continue
        else:
            if pre_node not in measured_nodes:
                return False
    return True


def teleportation(gs, cur_node, unmeasured_nodes):
    for pre_node in gs.predecessors(cur_node):
        if pre_node in gs.successors(cur_node):
            if pre_node in unmeasured_nodes:
                gs.nodes[pre_node]['layer'] = max(gs.nodes[pre_node]['layer'], gs.nodes[cur_node]['layer'])
    return gs

def partition(gs, input_nodes):    
    measured_nodes = []
    unmeaured_nodes = list(gs.nodes()).copy()

    for nnode in unmeaured_nodes:
        gs.nodes[nnode]['layer'] = 0
    
    for input_node in input_nodes:
        measured_nodes.append(input_node)
        unmeaured_nodes.remove(input_node)

    while len(unmeaured_nodes):
        print("unmeasured length", len(unmeaured_nodes))
        unmeaured_nodes_copy = unmeaured_nodes.copy()
        for nnode in unmeaured_nodes_copy:
            if is_measurable(gs, measured_nodes, nnode):
                for pre_node in gs.predecessors(nnode):
                    if pre_node in gs.successors(nnode):
                        gs.nodes[nnode]['layer'] = max(gs.nodes[nnode]['layer'], gs.nodes[pre_node]['layer'])
                    else:
                        gs.nodes[nnode]['layer'] = max(gs.nodes[nnode]['layer'], gs.nodes[pre_node]['layer'] + 1)
                measured_nodes.append(nnode)
                unmeaured_nodes.remove(nnode)
                teleportation(gs, nnode, unmeaured_nodes)
    return gs