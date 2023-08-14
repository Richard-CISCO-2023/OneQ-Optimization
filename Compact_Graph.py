import networkx as nx
import matplotlib.pyplot as plt
import heapq
import random
from Generate_Tree import *
from Generate_Cyclic_Graph import *
from collections import deque

##########################################################
#                                                        #
#                     Multi Layers                       #
#                                                        #
##########################################################

# 定义网格大小
GraphN = 3000
NetN = 30
NetM = 30
MaxDegree = 3

# A star search node
class SearchNode:
    def __init__(self, net):
        self.net = net
        self.free_edges = []
        self.free_space = 0
        self.f = 0
        self.g = 0

    def __lt__(self, other):
        return self.f < other.f
    
class SearchNodeAlloca:
    def __init__(self, net):
        self.net = net
        self.last_node = 0
        self.f = 0
        self.g = 0

    def __lt__(self, other):
        return self.f < other.f       

class OneWaySearchNode:
    def __init__(self, net):
        self.net = net
        self.path = []
        self.f = 0

    def __lt__(self, other):
        return self.f > other.f      

def create_graph():
    # graph = generate_cyclic_graph(GraphN)
    graph = create_tree(GraphN)
    return graph

def show_graph(graph):
    # nx.draw_circular(graph, with_labels=True)
    # plt.show()
    # show_graph_tree(graph)
    show_cyclic_graph(graph)
    return

def create_net(alloca_nodes):
    net = nx.Graph()
    for key in alloca_nodes.keys():
        net.add_node(alloca_nodes[key], node_val = key, pos = (alloca_nodes[key] % NetM, alloca_nodes[key] // NetM))

    # 添加节点到网格中
    for i in range(NetN):
        for j in range(NetM):
            if i * NetM + j not in net.nodes():
                # -GraphN - 1 意味着没有分配节点，负数意味着是辅助节点，其绝对值是表示了它的归属性
                net.add_node(i * NetM + j, node_val = -GraphN - 1, pos = (j, i))

    return net

def show_net(pre_graph, net, index, layer_number):
    nodes_pos = nx.get_node_attributes(net, 'pos')
    nodes_color = []
    labels = {}
    for node in net.nodes():
        if node in index:
            nodes_color.append('green')
            labels[node] = str(pre_graph.nodes[net.nodes[node]['node_val']]['layer'])
            continue
        if net.nodes[node]['node_val'] == -GraphN - 1:
            nodes_color.append('gray')
            labels[node] = ""
        elif net.nodes[node]['node_val'] < 0:
            nodes_color.append('pink')
            labels[node] = ""
        else:
            nodes_color.append('blue')
            labels[node] = str(pre_graph.nodes[net.nodes[node]['node_val']]['layer'])
            #print(node, net.nodes[node]['node_val'])
    print(labels)
    plt.figure(figsize=(NetN, NetM))
    nx.draw(net, pos=nodes_pos, labels = labels, node_size=40, node_color=nodes_color, font_size=50, arrowsize=20)
    plt.savefig("layers/layer" + str(layer_number) + ".png")
    # plt.show()
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

def count_pos_take(net, pos):
    index = []

    if pos - NetM >= 0 and net.nodes[pos - NetM]['node_val'] != -GraphN - 1:
        if pos - NetM not in net.neighbors(pos):
            index.append(pos - NetM)

    if pos + NetM <= NetN * NetM - 1 and net.nodes[pos + NetM]['node_val'] != -GraphN - 1:
        if pos + NetM not in net.neighbors(pos):
            index.append(pos + NetM)  
    
    if pos % NetM != 0 and net.nodes[pos - 1]['node_val'] != -GraphN - 1:
        if pos - 1 not in net.neighbors(pos):
            index.append(pos - 1)

    if pos % NetM != NetM - 1 and net.nodes[pos + 1]['node_val'] != -GraphN - 1:
        if pos + 1 not in net.neighbors(pos):
            index.append(pos + 1)
    
    return index

def count_free_space(net, pos):
    neigh_net_nodes = list(net.neighbors(pos))
    count_pos_untake_list = count_pos_untake(net, pos)
    free_space = min(MaxDegree - len(neigh_net_nodes), len(count_pos_untake_list))
    return free_space


def map_and_route(graph, net, alloca_nodes_init, cur_layer):
    cur_layer_nodes = []
    
    for nnode in graph.nodes():
        if graph.nodes[nnode]['layer'] == cur_layer:
            cur_layer_nodes.append(nnode)
    
    for nnode in alloca_nodes_init.keys():
        if nnode not in cur_layer_nodes:
            cur_layer_nodes.append(nnode)
    
    cur_layer_graph = graph.subgraph(cur_layer_nodes)
    subgraphs = list(nx.connected_components(cur_layer_graph))
    unallocated_net_nodes = []
    for nnode in net.nodes():
        if net.nodes[nnode]['node_val'] == -GraphN - 1:
            unallocated_net_nodes.append(nnode)
    # #print(unallocated_net_nodes)
    # for G in subgraphs:
    #     #print(G)
    for G in subgraphs:
        # 起始的时候从空余位置中任意选一个位置开始
        
        # pos = unallocated_net_nodes[random.randint(int((len(unallocated_net_nodes) - 1)/ 4), int((len(unallocated_net_nodes) - 1) * 3/ 4))]
        #pos = unallocated_net_nodes[random.randint(0, len(unallocated_net_nodes) - 1)]
        # pos = 1275
        G_list = list(G)

        is_nodes_in_G_unalloca = 1
        for nnode in G_list:
            if nnode in alloca_nodes_init.keys():
                is_nodes_in_G_unalloca = 0
        if is_nodes_in_G_unalloca:
            pos = unallocated_net_nodes[random.randint(int((len(unallocated_net_nodes) - 1) / 4), int((len(unallocated_net_nodes) - 1) * 3 / 4))]
            net.nodes[pos]['node_val'] = G_list[0]
            unallocated_net_nodes.remove(pos)
            alloca_incomplete_nodes = []
            alloca_incomplete_nodes.append(G_list[0])
            alloca_nodes = {}
            alloca_nodes[G_list[0]] = pos
        else:
            alloca_incomplete_nodes = []
            for nnode in G_list:
                if nnode in alloca_nodes_init.keys():
                    alloca_incomplete_nodes.append(nnode)
            alloca_nodes = alloca_nodes_init.copy()
        
        if len(G_list) == 1:
            continue
        


        # 开始设置路由路线
        while len(alloca_incomplete_nodes):
            #print(alloca_nodes)
            #print(alloca_incomplete_nodes)
            node = alloca_incomplete_nodes[0]

            #print(node)
            
            if node not in graph.nodes():
                alloca_incomplete_nodes.remove(node)
                continue

            # 检测出来当前这个节点不是未分配完全点
            #print('neighbor:')
            #print(len(list(graph.neighbors(node))))
            if len(list(graph.neighbors(node))) == 0:
                G_list.remove(node)
                graph.remove_node(node)
                alloca_incomplete_nodes.remove(node)
                continue


            neigh_graph_nodes_all = list(graph.neighbors(node))
            neigh_graph_nodes = []
            neigh_graph_nodes_alloca = []

            is_neigh_unalloca_node_next_layer = False
            
            for nnode in neigh_graph_nodes_all:
                if nnode not in list(alloca_nodes.keys()):
                    if graph.nodes[nnode]['layer'] == cur_layer:
                        neigh_graph_nodes.append(nnode)
                else:
                    neigh_graph_nodes_alloca.append(nnode)


            neigh_graph_size = len(neigh_graph_nodes)

            # another kind of allocation
            
            search_set = []
            search_node = OneWaySearchNode(net.copy())
            pos = alloca_nodes[node]
            search_node.path.append(pos)
            neigh_net_nodes = list(net.neighbors(pos))
            count_pos_untake_list = count_pos_untake(net, pos)
            free_space = min(MaxDegree - len(neigh_net_nodes), len(count_pos_untake_list))
            search_node.f = free_space
            # print("search unalloca", pos, neigh_graph_size)
            # show_net(search_node.net)
            # print("node pos", node, pos)
            # print("search free_space", free_space, neigh_graph_size)
            heapq.heappush(search_set,search_node)
            search_flag = 0
            error1_flag = 0
            search_index = 0
            while len(search_set):
                if search_index >= 2000:
                    break
                # print("keep searching", search_index)
                search_index += 1 
                search_node = heapq.heappop(search_set)
                if search_node.f >= neigh_graph_size:
                    copy_net  = search_node.net.copy()
                    count_pos_untake_list = count_pos_untake(copy_net, search_node.path[-1])
                    copy_neigh_graph_nodes = neigh_graph_nodes.copy()
                    copy_graph = graph.copy()
                    copy_alloca_nodes = alloca_nodes.copy()
                    copy_alloca_incomplete_nodes = alloca_incomplete_nodes.copy()
                    while len(copy_neigh_graph_nodes) and len(count_pos_untake_list):
                        pos_alloca = count_pos_untake_list[0]
                        count_pos_untake_list.remove(pos_alloca)
                        up_pos = pos_alloca - NetM
                        down_pos = pos_alloca + NetM
                        left_pos = pos_alloca - 1
                        right_pos = pos_alloca + 1
                        # 判别一下pos会不会造成堵死
                        blocked_add_flag = 0
                        if up_pos >= 0 and copy_net.nodes[up_pos]['node_val'] != - GraphN - 1 and len(count_pos_untake(copy_net, up_pos))  <= 2 and copy_net.nodes[up_pos]['node_val'] in copy_alloca_incomplete_nodes:
                            blocked_add_flag = 1

                        if down_pos <= NetM * NetN - 1 and copy_net.nodes[down_pos]['node_val'] != - GraphN - 1 and len(count_pos_untake(copy_net, down_pos)) <= 2 and copy_net.nodes[down_pos]['node_val'] in copy_alloca_incomplete_nodes:
                            blocked_add_flag = 1

                        if left_pos % NetM != NetM - 1 and copy_net.nodes[left_pos]['node_val'] != - GraphN - 1 and len(count_pos_untake(copy_net, left_pos)) <= 2 and copy_net.nodes[left_pos]['node_val'] in copy_alloca_incomplete_nodes:
                            blocked_add_flag = 1

                        if right_pos % NetM != 0 and copy_net.nodes[right_pos]['node_val'] != - GraphN - 1 and len(count_pos_untake(copy_net, right_pos)) <= 2 and copy_net.nodes[right_pos]['node_val'] in copy_alloca_incomplete_nodes:
                            blocked_add_flag = 1
                        
                        if len(list(count_pos_untake(copy_net, pos_alloca))) == 0:
                            if len(list(copy_graph.neighbors(copy_neigh_graph_nodes[0]))):
                                blocked_add_flag = 1
                        
                        # print("blocked_add_flag", blocked_add_flag)
                        if blocked_add_flag == 0:
                            node_alloca = copy_neigh_graph_nodes[0]
                            copy_neigh_graph_nodes.remove(node_alloca)
                            copy_net.nodes[pos_alloca]['node_val'] = node_alloca
                            copy_net.add_edge(search_node.path[-1], pos_alloca)
                            copy_graph.remove_edge(node, node_alloca)
                            copy_alloca_nodes[node_alloca] = pos_alloca
                            #show_net(search_node.net)
                            if len(list(graph.neighbors(node_alloca))):
                                copy_alloca_incomplete_nodes.append(node_alloca)
                            else:
                                copy_graph.remove_node(node_alloca)
                    #show_net(net)
                    rand_mix = random.randint(1,100)
                    if len(copy_neigh_graph_nodes) == 0 and rand_mix >= 32:
                        search_flag = 1
                        net = copy_net
                        neigh_graph_nodes = copy_neigh_graph_nodes
                        graph = copy_graph
                        alloca_nodes = copy_alloca_nodes
                        alloca_incomplete_nodes = copy_alloca_incomplete_nodes
                        # print("hello")
                        break
                    # print("continue")
                
                if search_node.f >= 1:
                    count_pos_untake_list = count_pos_untake(search_node.net, search_node.path[-1])
                    for nnode in count_pos_untake_list:
                        up_nnode = nnode - NetM
                        down_nnode = nnode + NetM
                        left_nnode = nnode - 1
                        right_nnode = nnode + 1
                        # 判别一下nnode会不会造成堵死
                        if up_nnode >= 0 and search_node.net.nodes[up_nnode]['node_val'] != - GraphN - 1 and len(count_pos_untake(search_node.net, up_nnode))  <= 1 and up_nnode in alloca_incomplete_nodes:
                            continue

                        if down_nnode <= NetM * NetN - 1 and search_node.net.nodes[down_nnode]['node_val'] != - GraphN - 1 and len(count_pos_untake(search_node.net, down_nnode)) <= 2 and down_nnode in alloca_incomplete_nodes:
                            continue

                        if left_nnode % NetM != NetM - 1 and search_node.net.nodes[left_nnode]['node_val'] != - GraphN - 1 and len(count_pos_untake(search_node.net, left_nnode)) <= 2 and left_nnode in alloca_incomplete_nodes:
                            continue

                        if right_nnode % NetM != 0 and search_node.net.nodes[right_nnode]['node_val'] != - GraphN - 1 and len(count_pos_untake(search_node.net, right_nnode)) <= 2 and right_nnode in alloca_incomplete_nodes:
                            continue
                        new_node = OneWaySearchNode(search_node.net.copy())
                        new_node.net.add_edge(search_node.path[-1], nnode)
                        new_node.net.nodes[nnode]['node_val'] = - node
                        new_node.path = search_node.path.copy()
                        new_node.path.append(nnode)
                        nn_count_pos_untake_list = count_pos_untake(new_node.net, nnode)
                        new_node.f = min(MaxDegree - 1, len(nn_count_pos_untake_list))
                        # print("len untake pos", len(nn_count_pos_untake_list))
                        # print("new node free space", new_node.f)
                        # show_net(new_node.net)
                        heapq.heappush(search_set, new_node)
            if search_flag == 0:
                # print('error1')
                if search_node.f:
                    net = search_node.net.copy()
                    count_pos_untake_list = count_pos_untake(net, search_node.path[-1])
                    while len(neigh_graph_nodes) and len(count_pos_untake_list):
                        pos_alloca = count_pos_untake_list[0]
                        count_pos_untake_list.remove(pos_alloca)
                        # up_pos = pos_alloca - NetM
                        # down_pos = pos_alloca + NetM
                        # left_pos = pos_alloca - 1
                        # right_pos = pos_alloca + 1
                        # # 判别一下pos会不会造成堵死
                        blocked_add_flag = 0
                        # if up_pos >= 0 and copy_net.nodes[up_pos]['node_val'] != - GraphN - 1 and len(count_pos_untake(copy_net, up_pos))  <= 2 and copy_net.nodes[up_pos]['node_val'] in copy_alloca_incomplete_nodes:
                        #     blocked_add_flag = 1

                        # if down_pos <= NetM * NetN - 1 and copy_net.nodes[down_pos]['node_val'] != - GraphN - 1 and len(count_pos_untake(copy_net, down_pos)) <= 2 and copy_net.nodes[down_pos]['node_val'] in copy_alloca_incomplete_nodes:
                        #     blocked_add_flag = 1

                        # if left_pos % NetM != NetM - 1 and copy_net.nodes[left_pos]['node_val'] != - GraphN - 1 and len(count_pos_untake(copy_net, left_pos)) <= 2 and copy_net.nodes[left_pos]['node_val'] in copy_alloca_incomplete_nodes:
                        #     blocked_add_flag = 1

                        # if right_pos % NetM != 0 and copy_net.nodes[right_pos]['node_val'] != - GraphN - 1 and len(count_pos_untake(copy_net, right_pos)) <= 2 and copy_net.nodes[right_pos]['node_val'] in copy_alloca_incomplete_nodes:
                        #     blocked_add_flag = 1
                        
                        # if len(list(count_pos_untake(copy_net, pos_alloca))) == 0:
                        #     if len(list(copy_graph.neighbors(copy_neigh_graph_nodes[0]))):
                        #         blocked_add_flag = 1
                        
                        # print("blocked_add_flag", blocked_add_flag)
                        if blocked_add_flag == 0:
                            node_alloca = neigh_graph_nodes[0]
                            neigh_graph_nodes.remove(node_alloca)
                            net.nodes[pos_alloca]['node_val'] = node_alloca
                            net.add_edge(search_node.path[-1], pos_alloca)
                            graph.remove_edge(node, node_alloca)
                            alloca_nodes[node_alloca] = pos_alloca
                            #show_net(search_node.net)
                            if len(list(graph.neighbors(node_alloca))):
                                alloca_incomplete_nodes.append(node_alloca)
                            else:
                                graph.remove_node(node_alloca) 
                error1_flag = 1
                index = []
                index.append(pos)
                # show_net(search_node.net, index)
            error2_flag = 0
            while len(neigh_graph_nodes_alloca):
                node_dest = neigh_graph_nodes_alloca[0]
                neigh_graph_nodes_alloca.remove(node_dest)
                pos_src = alloca_nodes[node] 
                pos_dest = alloca_nodes[node_dest]
                # print("search src dest",pos_src, pos_dest)
                node_set = [pos_src, pos_dest]
                for nnode in net.nodes():
                    if net.nodes[nnode]['node_val'] == - GraphN - 1 or net.nodes[nnode]['node_val'] == - node:
                        blocked_add_flag = 0
                        up_nnode = nnode - NetM
                        down_nnode = nnode + NetM
                        left_nnode = nnode - 1
                        right_nnode = nnode + 1
                        # 判别一下nnode会不会造成堵死
                        if up_nnode >= 0 and net.nodes[up_nnode]['node_val'] != - GraphN - 1 and len(count_pos_untake(net, up_nnode))  == 1 and up_nnode in alloca_incomplete_nodes:
                            blocked_add_flag = 1

                        if down_nnode <= NetM * NetN - 1 and net.nodes[down_nnode]['node_val'] != - GraphN - 1 and len(count_pos_untake(net, down_nnode)) == 1 and down_nnode in alloca_incomplete_nodes:
                            blocked_add_flag = 1

                        if left_nnode % NetM != NetM - 1 and net.nodes[left_nnode]['node_val'] != - GraphN - 1 and len(count_pos_untake(net, left_nnode)) == 1 and left_nnode in alloca_incomplete_nodes:
                            blocked_add_flag = 1

                        if right_nnode % NetM != 0 and net.nodes[right_nnode]['node_val'] != - GraphN - 1 and len(count_pos_untake(net, right_nnode)) == 1 and right_nnode in alloca_incomplete_nodes:
                            blocked_add_flag = 1
                        
                        if blocked_add_flag == 0:
                            node_set.append(nnode)
                # 创建新net
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
                # print("search for shortest path")
                has_shortest_path = nx.has_path(new_net, source=pos_src, target=pos_dest)
                # print("shortest path found")
                if has_shortest_path == 0:
                    # show_graph(net)
                    # print("error2")
                    error2_flag = 1
                else:
                    shortest_path = nx.shortest_path(new_net, source=pos_src, target=pos_dest)
                    path_nodes = shortest_path[1:]
                    # print(path_nodes)
                    pre_node = pos_src
                    for nnode in path_nodes:
                        if nnode != pos_dest:
                            net.nodes[nnode]['node_val'] = - node
                        net.add_edge(pre_node, nnode)
                        pre_node = nnode
                    graph.remove_edge(node, node_dest)
                    if len(list(graph.neighbors(node_dest))) == 0:
                        graph.remove_node(node_dest)  
                        alloca_incomplete_nodes.remove(node_dest)   
                    # show_net(net,[pos_src, pos_dest])          

            alloca_incomplete_nodes.remove(node)
        all_nodes = list(graph.nodes()).copy() 
        for nnode in all_nodes:
            if len(list(graph.neighbors(nnode))) == 0:
                graph.remove_node(nnode)  
    return net, graph

def one_layer_map(graph, alloca_nodes, cur_layer):
    # 创建网格
    net = create_net(alloca_nodes)
    index = []
    # show_net(net, index)
    # print(alloca_nodes)
    # 图 -> 网格
    net, unmatched_graph = map_and_route(graph, net, alloca_nodes, cur_layer)
    # print("finish")
    index = []
    # show_net(net, index)
    # show_graph(unmatched_graph)
    return net, unmatched_graph

def compact_graph(graph):
    # # 创建图
    # graph = create_graph()
    # show_graph(graph)
    index = 0
    alloca_nodes = {}
    while len(list(graph.nodes())):
        cur_layer = -1
        for nnode in graph.nodes():
            if nnode not in alloca_nodes.keys():
                if cur_layer == -1:
                    cur_layer = graph.nodes[nnode]['layer']
                else:
                    cur_layer = min(cur_layer, graph.nodes[nnode]['layer'])
        index = index + 1
        pre_graph = graph.copy()
        net, graph  = one_layer_map(graph, alloca_nodes, cur_layer)
        alloca_nodes.clear()
        for nnode in net.nodes():
            if net.nodes[nnode]['node_val'] > 0 and net.nodes[nnode]['node_val'] in graph.nodes():
                alloca_nodes[net.nodes[nnode]['node_val']] = nnode
        # print(alloca_nodes.values())
        show_net(pre_graph, net, alloca_nodes.values(), index)    
    print("number of layers", index)
    # # 创建网格
    # net = create_net()
    # index = []
    # show_net(net, index)

    # # 图 -> 网格
    # net, unmatched_graph = map_and_route(graph, net)
    # print("finish")
    # index = []
    # show_net(net, index)
    # show_graph(unmatched_graph)

# if __name__ == '__main__':
#     compact_graph()
