import networkx as nx
import matplotlib.pyplot as plt
import math
from Generate_State import *

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
    plt.figure()
    nx.draw(graph, pos, node_size=10, node_color=colors, arrowsize=20)
    plt.title("Show Graph")
    plt.show()    

def fusion_graph_dynamic(graph, max_degree, StarStructure, SpecialFusion):
    if StarStructure or max_degree <= 4:
        fusions = 0
        added_nodes =  []
        all_nodes = list(graph.nodes()).copy()
        nodes_size = len(all_nodes)
        for nnode in all_nodes:
            graph.nodes[nnode]['parent'] = nnode
        for nnode in all_nodes:
            neigh_nnodes = list(graph.neighbors(nnode))
            nnode_degree = len(neigh_nnodes)
            if nnode_degree > max_degree - 1:
                neighbor_con_qubits = {}
                for neigh_nnode in neigh_nnodes:
                    neighbor_con_qubits[neigh_nnode] = graph[nnode][neigh_nnode]['con_qubits'][neigh_nnode]
                    graph.remove_edge(nnode, neigh_nnode)
                    fusions -= 1
                for i in range(max_degree - 2):
                    neigh_nnode = neigh_nnodes[0]
                    graph.add_edge(nnode, neigh_nnode)
                    graph[nnode][neigh_nnode]['con_qubits'] = {}
                    graph[nnode][neigh_nnode]['con_qubits'][nnode] = 0
                    graph[nnode][neigh_nnode]['con_qubits'][neigh_nnode] = neighbor_con_qubits[neigh_nnode]
                    fusions += 1
                    neigh_nnodes.remove(neigh_nnode)
                pre_node = nodes_size
                added_nodes.append(nodes_size)
                graph.add_node(nodes_size)
                graph.nodes[nodes_size]['parent'] = graph.nodes[nnode]['parent']
                graph.add_edge(nnode, nodes_size)
                graph[nnode][nodes_size]['con_qubits'] = {}
                graph[nnode][nodes_size]['con_qubits'][nnode] = 0
                graph[nnode][nodes_size]['con_qubits'][nodes_size] = 1
                fusions += 1
                nodes_size += 1
                show_graph(graph, added_nodes)
                while len(neigh_nnodes):
                    if len(neigh_nnodes) > max_degree - 1:
                        for i in range(max_degree - 2):
                            if len(neigh_nnodes) == 0:
                                break
                            neigh_nnode = neigh_nnodes[0]
                            neigh_nnodes.remove(neigh_nnode)
                            graph.add_edge(pre_node, neigh_nnode)
                            graph[pre_node][neigh_nnode]['con_qubits'] = {}
                            graph[pre_node][neigh_nnode]['con_qubits'][pre_node] = 0
                            graph[pre_node][neigh_nnode]['con_qubits'][neigh_nnode] = neighbor_con_qubits[neigh_nnode]
                            fusions += 1
                        added_nodes.append(nodes_size)
                        graph.add_node(nodes_size)
                        graph.nodes[nodes_size]['parent'] = graph.nodes[pre_node]['parent']
                        graph.add_edge(pre_node, nodes_size)
                        graph[pre_node][nodes_size]['con_qubits'] = {}
                        graph[pre_node][nodes_size]['con_qubits'][pre_node] = 0
                        graph[pre_node][nodes_size]['con_qubits'][nodes_size] = 1
                        fusions += 1
                        pre_node = nodes_size
                        nodes_size += 1
                    else:
                        for i in range(max_degree - 1):
                            if len(neigh_nnodes) == 0:
                                break
                            neigh_nnode = neigh_nnodes[0]
                            neigh_nnodes.remove(neigh_nnode)
                            graph.add_edge(pre_node, neigh_nnode)  
                            graph[pre_node][neigh_nnode]['con_qubits'] = {}
                            graph[pre_node][neigh_nnode]['con_qubits'][pre_node] = 0
                            graph[pre_node][neigh_nnode]['con_qubits'][neigh_nnode] = neighbor_con_qubits[neigh_nnode]
                            fusions += 1       
    else:
        fusions = 0
        added_nodes =  []
        all_nodes = list(graph.nodes()).copy()
        nodes_size = len(all_nodes)
        for nnode in all_nodes:
            graph.nodes[nnode]['parent'] = nnode
        for nnode in all_nodes:
            neigh_nnodes = list(graph.neighbors(nnode))
            nnode_degree = len(neigh_nnodes)
            if nnode_degree > 2:
                neighbor_con_qubits = {}
                for neigh_nnode in neigh_nnodes:
                    neighbor_con_qubits[neigh_nnode] = graph[nnode][neigh_nnode]['con_qubits'][neigh_nnode]
                    graph.remove_edge(nnode, neigh_nnode)
                    fusions -= 1
                neigh_nnode = neigh_nnodes[0]
                graph.add_edge(nnode, neigh_nnode)
                graph[nnode][neigh_nnode]['con_qubits'] = {}
                graph[nnode][neigh_nnode]['con_qubits'][nnode] = 0
                graph[nnode][neigh_nnode]['con_qubits'][neigh_nnode] = neighbor_con_qubits[neigh_nnode]
                fusions += 1
                neigh_nnodes.remove(neigh_nnode)
                pre_node = nodes_size
                added_nodes.append(nodes_size)
                graph.add_node(nodes_size)
                graph.nodes[nodes_size]['phase'] = []
                graph.nodes[nodes_size]['parent'] = graph.nodes[nnode]['parent']
                graph.add_edge(nnode, nodes_size)
                graph[nnode][nodes_size]['con_qubits'] = {}
                graph[nnode][nodes_size]['con_qubits'][nnode] = 0
                graph[nnode][nodes_size]['con_qubits'][nodes_size] = 1
                fusions += 1
                nodes_size += 1
                show_graph(graph, added_nodes)
                while len(neigh_nnodes):
                    if len(neigh_nnodes) > 2:
                        if len(neigh_nnodes) == 0:
                            break
                        neigh_nnode = neigh_nnodes[0]
                        neigh_nnodes.remove(neigh_nnode)
                        graph.add_edge(pre_node, neigh_nnode)
                        graph[pre_node][neigh_nnode]['con_qubits'] = {}
                        graph[pre_node][neigh_nnode]['con_qubits'][pre_node] = 0
                        graph[pre_node][neigh_nnode]['con_qubits'][neigh_nnode] = neighbor_con_qubits[neigh_nnode]
                        fusions += 1
                        added_nodes.append(nodes_size)
                        graph.add_node(nodes_size)
                        graph.nodes[nodes_size]['phase'] = []
                        graph.nodes[nodes_size]['parent'] = graph.nodes[pre_node]['parent']
                        graph.add_edge(pre_node, nodes_size)
                        graph[pre_node][nodes_size]['con_qubits'] = {}
                        graph[pre_node][nodes_size]['con_qubits'][pre_node] = 0
                        graph[pre_node][nodes_size]['con_qubits'][nodes_size] = 1
                        fusions += 1
                        pre_node = nodes_size
                        nodes_size += 1
                    else:
                        for i in range(2):
                            if len(neigh_nnodes) == 0:
                                break
                            neigh_nnode = neigh_nnodes[0]
                            neigh_nnodes.remove(neigh_nnode)
                            graph.add_edge(pre_node, neigh_nnode)  
                            graph[pre_node][neigh_nnode]['con_qubits'] = {}
                            graph[pre_node][neigh_nnode]['con_qubits'][pre_node] = 0
                            graph[pre_node][neigh_nnode]['con_qubits'][neigh_nnode] = neighbor_con_qubits[neigh_nnode]
                            fusions += 1     

        for nnode in graph.nodes():
            graph.nodes[nnode]['avail_qubits'] = []
            for i in range(max_degree):
                graph.nodes[nnode]['avail_qubits'].append(i)

        for edge in graph.edges():
            if graph[edge[0]][edge[1]]['con_qubits'][edge[0]] == 0:
                if 0 in graph.nodes[edge[0]]['avail_qubits']:
                    graph.nodes[edge[0]]['avail_qubits'].remove(0)
                else:
                    graph.nodes[edge[0]]['avail_qubits'].remove(max_degree - 1)
                    graph[edge[0]][edge[1]]['con_qubits'][edge[0]] = max_degree -1
            else:
                graph.nodes[edge[0]]['avail_qubits'].remove(graph[edge[0]][edge[1]]['con_qubits'][edge[0]])
            
            if graph[edge[0]][edge[1]]['con_qubits'][edge[1]] == 0:
                if 0 in graph.nodes[edge[1]]['avail_qubits']:
                    graph.nodes[edge[1]]['avail_qubits'].remove(0)
                else:
                    graph.nodes[edge[1]]['avail_qubits'].remove(max_degree - 1)
                    graph[edge[0]][edge[1]]['con_qubits'][edge[1]] = max_degree -1
            else:
                graph.nodes[edge[1]]['avail_qubits'].remove(graph[edge[0]][edge[1]]['con_qubits'][edge[1]])
        if SpecialFusion:
            # line fusion added part  
            all_nodes = graph.nodes()
            degree_two_nodes = []
            for gnode in all_nodes:
                if len(list(graph.neighbors(gnode))) == 2:
                    degree_two_nodes.append(gnode)

            while len(degree_two_nodes) >= 1:
                cur_node = degree_two_nodes[0]
                degree_two_nodes.remove(cur_node)
                path = [cur_node]
                extend_flag = 1
                while extend_flag:
                    extend_flag = 0
                    neigh_head_nodes = list(graph.neighbors(path[0]))
                    for nnode in neigh_head_nodes:
                        if nnode not in path and nnode in degree_two_nodes:
                        # if nnode not in path and nnode in degree_two_nodes and graph.nodes[nnode]['parent'] == graph.nodes[path[0]]['parent']:
                            extend_flag = 1
                            degree_two_nodes.remove(nnode)
                            path = [nnode] + path
                            break
                    
                    neigh_tail_nodes = graph.neighbors(path[-1])
                    for nnode in neigh_tail_nodes:
                        if nnode not in path and nnode in degree_two_nodes:
                        # if nnode not in path and nnode in degree_two_nodes and graph.nodes[nnode]['parent'] == graph.nodes[path[-1]]['parent']:
                            extend_flag = 1
                            degree_two_nodes.remove(nnode)
                            path.append(nnode)
                            break

                neigh_head_nodes = graph.neighbors(path[0])
                for nnode in neigh_head_nodes:
                    if nnode not in path:
                        head_node = nnode
                        break  

                neigh_tail_nodes = graph.neighbors(path[-1])
                for nnode in neigh_tail_nodes:
                    if nnode not in path and nnode != head_node:
                        tail_node = nnode
                        break      
                
                parent = graph.nodes[path[0]]['parent']    
                number_nodes_to_be_connected = math.ceil(len(path) / (max_degree - 2))
                head_con = graph[head_node][path[0]]['con_qubits'][head_node]
                tail_con = graph[path[-1]][tail_node]['con_qubits'][tail_node]    
                if len(path) <= max_degree - 3:
                    if graph[head_node][path[0]]['con_qubits'][head_node] == max_degree - 1:
                    # if (graph[head_node][path[0]]['con_qubits'][head_node] == 0 or graph[head_node][path[0]]['con_qubits'][head_node] == max_degree - 1) and graph.nodes[head_node]['parent'] == parent:
                        pre_node = head_node
                        for pnode in path:
                            graph.remove_edge(pre_node, pnode)
                            graph.nodes[head_node]['phase'] = graph.nodes[head_node]['phase'] + graph.nodes[pnode]['phase']
                            if pre_node != head_node:
                                graph.remove_node(pre_node)
                            pre_node = pnode
                        graph.remove_edge(pre_node, tail_node)
                        graph.remove_node(pre_node)
                        graph.add_edge(head_node, tail_node)
                        graph[head_node][tail_node]['con_qubits'] = {}
                        graph[head_node][tail_node]['con_qubits'][head_node] = head_con
                        graph[head_node][tail_node]['con_qubits'][tail_node] = tail_con
                        continue
                    elif graph[path[-1]][tail_node]['con_qubits'][tail_node] == max_degree - 1:
                    # elif (graph[path[-1]][tail_node]['con_qubits'][tail_node] == 0 or graph[path[-1]][tail_node]['con_qubits'][tail_node] == max_degree - 1) and graph.nodes[tail_node]['parent'] == parent:
                        pre_node = head_node
                        phase_list = []
                        for pnode in path:
                            phase_list = graph.nodes[pnode]['phase'] + phase_list
                            graph.remove_edge(pre_node, pnode)
                            if pre_node != head_node:
                                graph.remove_node(pre_node)
                            pre_node = pnode
                        graph.remove_edge(pre_node, tail_node)
                        graph.remove_node(pre_node)
                        graph.add_edge(head_node, tail_node)
                        graph.nodes[tail_node]['phase'] = graph.nodes[tail_node]['phase'] + phase_list
                        graph[head_node][tail_node]['con_qubits'] = {}
                        graph[head_node][tail_node]['con_qubits'][head_node] = head_con
                        graph[head_node][tail_node]['con_qubits'][tail_node] = tail_con
                        continue                    
                # print(path)
                
                path.append(tail_node)
                pre_node = head_node
                phase_list = []
                for pnode in path:
                    # print(pre_node, pnode)
                    graph.remove_edge(pre_node, pnode)
                    if pre_node != head_node:
                        graph.remove_node(pre_node)
                        phase_list = phase_list + graph.nodes[pnode]['phase']
                    pre_node = pnode
                
                pre_node = head_node
                for i in range(number_nodes_to_be_connected):
                    graph.add_node(nodes_size)
                    graph.nodes[nodes_size]['phase'] = []
                    for i in range(max_degree - 2):
                        if len(phase_list) == 0:
                            break
                        cur_phase = phase_list[0]
                        phase_list.remove(cur_phase)
                        graph.nodes[nodes_size]['phase'].append(cur_phase)
                    graph.nodes[nodes_size]['parent'] = parent
                    graph.add_edge(pre_node, nodes_size)
                    graph[pre_node][nodes_size]['con_qubits'] = {}
                    if pre_node == head_node:
                        graph[pre_node][nodes_size]['con_qubits'][pre_node] = head_con
                    else:
                        graph[pre_node][nodes_size]['con_qubits'][pre_node] = 0
                        graph.nodes[pre_node]['avail_nodes'].remove(0)
                    graph.nodes[nodes_size]['avail_nodes'] = []
                    for i in range(max_degree):
                        graph.nodes[nodes_size]['avail_nodes'].append(i)
                    graph[pre_node][nodes_size]['con_qubits'][nodes_size] = max_degree - 1
                    graph.nodes[nodes_size]['avail_nodes'].remove(max_degree - 1)
                    pre_node = nodes_size
                    nodes_size += 1

                graph.add_edge(pre_node, tail_node)
                graph[pre_node][tail_node]['con_qubits'] = {}
                if pre_node == head_node:
                    graph[pre_node][tail_node]['con_qubits'][pre_node] = head_con
                else:
                    graph[pre_node][tail_node]['con_qubits'][pre_node] = 0
                    graph.nodes[pre_node]['avail_nodes'].remove(0)
                graph[pre_node][tail_node]['con_qubits'][tail_node] = tail_con 

        for nnode in graph.nodes():
            graph.nodes[nnode]['avail_qubits_vali'] = []
            for i in range(max_degree):
                graph.nodes[nnode]['avail_qubits_vali'].append(i)
        
        for edge in graph.edges():
            if graph[edge[0]][edge[1]]['con_qubits'][edge[0]] in graph.nodes[edge[0]]['avail_qubits_vali']:
                graph.nodes[edge[0]]['avail_qubits_vali'].remove(graph[edge[0]][edge[1]]['con_qubits'][edge[0]])
            else:
                print("fusion connected qubits validation error1!")
                return graph, added_nodes

            if graph[edge[0]][edge[1]]['con_qubits'][edge[1]] in graph.nodes[edge[1]]['avail_qubits_vali']:
                graph.nodes[edge[1]]['avail_qubits_vali'].remove(graph[edge[0]][edge[1]]['con_qubits'][edge[1]])
            else:
                print("fusion connected qubits validation error2!")
                return graph, added_nodes          
        print("fusion connected qubits validation success!")
        show_graph(graph, added_nodes)
    # print("fusions:", fusions)    
    return graph, added_nodes

def fusion_graph(graph, max_degree, StarStructure):
    if StarStructure:
        added_nodes =  []
        all_nodes = list(graph.nodes()).copy()
        nodes_size = len(all_nodes)
        for nnode in all_nodes:
            neigh_nnodes = list(graph.neighbors(nnode))
            nnode_degree = len(neigh_nnodes)
            if nnode_degree > max_degree - 1:
                neighbor_con_qubits = {}
                for neigh_nnode in neigh_nnodes:
                    neighbor_con_qubits[neigh_nnode] = graph[nnode][neigh_nnode]['con_qubits'][neigh_nnode]
                    graph.remove_edge(nnode, neigh_nnode)
                for i in range(max_degree - 2):
                    neigh_nnode = neigh_nnodes[0]
                    graph.add_edge(nnode, neigh_nnode)
                    graph[nnode][neigh_nnode]['con_qubits'] = {}
                    graph[nnode][neigh_nnode]['con_qubits'][nnode] = 0
                    graph[nnode][neigh_nnode]['con_qubits'][neigh_nnode] = 0
                    neigh_nnodes.remove(neigh_nnode)
                pre_node = nodes_size
                added_nodes.append(nodes_size)
                graph.add_node(nodes_size)
                graph.nodes[nodes_size]['layer'] = graph.nodes[nnode]['layer']
                graph.add_edge(nnode, nodes_size)
                graph[nnode][nodes_size]['con_qubits'] = {}
                graph[nnode][nodes_size]['con_qubits'][nnode] = 0
                graph[nnode][nodes_size]['con_qubits'][nodes_size] = 1
                nodes_size += 1
                show_graph(graph, added_nodes)
                while len(neigh_nnodes):
                    if len(neigh_nnodes) > max_degree - 1:
                        for i in range(max_degree - 2):
                            if len(neigh_nnodes) == 0:
                                break
                            neigh_nnode = neigh_nnodes[0]
                            neigh_nnodes.remove(neigh_nnode)
                            graph.add_edge(pre_node, neigh_nnode)
                            graph[pre_node][neigh_nnode]['con_qubits'] = {}
                            graph[pre_node][neigh_nnode]['con_qubits'][pre_node] = 0
                            graph[pre_node][neigh_nnode]['con_qubits'][neigh_nnode] = neighbor_con_qubits[neigh_nnode]
                        added_nodes.append(nodes_size)
                        graph.add_node(nodes_size)
                        graph.nodes[nodes_size]['layer'] = graph.nodes[pre_node]['layer']
                        graph.add_edge(pre_node, nodes_size)
                        graph[pre_node][nodes_size]['con_qubits'] = {}
                        graph[pre_node][nodes_size]['con_qubits'][pre_node] = 0
                        graph[pre_node][nodes_size]['con_qubits'][nodes_size] = 1                
                        pre_node = nodes_size
                        nodes_size += 1
                    else:
                        for i in range(max_degree - 1):
                            if len(neigh_nnodes) == 0:
                                break
                            neigh_nnode = neigh_nnodes[0]
                            neigh_nnodes.remove(neigh_nnode)
                            graph.add_edge(pre_node, neigh_nnode)     
                            graph[pre_node][neigh_nnode]['con_qubits'] = {}
                            graph[pre_node][neigh_nnode]['con_qubits'][pre_node] = 0
                            graph[pre_node][neigh_nnode]['con_qubits'][neigh_nnode] = neighbor_con_qubits[neigh_nnode]               
                    show_graph(graph, added_nodes)
        
    return graph, added_nodes


def get_basic_rs(rs):
    '''
    INPUT
    rs = networkx graph object G, generate_state output
    '''

    rnode_with_max_degree = 0
    avail_to_visit = {} # Dictionary for qubit index : 0 = visited , 1 = unvisted
    depths = []

    # Looking through the nodes and neighbours 
    # Attempted find the highest degree node made.
    for rnode in rs.nodes():
        avail_to_visit[rnode] = 1 # Setting all nodes in RS to unvisted 
        if len(list(rs.neighbors(rnode))) > len(list(rs.neighbors(rnode_with_max_degree))):
            rnode_with_max_degree = rnode
    
    # Analysing the neighbours of rnode_with_max_degree
    neigh_rnodes = list(rs.neighbors(rnode_with_max_degree))
    pre_degree_nodes = []
    avail_to_visit[rnode_with_max_degree] = 0
    while len(neigh_rnodes):
        neigh_rnode = neigh_rnodes[0] # Visiting first term
        neigh_rnodes.remove(neigh_rnode) # Removing it so that 2nd term is ready to be first term
        avail_to_visit[neigh_rnode] = 0 # Marking as visted 
        pre_degree_nodes.append(neigh_rnode)  # Adding visted to list

        # Beginning of traversal
        # Looked at the next neighbour 
        for nneigh_rnode in rs.neighbors(neigh_rnode): # Looking at the neighbours/next neighbours (nb nb) of rnode_with_max_degree
            if nneigh_rnode in neigh_rnodes: # If the nb nb is also a neighbour of rnode_with_max_degree...
                neigh_rnodes.remove(nneigh_rnode) # Remove it & assign it as visited
                avail_to_visit[nneigh_rnode] = 0
            else:
                if avail_to_visit[nneigh_rnode] > 0: # If the next neighbour has not been visited...
                    avail_to_visit[nneigh_rnode] = - 1 # ...mark as visited/ 
                elif avail_to_visit[nneigh_rnode] < 0:# ...otherwise keep visited?
                    avail_to_visit[nneigh_rnode] = 0 

    max_degree = len(pre_degree_nodes) # Number connections highest node has.
    if max_degree < 2:
        return depths, max_degree, 0
    depth = 2
    
    while len(pre_degree_nodes):
        degree_nodes = []
        for pre_dnode in pre_degree_nodes: # For each neighbour of max degree...
            neigh_pre_nodes = []
            for neigh_pre_node in rs.neighbors(pre_dnode): # For next neighbours of that node...
                if avail_to_visit[neigh_pre_node] != 0: # If it has been visited 
                    neigh_pre_nodes.append(neigh_pre_node) # Store it
            if len(neigh_pre_nodes):
                new_node = neigh_pre_nodes[len(neigh_pre_nodes) // 2] 
                degree_nodes.append(new_node) 
                avail_to_visit[new_node] = 0
                for neigh_pre_node in neigh_pre_nodes:
                    if neigh_pre_node != new_node:
                        avail_to_visit[neigh_pre_node] = 0
                for neigh_new_node in rs.neighbors(new_node):
                    if avail_to_visit[neigh_new_node] > 0:
                        avail_to_visit[neigh_new_node] = -1
                    elif avail_to_visit[neigh_new_node] < 0:
                        avail_to_visit[neigh_new_node] = 0
            else:
                depths.append(depth)

        depth += 1
        pre_degree_nodes = degree_nodes

    rnode_with_min_degree = 0

    for rnode in rs.nodes():
        if len(list(rs.neighbors(rnode_with_min_degree))) == 0:
            rnode_with_min_degree = rnode
        avail_to_visit[rnode] = 1
        if len(list(rs.neighbors(rnode))) < len(list(rs.neighbors(rnode_with_min_degree))) and len(list(rs.neighbors(rnode))) != 0:
            rnode_with_min_degree = rnode

    avail_to_visit[rnode_with_min_degree] = 0

    all_nodes = list(rs.nodes()).copy()
    for rnode in all_nodes:
        if len(list(rs.neighbors(rnode))) == 0:
            rs.remove_node(rnode)

    if len(list(rs.nodes())):
        cur_node = list(rs.nodes())[0]
        line = [cur_node, list(rs.neighbors(cur_node))[0]]
        rs.remove_edge(line[0], line[1])
        while cur_node != -1:
            # print(line)
            cur_node = -1
            if line[0] in rs.nodes():
                neigh_nodes = list(rs.neighbors(line[0]))
                if len(neigh_nodes) != 0:
                    cur_node = neigh_nodes[0]
                    for neigh_node in neigh_nodes:
                        rs.remove_edge(line[0], neigh_node)
                        if neigh_node != cur_node:
                            nneigh_nodes = list(rs.neighbors(neigh_node)).copy()
                            for nneigh_node in nneigh_nodes:
                                rs.remove_edge(neigh_node, nneigh_node)
                            rs.remove_node(neigh_node)
                    rs.remove_node(line[0])
                    line = [cur_node] + line
            if line[-1] in rs.nodes():
                neigh_nodes = list(rs.neighbors(line[-1]))
                if len(neigh_nodes) != 0:
                    cur_node = neigh_nodes[0]
                    for neigh_node in neigh_nodes:
                        rs.remove_edge(line[-1], neigh_node)
                        if neigh_node != cur_node:
                            nneigh_nodes = list(rs.neighbors(neigh_node)).copy()
                            for nneigh_node in nneigh_nodes:
                                rs.remove_edge(neigh_node, nneigh_node)
                            rs.remove_node(neigh_node)
                    rs.remove_node(line[-1])
                    line = line + [cur_node]
        max_length = len(line)


    else:
        max_length = 0
    return depths, max_degree, max_length

def fusion_dynamic_general(graph, rs):
    """
    PURPOSE
    -------------
    INPUT
    graph = undirected graph of the converted pyZX circuit
    rs = resource state that is randomly generated
    ------------
    OUTPUT
    graph = new edited graph that should now represent the fusion
    """
    # Obtaining resource state parameters to inform building
    depths, max_degree, max_length = get_basic_rs(rs)

    # Excluding generations that have too little entanglement.
    if max_degree < 2:
        print ("MAX DEGREE WAS LESS THAN 2")
        return -1 
    print(f'The depth {depths}, Max degree, {max_degree}, Max length {max_length}')

    # Initialising variables
    fusions = 0
    added_nodes =  [] 

    # Details of nodes of undirected graph. 
    all_nodes = list(graph.nodes()).copy() # Returns  [  (n, ddict), ... ] 
    nodes_size = len(all_nodes) # total no. nodes in the graph?
    
    for nnode in all_nodes:
        graph.nodes[nnode]['parent'] = nnode # Access nnode attribute of a node in graph.
                                             # Assign it's parent attribute to be nnode/ aka itself. 
    for nnode in all_nodes:
        neigh_nnodes = list(graph.neighbors(nnode)) # Each node has a list of neighbours
        nnode_degree = len(neigh_nnodes)  # Number neighbours = degree
        if nnode_degree > max_degree: # Max Degree allowed is determined by the Resource state.
            neighbor_con_qubits = {}
            for neigh_nnode in neigh_nnodes: # Looking at the neighbours of a single node
                neighbor_con_qubits[neigh_nnode] = graph[nnode][neigh_nnode]['con_qubits'][neigh_nnode]
                graph.remove_edge(nnode, neigh_nnode) # Storing neighbour information within the nnode
                fusions -= 1 ###?????????????
            for i in range(max_degree - 1): # connect nnode with neighbours as much as possible,
                                            # leaving room to extend, 
                neigh_nnode = neigh_nnodes[0]
                graph.add_edge(nnode, neigh_nnode)
                graph[nnode][neigh_nnode]['con_qubits'] = {}
                graph[nnode][neigh_nnode]['con_qubits'][nnode] = 1
                graph[nnode][neigh_nnode]['con_qubits'][neigh_nnode] = neighbor_con_qubits[neigh_nnode]
                fusions += 1
                neigh_nnodes.remove(neigh_nnode) # Neighbour succesfully reconnected graphically, may 
                                                # remove it from list of nieghbour nodes since it no longer needs to be considered.
            
            pre_node = nodes_size # Storing total no. nodes in the graph intially
            added_nodes.append(nodes_size) # First addition to empty list.
            graph.add_node(nodes_size)
#-#-#-##-#-#-##-#-#-##-#-#-##-#-#-##-#-#-##-#-#-##-#-#-##-#-#-##-#-#-##-#-#-##-#-#-##-#-#-##-#-#-#
            graph.nodes[nodes_size]['phase'] = {} 
            graph.nodes[nodes_size]['phase'][0] = []
            graph.nodes[nodes_size]['parent'] = graph.nodes[nnode]['parent']
#-#-#-##-#-#-##-#-#-##-#-#-##-#-#-##-#-#-##-#-#-##-#-#-##-#-#-##-#-#-##-#-#-##-#-#-##-#-#-##-#-#-#
            graph.add_edge(nnode, nodes_size)
            graph[nnode][nodes_size]['con_qubits'] = {}
            graph[nnode][nodes_size]['con_qubits'][nnode] = 1
            graph[nnode][nodes_size]['con_qubits'][nodes_size] = 0
            fusions += 1
            nodes_size += 1
            show_graph(graph, added_nodes)
            while len(neigh_nnodes): # Whilst there are still neighbours...
                if len(neigh_nnodes) > max_degree: # As long as more neighbours than degree can support
                    for i in range(max_degree - 1):
                        if len(neigh_nnodes) == 0:
                            break
                        neigh_nnode = neigh_nnodes[0] #Takes 1st neighbour and removes from list 
                        neigh_nnodes.remove(neigh_nnode)
                        graph.add_edge(pre_node, neigh_nnode)
                        graph[pre_node][neigh_nnode]['con_qubits'] = {}
                        graph[pre_node][neigh_nnode]['con_qubits'][pre_node] = 1
                        graph[pre_node][neigh_nnode]['con_qubits'][neigh_nnode] = neighbor_con_qubits[neigh_nnode]
                        fusions += 1
                    added_nodes.append(nodes_size)
                    graph.add_node(nodes_size)
#-#-#-##-#-#-##-#-#-##-#-#-##-#-#-##-#-#-##-#-#-##-#-#-##-#-#-##-#-#-##-#-#-##-#-#-##-#-#-##-#-#-#
                    graph.nodes[nodes_size]['phase'] = {}
                    graph.nodes[nodes_size]['phase'][0] = []
                    graph.nodes[nodes_size]['parent'] = graph.nodes[pre_node]['parent']
#-#-#-##-#-#-##-#-#-##-#-#-##-#-#-##-#-#-##-#-#-##-#-#-##-#-#-##-#-#-##-#-#-##-#-#-##-#-#-##-#-#-#
                    graph.add_edge(pre_node, nodes_size)
                    graph[pre_node][nodes_size]['con_qubits'] = {}
                    graph[pre_node][nodes_size]['con_qubits'][pre_node] = 1
                    graph[pre_node][nodes_size]['con_qubits'][nodes_size] = 0
                    fusions += 1
                    pre_node = nodes_size
                    nodes_size += 1
                else:
                    for i in range(max_degree):
                        if len(neigh_nnodes) == 0:
                            break
                        neigh_nnode = neigh_nnodes[0]
                        neigh_nnodes.remove(neigh_nnode)
                        graph.add_edge(pre_node, neigh_nnode)  
                        graph[pre_node][neigh_nnode]['con_qubits'] = {}
                        graph[pre_node][neigh_nnode]['con_qubits'][pre_node] = 1
                        graph[pre_node][neigh_nnode]['con_qubits'][neigh_nnode] = neighbor_con_qubits[neigh_nnode]
                        fusions += 1   
  
    for nnode in graph.nodes(): # Looking at each node in graph
        graph.nodes[nnode]['avail_qubits'] = [] # initialise empty list for every node. 
        for i in range(1, max_degree + 1):
            graph.nodes[nnode]['avail_qubits'].append(i) # initialising connections a node has?

        if len(list(graph.neighbors(nnode))) > max_degree + 1: # Check, ensures each node has neighbours not exceeding max degree limitations 
            print("degree error")

    for edge in graph.edges():
        # Analysing qubit 1 of the edge
        if graph[edge[0]][edge[1]]['con_qubits'][edge[0]] > 0:
            # If connection qubit can replace available qubit, do it
            if graph[edge[0]][edge[1]]['con_qubits'][edge[0]] in graph.nodes[edge[0]]['avail_qubits']:
                graph.nodes[edge[0]]['avail_qubits'].remove(graph[edge[0]][edge[1]]['con_qubits'][edge[0]])
            # If not, New qubit must be added
            else:
                new_qubit = graph.nodes[edge[0]]['avail_qubits'][0]
                graph.nodes[edge[0]]['avail_qubits'].remove(new_qubit)
                graph[edge[0]][edge[1]]['con_qubits'][edge[0]] = new_qubit
        
        # Analysing qubit 2 of the edge
        if graph[edge[0]][edge[1]]['con_qubits'][edge[1]] > 0:
            if graph[edge[0]][edge[1]]['con_qubits'][edge[1]] in graph.nodes[edge[1]]['avail_qubits']:
                graph.nodes[edge[1]]['avail_qubits'].remove(graph[edge[0]][edge[1]]['con_qubits'][edge[1]])
            else:
                new_qubit = graph.nodes[edge[1]]['avail_qubits'][0]
                graph.nodes[edge[1]]['avail_qubits'].remove(new_qubit)
                graph[edge[0]][edge[1]]['con_qubits'][edge[1]] = new_qubit
    
    # rewrite special fusion
    all_nodes = graph.nodes()

    # Storing all nodes ,qubit index, that only have 2 connections
    degree_two_nodes = []
    for gnode in all_nodes:
        if len(list(graph.neighbors(gnode))) == 2:
            degree_two_nodes.append(gnode)   


    ##### PROCESSING ALL THE NODES WITH ONLY 2 DEGREES  
    # This step puts the nodes with only 2 connections onto a path. 
    # It checks if those nodes are connected to other 2 connection nodes. i.e. straight forward to put onto path.
    # It does it starting from 0 then does -1, converging in centre.
    while len(degree_two_nodes) >= 1:
        print(f"Processing 2 degree nodes: {degree_two_nodes}")
        cur_node = degree_two_nodes[0]
        degree_two_nodes.remove(cur_node)
        path = [cur_node] # Initialise a path with node 0 

        # Initialising while loop
        extend_flag = 1
        # Looking at the start and end nodes for extendable routes
        while extend_flag:
            extend_flag = 0 # Set to stop while loop for now.
            neigh_head_nodes = list(graph.neighbors(path[0])) # List the neighbours of the first 2-degree node in list.
            for neigh_node in neigh_head_nodes:
                if neigh_node not in path and neigh_node in degree_two_nodes: # Checks if neighbours can be applicable as extenders. must not already have been pathed before
                    extend_flag = 1 # Allows while loop to resume
                    degree_two_nodes.remove(neigh_node) 
                    path = [neigh_node] + path # The neighbouring node has been added to path. 
                    print(f'Current progress of Head nodes {path}')
                    break 
            neigh_tail_nodes = list(graph.neighbors(path[-1]))
            for neigh_node in neigh_tail_nodes: # List the neighbours of the last 2-degree node in list.
                if neigh_node not in path and neigh_node in degree_two_nodes:
                    extend_flag = 1
                    degree_two_nodes.remove(neigh_node)
                    path.append(neigh_node)
                    print(f'Current progress of Tail nodes {path}')
                    break
        
        # Identifying starting node, confirming pathable neighbours have been pathed      
        neigh_head_nodes = list(graph.neighbors(path[0])) # For example, [1,2,3] would mean are all the neighbours of qubit 0.  Looking at 1. 
        
        print(f'The path to be mapped, {path}')
        print(f'The neighbours of the, {path[0]}, head node {neigh_head_nodes}')
        for neigh_node in neigh_head_nodes: # Looking at qubit index adjacent to pathed node (starting)
            # More specifically looking at neighbours that have not been included in 2 degree analysis
            # Also checking the number of neighbours for THAT neighbour is not 2. 
            if neigh_node not in path and len(list(graph.neighbors(neigh_node))) != 2:
                head_node = neigh_node
                break
        # Identifying end node, confirming pathable neighbours have been pathed
        neigh_tail_nodes = list(graph.neighbors(path[-1]))
        print(f'The neighbours of the, {path[-1]}, tail node {neigh_tail_nodes}')
        for neigh_node in neigh_tail_nodes:
            if neigh_node not in path and len(list(graph.neighbors(neigh_node))) != 2 and neigh_node != head_node:
                tail_node = neigh_node
                break  
        
        # retrieve qubit connection information of top & tail 
        # (since they'll be the only nodes with more than 2 connections)
        # Accessing the attribute 'con_qubits' of the edge between head_node and the first node in path (denoted as path[0]), which contains a dictionary. Within this dictionary, the key corresponding to head_node is used to retrieve a specific qubit index.
        head_con = graph[head_node][path[0]]['con_qubits'][head_node] # Low integer value 1+ 
        tail_con = graph[path[-1]][tail_node]['con_qubits'][tail_node]  
        print(f'Head connectivity {head_con} , {graph[head_node],graph[path[0]]}\nTail connectivity {tail_con}, {graph[path[-1]][tail_node]}')
        print(f'The path: {path}')
        # Analysing head_connectivity (con of head node)
        if head_con: # As long as head_con =/= 0
            head_depth = depths[head_con - 1] - 2  # Depths is a metric from RS. 
            #print(f'The RS depths: {depths}') # The RS depths: [2, 2, 2, 2, 2, 3, 3, 3, 4]
            print(f'Depths: {depths}, Head connectivity: {head_con} ')
            print(f'Head depths: {head_depth}') # Usually 0
            pre_node = head_node  # Storing head_node initial state.
            for i in range(head_depth):
                if len(path) == 0:  # No further nodes in path list to process. 
                    break           # Following is redundant so... Break.   
                graph.remove_edge(pre_node, path[0])
                if pre_node != head_node:
                    if head_con not in graph.nodes[head_node]['phase'].keys():
                        graph.nodes[head_node]['phase'][head_con] = []
                    graph.nodes[head_node]['phase'][head_con] = graph.nodes[head_node]['phase'][head_con] + graph.nodes[pre_node]['phase'][0]
                    graph.remove_node(pre_node)
                    
                pre_node = path[0]
                path.remove(pre_node)

            if len(path): # If exists nodes in Path list
                path_con = graph[pre_node][path[0]]['con_qubits'][path[0]]
                graph.remove_edge(pre_node, path[0])
###################################################################### 
                if pre_node != head_node:
                    print(graph.nodes[head_node]['phase'])
                    print(graph.nodes[head_node]['phase'].keys())
                    if head_con not in graph.nodes[head_node]['phase'].keys():
                        graph.nodes[head_node]['phase'][head_con] = []
                    graph.nodes[head_node]['phase'][head_con] = graph.nodes[head_node]['phase'][head_con] + graph.nodes[pre_node]['phase'][0]
                    graph.remove_node(pre_node)
                    
                graph.add_edge(head_node, path[0])
                graph[head_node][path[0]]['con_qubits'] = {}
                graph[head_node][path[0]]['con_qubits'][head_node] = head_con
                graph[head_node][path[0]]['con_qubits'][path[0]] = path_con 
            else:
                graph.remove_edge(pre_node, tail_node)
######################################################################
                if pre_node != head_node:
                    print(graph.nodes[head_node])
                    print(graph.nodes[head_node]['phase'])
                    print(graph.nodes[head_node]['phase'].keys())
                    if head_con not in graph.nodes[head_node]['phase'].keys():
                        graph.nodes[head_node]['phase'][head_con] = []
                    graph.nodes[head_node]['phase'][head_con] = graph.nodes[head_node]['phase'][head_con] + graph.nodes[pre_node]['phase'][0]
                    graph.remove_node(pre_node)
                    
                graph.add_edge(head_node, tail_node)
                graph[head_node][tail_node]['con_qubits'] = {}
                graph[head_node][tail_node]['con_qubits'][head_node] = head_con
                graph[head_node][tail_node]['con_qubits'][tail_node] = tail_con 
        
        # Analysing tail_connectivity (con of tail node)
        if tail_con:
            tail_depth = depths[tail_con - 1] - 2
            pre_node = tail_node
            for i in range(tail_depth):
                if len(path) == 0:
                    break         
                graph.remove_edge(path[-1], pre_node)
                if pre_node != tail_node:
######################################################################
                    print(graph.nodes[tail_node])
                    print(graph.nodes[tail_node]['phase']) # Returns a dictionary {0: []}
                    print(graph.nodes[tail_node]['phase'].keys()) # Returns key dict_keys([0]) Only 0 key
                    if tail_con not in graph.nodes[tail_node]['phase'].keys(): # Accessing the node labelled tail_node, accessing specific attribute phase, keys suggest the phase is 
                        graph.nodes[tail_node]['phase'][tail_con] = [] 
                    graph.nodes[tail_node]['phase'][tail_con] = graph.nodes[tail_node]['phase'][tail_con] + graph.nodes[pre_node]['phase'][0]

                pre_node = path[-1]
                path.remove(pre_node)
            if len(path):
                path_con = graph[path[-1]][pre_node]['con_qubits'][path[-1]]
                graph.remove_edge(pre_node, path[-1])
                if pre_node != tail_node:
                    if tail_con not in graph.nodes[tail_node]['phase'].keys():
                        graph.nodes[tail_node]['phase'][tail_con] = []
###################################################################### 
#Error area 3 [] [0]
#Error area 3 [] [0]
#Error area 3 [] [-1]
#Error area 3 [] [0]
#Error area 3 [] [1]
#Error area 3 [] [0]Error area 3 [] [1]

                    print(graph.nodes[tail_node]['phase'][tail_con], graph.nodes[pre_node]['phase'][0])
                    graph.nodes[tail_node]['phase'][tail_con] = graph.nodes[tail_node]['phase'][tail_con] + graph.nodes[pre_node]['phase'][0]
                    graph.remove_node(pre_node)

                graph.add_edge(tail_node, path[-1])
                graph[tail_node][path[-1]]['con_qubits'] = {}
                graph[tail_node][path[-1]]['con_qubits'][tail_node] = tail_con
                graph[tail_node][path[-1]]['con_qubits'][path[-1]] = path_con 
            else:
                graph.remove_edge(pre_node, head_node)
                if pre_node != tail_node:
                    if tail_con not in graph.nodes[tail_node]['phase'].keys():
                        graph.nodes[tail_node]['phase'][tail_con] = []
                    graph.nodes[tail_node]['phase'][tail_con] = graph.nodes[tail_node]['phase'][tail_con] + graph.nodes[pre_node]['phase'][0]
                    graph.remove_node(pre_node)
                graph.add_edge(head_node, tail_node)
                graph[head_node][tail_node]['con_qubits'] = {}
                graph[head_node][tail_node]['con_qubits'][head_node] = head_con
                graph[head_node][tail_node]['con_qubits'][tail_node] = tail_con

            print("************************* \nAbove was during 1 while loop")        






    for nnode in graph.nodes():
        graph.nodes[nnode]['avail_qubits_vali'] = []
        for i in range(max_degree + 1):
            graph.nodes[nnode]['avail_qubits_vali'].append(i)
        # print(graph.nodes[nnode]['avail_qubits_vali'])
        
    for edge in graph.edges():
        if graph[edge[0]][edge[1]]['con_qubits'][edge[0]] in graph.nodes[edge[0]]['avail_qubits_vali']:
            graph.nodes[edge[0]]['avail_qubits_vali'].remove(graph[edge[0]][edge[1]]['con_qubits'][edge[0]])
        else:
            print(graph[edge[0]][edge[1]]['con_qubits'][edge[0]])
            print("fusion connected qubits validation error1!")
            return graph

        if graph[edge[0]][edge[1]]['con_qubits'][edge[1]] in graph.nodes[edge[1]]['avail_qubits_vali']:
            graph.nodes[edge[1]]['avail_qubits_vali'].remove(graph[edge[0]][edge[1]]['con_qubits'][edge[1]])
        else:
            print(graph[edge[0]][edge[1]]['con_qubits'][edge[1]])
            print(max_degree, max_length)
            print("fusion connected qubits validation error2!")
            return graph       
    print("fusion connected qubits validation success!")
    show_graph(graph, added_nodes)
    return graph

# rs = generate_state(10)
# nx.draw(rs)
# plt.show()
# depths, max_degree, max_length = get_basic_rs(rs)
# print(depths, max_degree, max_length)