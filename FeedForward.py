def feed_forward_transformation(net_list, fgraph,  graph_node_to_net, graph_edge_to_path):
    pre_node_finished = []
    for i in range(len(net_list)):
        for nnode in net_list[i].nodes():
            if net_list[i].nodes[nnode]['node_val'] > 0:
                for direction in net_list[i].nodes[nnode]['depend_list_fusion'].keys():
                    for depth in range(len(net_list[i].nodes[nnode]['phase'][direction])):
                        list_copy = list(net_list[i].nodes[nnode]['depend_list_fusion'][direction][depth]).copy()
                        net_list[i].nodes[nnode]['depend_list_fusion'][direction][depth] = list_copy

    layer_index = 0
    for i in range(len(net_list)):
        layer_index += 1
        for nnode in net_list[i].nodes():
            if net_list[i].nodes[nnode]['node_val'] > 0:
                if net_list[i].nodes[nnode]['node_val'] not in pre_node_finished:
                    # print(layer_index, net_list[i].nodes[nnode]['node_val'])
                    # print(pre_node_finished)
                    pre_node_finished.append(net_list[i].nodes[nnode]['node_val'])
                    keys = list(net_list[i].nodes[nnode]['depend_list_fusion'].keys()).copy()
                    for direction in keys:
                        for depth in range(len(net_list[i].nodes[nnode]['phase'][direction])):
                            depend_list_fusion = []
                            for fusion_pair in net_list[i].nodes[nnode]['depend_list_fusion'][direction][depth]:
                                if fusion_pair not in fgraph.edges():
                                    print(fusion_pair)
                                    print("error")
                                depend_list_fusion += graph_edge_to_path[fusion_pair]
                            net_list[i].nodes[nnode]['depend_list_fusion'][direction][depth] = depend_list_fusion.copy()

                        if direction == 0:
                            x_set = list(net_list[i].nodes[nnode]["depend_list_x"][0]).copy()
                            net_list[i].nodes[nnode]["depend_list_x"][0] = []
                            for depend_x in x_set:
                                net_list[i].nodes[nnode]["depend_list_x"][0].append((graph_node_to_net[depend_x[0]], depend_x[1], depend_x[2]))
                        else:    
                            for depth in range(len(net_list[i].nodes[nnode]['phase'][direction])):
                                x_set = list(net_list[i].nodes[nnode]["depend_list_x"][direction][depth]).copy()
                                net_list[i].nodes[nnode]["depend_list_x"][direction][depth] = []
                                for depend_x in x_set:
                                    net_list[i].nodes[nnode]["depend_list_x"][direction][depth].append((graph_node_to_net[depend_x[0]], depend_x[1], depend_x[2]))

                        if direction == 0:
                            z_set = list(net_list[i].nodes[nnode]["depend_list_z"][0]).copy()
                            net_list[i].nodes[nnode]["depend_list_z"][0] = []
                            for depend_z in z_set:
                                net_list[i].nodes[nnode]["depend_list_z"][0].append((graph_node_to_net[depend_z[0]], depend_z[1], depend_z[2]))
                        else:    
                            for depth in range(len(net_list[i].nodes[nnode]['phase'][direction])):
                                z_set = list(net_list[i].nodes[nnode]["depend_list_z"][direction][depth]).copy()
                                net_list[i].nodes[nnode]["depend_list_z"][direction][depth] = []
                                for depend_z in z_set:
                                    net_list[i].nodes[nnode]["depend_list_z"][direction][depth].append((graph_node_to_net[depend_z[0]], depend_z[1], depend_z[2]))
                # else:
                    # print(pre_node_finished)
    return net_list