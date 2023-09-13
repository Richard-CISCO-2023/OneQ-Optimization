import networkx as nx
import matplotlib.pyplot as plt
import math

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
    # nx.draw(graph, pos, node_size=10, node_color=colors, arrowsize=20)
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
                # show_graph(graph, added_nodes)
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
                # show_graph(graph, added_nodes)
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
                    neigh_head_nodes = graph.neighbors(path[0])
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
                # show_graph(graph, added_nodes)
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
                # show_graph(graph, added_nodes)
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
                    # show_graph(graph, added_nodes)
        
    return graph, added_nodes


