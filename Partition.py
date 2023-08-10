from Graph_State import *

def is_measurable(gs, measured_nodes, cur_node):
    is_measurable_flag = True
    pre_nodes = []
    visited_nodes = []
    visited = {}
    for nnode in gs.nodes():
        visited[nnode] = 0

    for pre_node in gs.predecessors(cur_node):
        if visited[pre_node] == 0:
            if pre_node in gs.successors(cur_node):
                if pre_node not in measured_nodes:
                    visited_nodes.append(pre_node)
                else:
                    pre_nodes.append(pre_node)
            else:
                if pre_node not in measured_nodes:
                    return False, pre_nodes
                else:
                    pre_nodes.append(pre_node)
            visited[pre_node] = 1
    while len(visited_nodes):
        visited_nodes.clear()
        visited_nodes_copy = visited_nodes.copy()
        for nnode in visited_nodes_copy:
            for pre_node in gs.predecessors(nnode):
                if visited[pre_node] == 0:
                    if pre_node in gs.successors(nnode):
                        visited_nodes.append(pre_node)
                    else:
                        if pre_node not in measured_nodes:
                            return False, pre_nodes
                        else:
                            pre_nodes.append(pre_node)           
                    visited[pre_node] = 1 

    return True, pre_nodes


# def teleportation(gs, cur_node, unmeasured_nodes):
#     for pre_node in gs.predecessors(cur_node):
#         if pre_node in gs.successors(cur_node):
#             if pre_node in unmeasured_nodes:
#                 gs.nodes[pre_node]['layer'] = max(gs.nodes[pre_node]['layer'], gs.nodes[cur_node]['layer'])
#     return gs

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
        unmeasured_nodes_copy = unmeaured_nodes.copy()
        for nnode in unmeasured_nodes_copy:
            is_measurabled, pre_nodes = is_measurable(gs, measured_nodes, nnode)
            if is_measurabled:
                for pre_node in pre_nodes:
                    if pre_node in gs.successors(nnode):
                        gs.nodes[nnode]['layer'] = max(gs.nodes[nnode]['layer'], gs.nodes[pre_node]['layer'])
                    else:
                        gs.nodes[nnode]['layer'] = max(gs.nodes[nnode]['layer'], gs.nodes[pre_node]['layer'] + 1)
                measured_nodes.append(nnode)
                unmeaured_nodes.remove(nnode)
                # teleportation(gs, nnode, unmeaured_nodes)
    return gs