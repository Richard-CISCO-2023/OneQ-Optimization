import networkx as nx
import matplotlib.pyplot as plt
import heapq
import random
import math

from Generate_State import *

##########################################################
#                                                        #
#           Multi Layers with Dependency                 #
#                                                        #
##########################################################

NetN = 25
NetM = 25
GraphN = 1000000
SearchUpperBound = 20

def create_net(alloca_nodes, graph):
    # print("GraphN,",GraphN)
    net = nx.Graph()
    for key in alloca_nodes.keys():
        net.add_node(alloca_nodes[key], node_val = key, pos = (alloca_nodes[key] % NetM, alloca_nodes[key] // NetM))

    # add nodes to the net
    for i in range(NetN):
        for j in range(NetM):
            if i * NetM + j not in net.nodes():
                # -GraphN - 1 means no node allocated, negative number means its auxiliary identity
                net.add_node(i * NetM + j, node_val = - GraphN - 1, pos = (j, i))
    return net

def save_net(pre_graph, net, alloca_pos, layer_index):
    colors = []
    labels = {}
    for nnode in net.nodes():
        # node already allocated but still in graph, show green color
        if nnode in alloca_pos:
            colors.append('green')
            labels[nnode] = net.nodes[nnode]['node_val']
            continue
        
        # unallocated node, show gray
        if net.nodes[nnode]['node_val'] == - GraphN - 1:
            colors.append('gray')
            labels[nnode] = net.nodes[nnode]['node_val']
        # auxiliary node, show pink
        elif net.nodes[nnode]['node_val'] < 0:
            colors.append('pink')
            labels[nnode] = net.nodes[nnode]['node_val']
        # allocated node with real value, show blue
        else:
            colors.append('blue')
            labels[nnode] = net.nodes[nnode]['node_val']
    
    # get nodes' positions
    pos = nx.get_node_attributes(net, 'pos')

    # show net
    plt.figure(figsize=(NetN, NetM))
    nx.draw(net, pos = pos, node_color = colors, node_size = 40, font_size = 20)
    # save image     
    plt.savefig("layers/layer" + str(layer_index) + ".png")
    plt.show()
    return

def count_pos_untake(net, pos):
    index = []

    if pos - NetM >= 0 and net.nodes[pos - NetM]['node_val'] == -GraphN - 1:
        index.append(pos - NetM)

    if pos + NetM <= NetN * NetM - 1 and net.nodes[pos + NetM]['node_val'] == -GraphN - 1:
        index.append(pos + NetM)  
    
    if pos % NetM != 0 and net.nodes[pos - 1]['node_val'] == -GraphN - 1:
        index.append(pos - 1)

    if pos % NetM != NetM - 1 and net.nodes[pos + 1]['node_val'] == -GraphN - 1:
        index.append(pos + 1)
    
    return index

# used for allocate the unallocated nodes, the path is one way like
class OneWaySearchNode:
    def __init__(self, net, path):
        self.net = net.copy()
        self.path = path.copy()
        self.f = 0
        self.free_space = set()
        for pnode in path:
            for nnode in count_pos_untake(net, pnode):
                self.free_space.add(nnode)
        self.f = len(self.free_space)
    def __lt__(self, other):
        return self.f > other.f      

def find_pre_pos(net, path, pos, MaxDegree):
    if pos - NetM >= 0 and pos - NetM in path and len(list(net.neighbors(pos - NetM))) <= MaxDegree - 1:
        return pos - NetM

    if pos + NetM <= NetN * NetM - 1 and pos + NetM in path and len(list(net.neighbors(pos + NetM))) <= MaxDegree - 1:
        return pos + NetM 
    
    if pos % NetM != 0 and pos - 1 in path and len(list(net.neighbors(pos - 1))) <= MaxDegree - 1:
        return pos - 1

    if pos % NetM != NetM - 1 and pos + 1 in path and len(list(net.neighbors(pos + 1))) <= MaxDegree - 1:
        return pos + 1  
    return -1

def divide_rs(rs):
    line_list = []
    all_nodes = list(rs.nodes()).copy()
    for rnode in all_nodes:
        if len(list(rs.neighbors(rnode))) == 0:
            rs.remove_node(rnode)
    while len(list(rs.nodes())):
        # nx.draw(rs)
        # plt.show()
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
        line_list.append(line)
        all_nodes = list(rs.nodes()).copy()
        for rnode in all_nodes:
            if len(list(rs.neighbors(rnode))) == 0:
                rs.remove_node(rnode)
    bi = 0
    for line in line_list:
        bi += (len(line) + 1) // 3
    return bi

def one_layer_map(graph, dgraph, alloca_nodes, alloca_nodes_cache, max_used_times):
    auxiliary_nodes_used_times = {}
    auxiliary_nodes_used_avail_nodes = {}
    auxiliary_nodes_used_tri = []

    # if not SpeicialFusion:
    #     max_used_times_tri = math.ceil((2 - MaxDegree % 3) / 2) 
    # else:
    #     max_used_times_tri = 0
    MaxDegree = 10
    max_used_times_tri = 0
    
    # print(max_used_times)
    # print(max_used_times_tri)
    initial_alloca_nodes = alloca_nodes.copy()
    # initial net
    net = create_net(alloca_nodes, graph)
    
    failed_nodes = []

    for i in range(3):
        copy_graph_nodes = list(graph.nodes()).copy()
        for gnode in copy_graph_nodes:
            if len(list(graph.neighbors(gnode))) == 0:
                graph.remove_node(gnode)

        if len(list(graph.nodes())) == 0:
            return net, graph, dgraph, alloca_nodes, alloca_nodes_cache

        parent_values = set()
        for gnode in graph.nodes():
            parent_values.add(graph.nodes[gnode]['parent'])
        
        dgraph_nodes = list(dgraph.nodes()).copy()
        nodes_to_be_removed = []
        for dnode in dgraph_nodes:
            if dnode not in parent_values:
                succ_nodes = list(dgraph.successors(dnode)).copy()
                for snode in succ_nodes:
                    dgraph.remove_edge(dnode, snode)
                nodes_to_be_removed.append(dnode)
        for dnode in nodes_to_be_removed:
            dgraph.remove_node(dnode)

        # Determine nodes for the current layer
        cur_layer_nodes = []
        # nodes on the current layer
        for gnode in graph.nodes():
            if (graph.nodes[gnode]['parent'] in dgraph.nodes() and gnode not in alloca_nodes_cache.keys()) or (graph.nodes[gnode]['parent'] in dgraph.nodes() and len(list(dgraph.predecessors(graph.nodes[gnode]['parent']))) == 0 and gnode not in alloca_nodes_cache.keys()) or (gnode in alloca_nodes.keys()):
                cur_layer_nodes.append(gnode)
        
        copy_cur_layer_nodes = cur_layer_nodes.copy()
        for cur_layer_node in copy_cur_layer_nodes:
            if cur_layer_node in failed_nodes:
                cur_layer_nodes.remove(cur_layer_node)
        
        if len(cur_layer_nodes) == 0:
            return net, graph, dgraph, alloca_nodes, alloca_nodes_cache

        # get the subgraph to be allocated
        cur_layer_graph = graph.subgraph(cur_layer_nodes)

        plt.show()

        # get connected subgraph list
        subgraphs = list(nx.connected_components(cur_layer_graph))
        
        failed_nodes = []
        # begin mapping and routing for each subgraph
        for gnodes in subgraphs:
            # update graph after mapping
            all_nodes = list(graph.nodes()).copy() 
            for nnode in all_nodes:
                if len(list(graph.neighbors(nnode))) == 0:
                    graph.remove_node(nnode)  

            gnodes = list(gnodes)
            alloca_incomplete_nodes = []
            # check whether all nodes in this subgraph unallocated
            is_all_gnodes_unalloca = True
            for gnode in gnodes:
                if gnode in alloca_nodes.keys():
                    is_all_gnodes_unalloca = False
                    break
            
            # all nodes in gnods is unallocated
            if is_all_gnodes_unalloca:
                unallocated_net_nodes = []
                for nnode in net.nodes():
                    if net.nodes[nnode]['node_val'] == -GraphN - 1:
                        unallocated_net_nodes.append(nnode)
                if len(unallocated_net_nodes) == 0:
                    return net, graph, dgraph, alloca_nodes, alloca_nodes_cache
                alloca_pos = unallocated_net_nodes[random.randint(int((len(unallocated_net_nodes) - 1) / 4), int((len(unallocated_net_nodes) - 1) * 3 / 4))]
                # allocate the node to a random position
                net.nodes[alloca_pos]['node_val'] = gnodes[0]
                alloca_nodes[gnodes[0]] = alloca_pos
                alloca_incomplete_nodes.append(gnodes[0])
            else:
                for gnode in gnodes:
                    if gnode in alloca_nodes.keys():
                        alloca_incomplete_nodes.append(gnode)

            if len(gnodes) == 1:
                if len(list(graph.neighbors(gnodes[0]))) and len(list(net.neighbors(alloca_nodes[gnodes[0]]))) == 0:
                    alloca_node = gnodes[0]
                    alloca_pos = alloca_nodes[alloca_node]
                    net.nodes[alloca_nodes[alloca_node]]['node_val'] = - GraphN - 1
                    # if alloca_node in cur_layer_nodes:
                        # failed_nodes.append(alloca_node)                
                    del alloca_nodes[alloca_node]
                    if alloca_node in initial_alloca_nodes.keys():
                        alloca_nodes_cache[alloca_node] = alloca_pos
                continue
            
            # diffusion from allocated incomplete nodes
            while len(alloca_incomplete_nodes):
                # choose one allocated incomplete_node to diffuse
                alloca_node = alloca_incomplete_nodes[0]

                # make sure that it is still in the graph
                if alloca_node not in graph.nodes():
                    alloca_incomplete_nodes.remove(alloca_node)
                    continue          

                # check again whether it is incomplete
                if len(list(graph.neighbors(alloca_node))) == 0:
                    graph.remove_node(alloca_node)
                    alloca_incomplete_nodes.remove(alloca_node)
                    continue           
                
                # divide the neighbor nodes into allocated list and unallocated list
                neigh_graph_nodes_all = list(graph.neighbors(alloca_node))
                neigh_graph_nodes_alloca = []
                neigh_graph_nodes_unalloca = []
                neigh_graph_nodes_unalloca_with_one = []
                begin_qubit = set()

                for gnode in neigh_graph_nodes_all:
                    if gnode not in list(alloca_nodes.keys()):
                        if gnode in cur_layer_nodes:
                            if graph[alloca_node][gnode]['con_qubits'][alloca_node] == 0 or graph[alloca_node][gnode]['con_qubits'][alloca_node] == MaxDegree - 1:
                                neigh_graph_nodes_unalloca.append(gnode)
                                begin_qubit.add(graph[alloca_node][gnode]['con_qubits'][alloca_node])
                            else:
                                neigh_graph_nodes_unalloca_with_one.append(gnode)
                    else:
                        if gnode in cur_layer_nodes:
                            neigh_graph_nodes_alloca.append(gnode)                

                # allocate the unallocated neighbor nodes
                neigh_graph_nodes_unalloca_size = len(neigh_graph_nodes_unalloca)

                search_set = []
                search_node = OneWaySearchNode(net, [alloca_nodes[alloca_node]])
                heapq.heappush(search_set, search_node)
                tri_flag = 0
                search_index = 0
                while len(search_set):
                    # reach the search times' upper bound
                    if search_index > SearchUpperBound:
                        break

                    search_index += 1
                    search_node = heapq.heappop(search_set)
                    
                    # find a available solution
                    if search_node.f >= neigh_graph_nodes_unalloca_size:
                        break

                    # keep searching
                    if search_node.f >= 1:
                        search_node_net = search_node.net
                        search_node_path = search_node.path
                        # if MaxDegree <= 4:
                        count_pos_untake_list = count_pos_untake(search_node_net, search_node_path[-1])
                        # else:
                        #     count_pos_untake_list = []

                        #     if search_node_path[-1] - NetM >= 0 and search_node_net.nodes[search_node_path[-1] - NetM]['node_val'] < 0:
                        #         count_pos_untake_list.append(search_node_path[-1] - NetM)

                        #     if search_node_path[-1] + NetM <= NetN * NetM - 1 and search_node_net.nodes[search_node_path[-1] + NetM]['node_val'] < 0:
                        #         count_pos_untake_list.append(search_node_path[-1] + NetM)  
                            
                        #     if search_node_path[-1] % NetM != 0 and search_node_net.nodes[search_node_path[-1] - 1]['node_val'] < 0:
                        #         count_pos_untake_list.append(search_node_path[-1] - 1)

                        #     if search_node_path[-1] % NetM != NetM - 1 and search_node_net.nodes[search_node_path[-1] + 1]['node_val'] < 0:
                        #         count_pos_untake_list.append(search_node_path[-1] + 1)
                        for untake_pos in count_pos_untake_list:
                            up_pos = untake_pos - NetM
                            down_pos = untake_pos + NetM
                            left_pos = untake_pos - 1
                            right_pos = untake_pos + 1

                            # check whether the path will lead to blockness
                            if up_pos >= 0 and search_node_net.nodes[up_pos]['node_val'] != - GraphN - 1 and len(count_pos_untake(search_node_net, up_pos))  <= 1 and up_pos in alloca_incomplete_nodes:
                                continue

                            if down_pos <= NetM * NetN - 1 and search_node_net.nodes[down_pos]['node_val'] != - GraphN - 1 and len(count_pos_untake(search_node_net, down_pos)) <= 2 and down_pos in alloca_incomplete_nodes:
                                continue

                            if left_pos % NetM != NetM - 1 and search_node_net.nodes[left_pos]['node_val'] != - GraphN - 1 and len(count_pos_untake(search_node_net, left_pos)) <= 2 and left_pos in alloca_incomplete_nodes:
                                continue

                            if right_pos % NetM != 0 and search_node_net.nodes[right_pos]['node_val'] != - GraphN - 1 and len(count_pos_untake(search_node_net, right_pos)) <= 2 and right_pos in alloca_incomplete_nodes:
                                continue
                            new_node_net = search_node_net.copy()
                            new_node_net.add_edge(search_node_path[-1], untake_pos)

                            # if tri_flag:
                            #     auxiliary_nodes_used_tri.append(untake_pos)
                            #     auxiliary_nodes_used_times[untake_pos] = max_used_times
                            #     auxiliary_nodes_used_avail_nodes[untake_pos] = all_qubits.copy()
                            #     new_node_net[search_node_path[-1]][untake_pos]['con_qubits'] = []
                            #     if search_node_path[-1] != search_node_path[0]:
                            #         new_node_net[search_node_path[-1]][untake_pos]['con_qubits'].append({search_node_path[-1]: MaxDegree - 1, untake_pos: MaxDegree - 2})
                            #         if MaxDegree - 2 in auxiliary_nodes_used_avail_nodes[untake_pos]:
                            #             auxiliary_nodes_used_avail_nodes[untake_pos].remove(MaxDegree - 2)
                            #         else:
                            #             print("mapping error1")
                            #         if MaxDegree - 1 in auxiliary_nodes_used_avail_nodes[search_node_path[-1]]:
                            #             auxiliary_nodes_used_avail_nodes[search_node_path[-1]].remove(MaxDegree - 1)
                            #         else:
                            #             print("mapping error2")                                    
                            new_node_net.nodes[untake_pos]['node_val'] = - alloca_node
                            new_node_path = search_node_path.copy()
                            new_node_path.append(untake_pos)
                            new_node = OneWaySearchNode(new_node_net, new_node_path)
                            heapq.heappush(search_set, new_node)
                
                if search_node.f:
                    if len(search_node.path) == 1:
                        neigh_graph_nodes_unalloca = neigh_graph_nodes_unalloca + neigh_graph_nodes_unalloca_with_one
                    net = search_node.net
                    count_pos_untake_list = list(search_node.free_space)
                    # allocate the nodes
                    pre_nodes = []
                    first_time_flag = 1
                    index = 0
                    if tri_flag:
                        pre_node = search_node.path[0]
                        for untake_pos in search_node.path[1:]:
                            auxiliary_nodes_used_tri.append(untake_pos)
                            auxiliary_nodes_used_times[untake_pos] = max_used_times
                            net[pre_node][untake_pos]['con_qubits'] = []
                            if pre_node != search_node_path[0]:
                                net[pre_node][untake_pos]['con_qubits'].append({pre_node: MaxDegree - 1, untake_pos: MaxDegree - 2})
                                # if MaxDegree - 2 in auxiliary_nodes_used_avail_nodes[untake_pos]:
                                #     auxiliary_nodes_used_avail_nodes[untake_pos].remove(MaxDegree - 2)
                                # else:
                                #     print("mapping error1")
                                # if MaxDegree - 1 in auxiliary_nodes_used_avail_nodes[pre_node]:
                                #     auxiliary_nodes_used_avail_nodes[pre_node].remove(MaxDegree - 1)
                                # else:
                                #     print("mapping error2")      
                            pre_node = untake_pos    
                    while len(count_pos_untake_list) and len(neigh_graph_nodes_unalloca):
                        untake_pos = count_pos_untake_list[0]
                        count_pos_untake_list.remove(untake_pos)
                        unalloca_node = neigh_graph_nodes_unalloca[0]
                        neigh_graph_nodes_unalloca.remove(unalloca_node)
                        net.nodes[untake_pos]['node_val'] = unalloca_node
                        pre_pos = find_pre_pos(net, search_node.path, untake_pos, MaxDegree)
                        if pre_pos == -1:
                            neigh_graph_nodes_unalloca.append(unalloca_node)
                            continue
                        index += 1
                        if tri_flag and first_time_flag and len(search_node.path) > 1:
                            net[search_node.path[0]][search_node.path[1]]['con_qubits'].append({search_node.path[0]: graph[alloca_node][unalloca_node]['con_qubits'][alloca_node], search_node.path[1]: MaxDegree - 2})
                            # if MaxDegree - 2 in auxiliary_nodes_used_avail_nodes[search_node.path[1]]:
                            #     auxiliary_nodes_used_avail_nodes[search_node.path[1]].remove(MaxDegree - 2)
                            # else:
                            #     print("mapping error3")       
                            first_time_flag = 0
                        net.add_edge(pre_pos, untake_pos)
                        # print(max_used_times)
                        # print("index", index)
                        if not tri_flag:
                            if index <= max_used_times:
                                pre_pnode = search_node.path[0]
                                for pnode in search_node.path[1: search_node.path.index(pre_pos) + 1]:
                                    if pnode in auxiliary_nodes_used_times.keys():
                                        auxiliary_nodes_used_times[pnode] -= 1
                                    else:
                                        auxiliary_nodes_used_times[pnode] = max_used_times - 1
                                    
                                    if 'con_qubits' not in net[pre_pnode][pnode].keys():
                                        net[pre_pnode][pnode]['con_qubits'] = []
                                    if pre_pnode == search_node.path[0]:
                                        net[pre_pnode][pnode]['con_qubits'].append({pre_pnode: graph[alloca_node][unalloca_node]['con_qubits'][alloca_node], pnode: 3 * auxiliary_nodes_used_times[pnode]})
                                        # if 3 * auxiliary_nodes_used_times[pnode] in auxiliary_nodes_used_avail_nodes[pnode]:
                                        #     auxiliary_nodes_used_avail_nodes[pnode].remove(3 * auxiliary_nodes_used_times[pnode])
                                        # else:
                                        #     print("mapping error4")  
                                    else:
                                        net[pre_pnode][pnode]['con_qubits'].append({pre_pnode: 1 + 3 * auxiliary_nodes_used_times[pre_pnode], pnode: 3 * auxiliary_nodes_used_times[pnode]})
                                        # if 3 * auxiliary_nodes_used_times[pnode] in auxiliary_nodes_used_avail_nodes[pnode]:
                                        #     auxiliary_nodes_used_avail_nodes[pnode].remove(3 * auxiliary_nodes_used_times[pnode])
                                        # else:
                                        #     print("mapping error5")  
                                        # if 1 + 3 * auxiliary_nodes_used_times[pre_pnode] in auxiliary_nodes_used_avail_nodes[pre_pnode]:
                                        #     auxiliary_nodes_used_avail_nodes[pre_pnode].remove(1 + 3 * auxiliary_nodes_used_times[pre_pnode])
                                        # else:
                                        #     print("mapping error6")  
                                    pre_pnode = pnode

                                net[pre_pos][untake_pos]['con_qubits'] = []
                                if pre_pos != alloca_nodes[alloca_node]:
                                    net[pre_pos][untake_pos]['con_qubits'].append({pre_pnode: 1 + 3 * auxiliary_nodes_used_times[pre_pnode], untake_pos: graph[alloca_node][unalloca_node]['con_qubits'][unalloca_node]})
                                    # if 1 + 3 * auxiliary_nodes_used_times[pre_pnode] in auxiliary_nodes_used_avail_nodes[pre_pnode]:
                                    #     auxiliary_nodes_used_avail_nodes[pre_pnode].remove(1 + 3 * auxiliary_nodes_used_times[pre_pnode])
                                    # else:
                                    #     print("mapping error7")  
                                else:
                                    net[pre_pos][untake_pos]['con_qubits'].append({pre_pnode: graph[alloca_node][unalloca_node]['con_qubits'][alloca_node], untake_pos: graph[alloca_node][unalloca_node]['con_qubits'][unalloca_node]})
                        #     else:
                        #         print("use tri to support bi")
                        #         pre_pnode = search_node.path[0]
                        #         for pnode in search_node.path[1: search_node.path.index(pre_pos) + 1]:                                
                        #             auxiliary_nodes_used_tri.append(pnode)
                        #             if 'con_qubits' not in net[pre_pnode][pnode].keys():
                        #                 net[pre_pnode][pnode]['con_qubits'] = []
                        #             if pre_pnode == search_node.path[0]:
                        #                 net[pre_pnode][pnode]['con_qubits'].append({pre_pnode: graph[alloca_node][unalloca_node]['con_qubits'][alloca_node], pnode: MaxDegree - 2})
                        #                 # if MaxDegree - 2 in auxiliary_nodes_used_avail_nodes[pnode]:
                        #                 #     auxiliary_nodes_used_avail_nodes[pnode].remove(MaxDegree - 2)
                        #                 # else:
                        #                 #     print("mapping error8")  
                        #             else:
                        #                 net[pre_pnode][pnode]['con_qubits'].append({pre_pnode: MaxDegree - 1, pnode: MaxDegree - 2})
                        #                 # if MaxDegree - 2 in auxiliary_nodes_used_avail_nodes[pnode]:
                        #                 #     auxiliary_nodes_used_avail_nodes[pnode].remove(MaxDegree - 2)
                        #                 # else:
                        #                 #     print("mapping error9")  
                        #                 # if MaxDegree - 1 in auxiliary_nodes_used_avail_nodes[pre_pnode]:
                        #                 #     auxiliary_nodes_used_avail_nodes[pre_pnode].remove(MaxDegree - 1)
                        #                 # else:
                        #                 #     print("mapping error10")   
                        #             pre_pnode = pnode        
                        #         net[pre_pos][untake_pos]['con_qubits'] = []
                        #         if pre_pos != alloca_nodes[alloca_node]:
                        #             net[pre_pos][untake_pos]['con_qubits'].append({pre_pnode: MaxDegree - 1, untake_pos: graph[alloca_node][unalloca_node]['con_qubits'][unalloca_node]})
                        #             # if MaxDegree - 1 in auxiliary_nodes_used_avail_nodes[pre_pnode]:
                        #             #     auxiliary_nodes_used_avail_nodes[pre_pnode].remove(MaxDegree - 1)
                        #             # else:
                        #             #     print("mapping error11")                                   
                        #         else:
                        #             net[pre_pos][untake_pos]['con_qubits'].append({pre_pnode: graph[alloca_node][unalloca_node]['con_qubits'][alloca_node], untake_pos: graph[alloca_node][unalloca_node]['con_qubits'][unalloca_node]})                           
                        else:
                            net[pre_pos][untake_pos]['con_qubits'] = []
                            if pre_pos != alloca_nodes[alloca_node]:
                                if pre_pos not in pre_nodes:
                                    dict_add = {} 
                                    dict_add[pre_pos] = MaxDegree - 3
                                    dict_add[untake_pos] = graph[alloca_node][unalloca_node]['con_qubits'][unalloca_node]
                                    net[pre_pos][untake_pos]['con_qubits'].append(dict_add)
                                    # if MaxDegree - 3 in auxiliary_nodes_used_avail_nodes[pre_pos]:
                                    #     auxiliary_nodes_used_avail_nodes[pre_pos].remove(MaxDegree - 3)
                                    # else:
                                    #     print("mapping error12")                                       
                                    pre_nodes.append(pre_pos)
                                    # print(1, pre_pos)
                                else:
                                    net[pre_pos][untake_pos]['con_qubits'].append({pre_pos: MaxDegree - 1, untake_pos: graph[alloca_node][unalloca_node]['con_qubits'][unalloca_node]})
                                    # if MaxDegree - 1 in auxiliary_nodes_used_avail_nodes[pre_pos]:
                                    #     auxiliary_nodes_used_avail_nodes[pre_pos].remove(MaxDegree - 1)
                                    # else:
                                    #     print("mapping error26")    
                                    # print(2, pre_pos)
                            else:
                                net[pre_pos][untake_pos]['con_qubits'].append({pre_pos: graph[alloca_node][unalloca_node]['con_qubits'][alloca_node], untake_pos: graph[alloca_node][unalloca_node]['con_qubits'][unalloca_node]})
                        alloca_nodes[unalloca_node] = untake_pos
                        graph.remove_edge(alloca_node, unalloca_node)
                        if len(list(graph.neighbors(unalloca_node))):
                            alloca_incomplete_nodes.append(unalloca_node)
                        else:
                            graph.remove_node(unalloca_node)

                # search path to node allocated
                while len(neigh_graph_nodes_alloca):
                    node_dest = neigh_graph_nodes_alloca[0]
                    neigh_graph_nodes_alloca.remove(node_dest)
                    src_pos = alloca_nodes[alloca_node]
                    dest_pos = alloca_nodes[node_dest]

                    # create new net to use the shortest path function
                    node_set = [src_pos, dest_pos]
                    for nnode in net.nodes():
                        if max_used_times_tri == 0:
                            if (net.nodes[nnode]['node_val'] == - GraphN - 1) or (nnode in auxiliary_nodes_used_times.keys() and auxiliary_nodes_used_times[nnode] > 0):
                                node_set.append(nnode)
                        else:
                            if (net.nodes[nnode]['node_val'] == - GraphN - 1) or (nnode in auxiliary_nodes_used_times.keys() and auxiliary_nodes_used_times[nnode] > 0) or (nnode in auxiliary_nodes_used_times.keys() and nnode not in auxiliary_nodes_used_tri):
                                node_set.append(nnode)                            
                    new_net = nx.Graph()
                    for nnode in node_set:
                        new_net.add_node(nnode)
                    
                    for nnode in node_set:
                        up_nnode = nnode - NetM
                        left_nnode = nnode - 1
                        if up_nnode in node_set and up_nnode >= 0:
                            new_net.add_edge(nnode, up_nnode)
                        if left_nnode in node_set and left_nnode % NetM != NetM - 1:
                            new_net.add_edge(nnode, left_nnode)   

                    # to make sure that there exists shortest path
                    has_shortest_path = nx.has_path(new_net, source=src_pos, target=dest_pos)
                    if has_shortest_path:
                        shortest_path = nx.shortest_path(new_net, source=src_pos, target=dest_pos)
                        path_nodes = shortest_path[1:]
                        pre_node = src_pos
                        pre_node_kind = 0
                        for nnode in path_nodes:
                            net.add_edge(pre_node, nnode)
                            if 'con_qubits' not in net[pre_node][nnode].keys():
                                net[pre_node][nnode]['con_qubits'] = []
                            # if net.nodes[nnode]['node_val'] == - GraphN - 1 or (nnode in auxiliary_nodes_used_times.keys() and auxiliary_nodes_used_times[nnode] > 0):
                            #     print("true")
                            # elif nnode == dest_pos:
                            #     print("false1")
                            # elif nnode == src_pos:
                            #     print("false2")
                            # else:
                            #     print("false3")
                            # if nnode in node_set:
                            #     print("true node")
                            # else:
                            #     print("false node")
                            if nnode == dest_pos:
                                if pre_node == src_pos:
                                    net[pre_node][nnode]['con_qubits'].append({pre_node: graph[alloca_node][node_dest]['con_qubits'][alloca_node], nnode: graph[alloca_node][node_dest]['con_qubits'][node_dest]})
                                else:
                                    if pre_node_kind == 1:
                                        net[pre_node][nnode]['con_qubits'].append({pre_node: MaxDegree - 1, nnode: graph[alloca_node][node_dest]['con_qubits'][node_dest]})
                                        # if MaxDegree - 1 in auxiliary_nodes_used_avail_nodes[pre_node]:
                                        #     auxiliary_nodes_used_avail_nodes[pre_node].remove(MaxDegree - 1)
                                        # else:
                                        #     print("mapping error14")  
                                    else:
                                        net[pre_node][nnode]['con_qubits'].append({pre_node: 1 + 3 * auxiliary_nodes_used_times[pre_node], nnode: graph[alloca_node][node_dest]['con_qubits'][node_dest]})
                                        # if 1 + 3 * auxiliary_nodes_used_times[pre_node] in auxiliary_nodes_used_avail_nodes[pre_node]:
                                        #     auxiliary_nodes_used_avail_nodes[pre_node].remove(1 + 3 * auxiliary_nodes_used_times[pre_node])
                                        # else:
                                        #     print("mapping error15")  
                            elif nnode in auxiliary_nodes_used_times.keys() and auxiliary_nodes_used_times[nnode] == 0:
                                auxiliary_nodes_used_tri.append(nnode)
                                if pre_node == src_pos:
                                    net[pre_node][nnode]['con_qubits'].append({pre_node: graph[alloca_node][node_dest]['con_qubits'][alloca_node], nnode: MaxDegree - 2})
                                    # if MaxDegree - 2 in auxiliary_nodes_used_avail_nodes[nnode]:
                                    #     auxiliary_nodes_used_avail_nodes[nnode].remove(MaxDegree - 2)
                                    # else:
                                    #     print("mapping error16")  
                                else:
                                    if pre_node_kind == 1:
                                        net[pre_node][nnode]['con_qubits'].append({pre_node: MaxDegree - 1, nnode: MaxDegree - 2})
                                        # if MaxDegree - 2 in auxiliary_nodes_used_avail_nodes[nnode]:
                                        #     auxiliary_nodes_used_avail_nodes[nnode].remove(MaxDegree - 2)
                                        # else:
                                        #     print("mapping error17")
                                        # if MaxDegree - 1 in auxiliary_nodes_used_avail_nodes[pre_node]:
                                        #     auxiliary_nodes_used_avail_nodes[pre_node].remove(MaxDegree - 1)
                                        # else:
                                        #     print("mapping error18")                                            
                                    else:
                                        net[pre_node][nnode]['con_qubits'].append({pre_node: 1 + 3 * auxiliary_nodes_used_times[pre_node], nnode: MaxDegree - 2})
                                        # if MaxDegree - 2 in auxiliary_nodes_used_avail_nodes[nnode]:
                                        #     auxiliary_nodes_used_avail_nodes[nnode].remove(MaxDegree - 2)
                                        # else:
                                        #     print("mapping error19")
                                        # if 1 + 3 * auxiliary_nodes_used_times[pre_node] in auxiliary_nodes_used_avail_nodes[pre_node]:
                                        #     auxiliary_nodes_used_avail_nodes[pre_node].remove(1 + 3 * auxiliary_nodes_used_times[pre_node])
                                        # else:
                                        #     print("mapping error20")  
                                pre_node_kind = 1
                            else:
                                if net.nodes[nnode]['node_val'] == - GraphN - 1:
                                    auxiliary_nodes_used_times[nnode] = max_used_times - 1
                                else:
                                    auxiliary_nodes_used_times[nnode] -= 1
                                if pre_node == src_pos:
                                    net[pre_node][nnode]['con_qubits'].append({pre_node: graph[alloca_node][node_dest]['con_qubits'][alloca_node], nnode: 3 * auxiliary_nodes_used_times[nnode]})
                                    # if  3 * auxiliary_nodes_used_times[nnode] in auxiliary_nodes_used_avail_nodes[nnode]:
                                    #     auxiliary_nodes_used_avail_nodes[nnode].remove( 3 * auxiliary_nodes_used_times[nnode])
                                    # else:
                                    #     print("mapping error21")
                                else:
                                    if pre_node_kind == 1:
                                        net[pre_node][nnode]['con_qubits'].append({pre_node: MaxDegree - 1, nnode: 3 * auxiliary_nodes_used_times[nnode]})
                                        # if MaxDegree - 1 in auxiliary_nodes_used_avail_nodes[pre_node]:
                                        #     auxiliary_nodes_used_avail_nodes[pre_node].remove(MaxDegree - 1)
                                        # else:
                                        #     print("mapping error22")   
                                        # if  3 * auxiliary_nodes_used_times[nnode] in auxiliary_nodes_used_avail_nodes[nnode]:
                                        #     auxiliary_nodes_used_avail_nodes[nnode].remove( 3 * auxiliary_nodes_used_times[nnode])
                                        # else:
                                        #     print("mapping error23")
                                    else:
                                        net[pre_node][nnode]['con_qubits'].append({pre_node: 1 + 3 * auxiliary_nodes_used_times[pre_node], nnode: 3 * auxiliary_nodes_used_times[nnode]})
                                        # if  3 * auxiliary_nodes_used_times[nnode] in auxiliary_nodes_used_avail_nodes[nnode]:
                                        #     auxiliary_nodes_used_avail_nodes[nnode].remove( 3 * auxiliary_nodes_used_times[nnode])
                                        # else:
                                        #     print("mapping error24")
                                        # if 1 + 3 * auxiliary_nodes_used_times[pre_node] in auxiliary_nodes_used_avail_nodes[pre_node]:
                                        #     auxiliary_nodes_used_avail_nodes[pre_node].remove(1 + 3 * auxiliary_nodes_used_times[pre_node])
                                        # else:
                                        #     print("mapping error25")  
                                pre_node_kind = 0
                            if nnode != dest_pos:
                                net.nodes[nnode]['node_val'] = - alloca_node
                            # if pre_node == src_pos:
                            #     net[pre_node][nnode]['con_qubits'][pre_node] = graph[alloca_node][node_dest]['con_qubits'][alloca_node]
                            # else:
                            #     net[pre_node][nnode]['con_qubits'][pre_node] = 0
                            # if nnode == dest_pos:
                            #     net[pre_node][nnode]['con_qubits'][nnode] = graph[alloca_node][node_dest]['con_qubits'][node_dest]
                            # else:
                            #     net[pre_node][nnode]['con_qubits'][nnode] = 0
                            pre_node = nnode
                        graph.remove_edge(alloca_node, node_dest)
                        if len(list(graph.neighbors(node_dest))) == 0:
                            graph.remove_node(node_dest)  
                            if node_dest in alloca_incomplete_nodes:
                                alloca_incomplete_nodes.remove(node_dest) 
                
                alloca_incomplete_nodes.remove(alloca_node)
                alloca_pos = alloca_nodes[alloca_node]
                if len(list(net.neighbors(alloca_pos))) == 0:
                    if len(list(graph.neighbors(alloca_node))):
                        net.nodes[alloca_pos]['node_val'] = - GraphN - 1
                        if alloca_node in cur_layer_nodes:
                            cur_layer_nodes.remove(alloca_node)
                        
                        # if alloca_node not in alloca_nodes_cache.keys():
                        #     # print("hello")
                        #     alloca_nodes_cache[alloca_node] = alloca_nodes[alloca_node]
                        del alloca_nodes[alloca_node]
                        if alloca_node in initial_alloca_nodes.keys():
                            alloca_nodes_cache[alloca_node] = alloca_pos

                        failed_nodes.append(alloca_node)
                        # update graph after mapping
            all_nodes = list(graph.nodes()).copy() 
            for nnode in all_nodes:
                if len(list(graph.neighbors(nnode))) == 0:
                    graph.remove_node(nnode)  
    return net, graph, dgraph, alloca_nodes, alloca_nodes_cache



def compact_graph_dynamic_general(fgraph, dgraph, rs):
    max_used_times = divide_rs(rs)
    # get fgraph information
    graph = fgraph.copy()
    GraphN = len(list(graph.nodes()))
    # collect mapping nets
    net_list = []

    # identify the mapping layer number
    layer_index = 0
    
    alloca_nodes_cache = {}
    alloca_nodes = {}
    pre_graph_nodes = len(list(graph.nodes()))
    # map and route
    while len(list(graph.nodes())):
        exit_flag = 1
        for edge in graph.edges():
            if edge[0] in alloca_nodes_cache.keys() and edge[1] in alloca_nodes_cache.keys() and alloca_nodes_cache[edge[0]] == alloca_nodes_cache[edge[1]]:
                exit_flag = exit_flag
            else:
                exit_flag = 0
                break
        if exit_flag == 1:
            break
        
        # reserve pre graph to show the mapping net
        pre_graph = graph.copy()

        # clear alloca_nodes
        alloca_nodes.clear()
        index = 0
        keys = list(alloca_nodes_cache.keys())
        while len(keys):
            if index >= 2 * NetM * NetN // 3:
                break
            key = keys[0]
            keys.remove(key)
            if alloca_nodes_cache[key] not in alloca_nodes.values():
                alloca_nodes[key] = alloca_nodes_cache[key]
                del alloca_nodes_cache[key]
                index += 1
            else:
                continue
            
            for kkey in keys:
                if graph.has_edge(key, kkey) and alloca_nodes_cache[kkey] not in alloca_nodes.values():
                    alloca_nodes[kkey] = alloca_nodes_cache[kkey]
                    del alloca_nodes_cache[kkey]  
                    keys.remove(kkey)
                    index += 1                  

        # map and route current layer nodes 
        net, graph, dgraph, alloca_nodes, alloca_nodes_cache = one_layer_map(graph, dgraph, alloca_nodes, alloca_nodes_cache, max_used_times)  
        for gnode in graph.nodes():
            if len(list(graph.neighbors(gnode))) == 0:
                graph.remove_node(gnode)

        # get the alloca nodes set  
        for nnode in net.nodes():
            if net.nodes[nnode]['node_val'] > 0 and net.nodes[nnode]['node_val'] in graph.nodes():
                alloca_nodes_cache[net.nodes[nnode]['node_val']] = nnode

        # delete complete nodes
        for gnode in alloca_nodes_cache.keys():
            if len(list(graph.neighbors(gnode))) == 0:
                del alloca_nodes_cache[gnode]

        net_list.append(net)
        alloca_values = []
        for nnode in net.nodes():
            if net.nodes[nnode]['node_val'] > 0:
                if net.nodes[nnode]['node_val'] in graph.nodes():
                    alloca_values.append(nnode)
        # show the mapping net and save it
        # save_net(pre_graph, net, alloca_values, layer_index)

        layer_index += 1  
        print(len(list(graph.nodes())))
        if len(list(graph.nodes())) == pre_graph_nodes:
            for nnode in graph.nodes():
                if nnode in alloca_nodes_cache.keys():
                    print(nnode, alloca_nodes_cache[nnode])
            print(graph.edges())
            nx.draw(dgraph)
            nx.draw(graph)
            break
        pre_graph_nodes = len(list(graph.nodes()))

    print(GraphN, "nodes")
    print(layer_index, "layers") 
    return net_list
