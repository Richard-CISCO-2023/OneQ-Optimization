import networkx as nx
import matplotlib.pyplot as plt
from Compact_Graph import *

def validate(net_list, fgraph):
    print("begin to validate!")
    alloca_nodes_cache = {}
    GraphN = len(list(fgraph.nodes()))
    net_index = 0
    for net in net_list:
        
        for nnode in net.nodes():
            # has been allocated actual nodes
            # print(alloca_nodes_cache)
            if net.nodes[nnode]['node_val'] > 0:
                gnode = net.nodes[nnode]['node_val']
                if gnode in alloca_nodes_cache.keys():
                    if nnode != alloca_nodes_cache[gnode]:
                        print("same node different 2D position")
                        exit()

                adj_list = [nnode]
                while len(adj_list):
                    new_adj_list = []
                    # print(adj_list)
                    for anode in adj_list:
                        neigh_nodes = list(net.neighbors(anode))
                        for neigh_node in neigh_nodes:
                            if net.nodes[neigh_node]['node_val'] > 0:
                                # print("layer", net_index, nnode, neigh_node, gnode, net.nodes[neigh_node]['node_val'])
                                fgraph.remove_edge(gnode, net.nodes[neigh_node]['node_val'])
                                net.remove_edge(anode, neigh_node)
                            elif net.nodes[neigh_node]['node_val'] == - gnode:
                                new_adj_list.append(neigh_node)
                                net.nodes[neigh_node]['node_val'] = - GraphN - 1
                                net.remove_edge(anode, neigh_node)
                    adj_list = new_adj_list
                
                if len(list(fgraph.neighbors(gnode))) != 0:
                    alloca_nodes_cache[gnode] = nnode
                else:
                    if gnode in alloca_nodes_cache.keys():
                        del alloca_nodes_cache[gnode]
        net_index += 1

    if len(list(fgraph.edges())) != 0:
        for edge in fgraph.edges():
            print(edge[0], edge[1], alloca_nodes_cache)
            if alloca_nodes_cache[edge[0]] != alloca_nodes_cache[edge[1]]:
                print("mapping incomplete error")
            else:
                print("validate success!") 
        # pos = nx.spring_layout(fgraph)
        # labels = {node: str(node) for node in fgraph.nodes()}
        # nx.draw(fgraph, pos = pos, labels  = labels)
        # plt.show()       
    else:
        print("validate success!") 
    return fgraph