def feed_forward_transformation(net_list, fgraph,  graph_node_to_net, graph_edge_to_path):
    pre_node_finished = []
    for net_i in reversed(net_list):
        for nnode in net_i.nodes():
            if net_i.nodes[nnode]['node_val'] > 0:
                for direction in net_i.nodes[nnode]['depend_list_fusion'].keys():
                    for fusion_pair in net_i.nodes[nnode]['depend_list_fusion'][direction]:
                        if type(fusion_pair) is tuple:
                            print(fusion_pair)
                            continue
                        else:
                            print("false")
    layer_index = 0
    for i in range(len(net_list)):
        layer_index += 1
        for nnode in net_list[len(net_list) - 1 - i].nodes():
            if net_list[len(net_list) - 1 - i].nodes[nnode]['node_val'] > 0:
                if net_list[len(net_list) - 1 - i].nodes[nnode]['node_val'] not in pre_node_finished:
                    print(layer_index, net_list[len(net_list) - 1 - i].nodes[nnode]['node_val'])
                    print(pre_node_finished)
                    pre_node_finished.append(net_list[len(net_list) - 1 - i].nodes[nnode]['node_val'])
                    keys = list(net_list[len(net_list) - 1 - i].nodes[nnode]['depend_list_fusion'].keys()).copy()
                    for direction in keys:
                        fusion_set = list(net_list[len(net_list) - 1 - i].nodes[nnode]['depend_list_fusion'][direction]).copy()
                        net_list[len(net_list) - 1 - i].nodes[nnode]['depend_list_fusion'][direction] = []
                        for fusion_pair in fusion_set:
                            if type(fusion_pair) is not tuple:
                                print("is not tuple")
                        for fusion_pair in fusion_set:
                            if fusion_pair not in fgraph.edges():
                                print(fusion_pair)
                                print("error")
                            net_list[len(net_list) - 1 - i].nodes[nnode]['depend_list_fusion'][direction].append(graph_edge_to_path[fusion_pair])

                        if direction == 0:
                            x_set = list(net_list[len(net_list) - 1 - i].nodes[nnode]["depend_list_x"][0]).copy()
                            net_list[len(net_list) - 1 - i].nodes[nnode]["depend_list_x"][0] = []
                            for depend_x in x_set:
                                net_list[len(net_list) - 1 - i].nodes[nnode]["depend_list_x"][0].append((graph_node_to_net[depend_x[0]], depend_x[1], depend_x[2]))
                        else:    
                            for depth in range(len(net_list[len(net_list) - 1 - i].nodes[nnode]['phase'][direction])):
                                x_set = list(net_list[len(net_list) - 1 - i].nodes[nnode]["depend_list_x"][direction][depth]).copy()
                                net_list[len(net_list) - 1 - i].nodes[nnode]["depend_list_x"][direction][depth] = []
                                for depend_x in x_set:
                                    net_list[len(net_list) - 1 - i].nodes[nnode]["depend_list_x"][direction][depth].append((graph_node_to_net[depend_x[0]], depend_x[1], depend_x[2]))

                        if direction == 0:
                            z_set = list(net_list[len(net_list) - 1 - i].nodes[nnode]["depend_list_z"][0]).copy()
                            net_list[len(net_list) - 1 - i].nodes[nnode]["depend_list_z"][0] = []
                            for depend_z in z_set:
                                net_list[len(net_list) - 1 - i].nodes[nnode]["depend_list_z"][0].append((graph_node_to_net[depend_z[0]], depend_z[1], depend_z[2]))
                        else:    
                            for depth in range(len(net_list[len(net_list) - 1 - i].nodes[nnode]['phase'][direction])):
                                z_set = list(net_list[len(net_list) - 1 - i].nodes[nnode]["depend_list_z"][direction][depth]).copy()
                                net_list[len(net_list) - 1 - i].nodes[nnode]["depend_list_z"][direction][depth] = []
                                for depend_z in z_set:
                                    net_list[len(net_list) - 1 - i].nodes[nnode]["depend_list_z"][direction][depth].append((graph_node_to_net[depend_z[0]], depend_z[1], depend_z[2]))
                else:
                    print(pre_node_finished)
    return net_list