import pyzx as zx
import networkx as nx
import JCZCircuit as JCZ


# using pyzx to help draw cz j circuit, assume xphase to be j phase
def show_circuit(qubits, gates_list):
    c = zx.Circuit(qubit_amount=qubits)
    for gate in gates_list:
        if gate.type() == "J":
            if gate.gate_name == 'H':
                 c.add_gate("HAD",gate.qubit )
                 
            else:
            # XPhase. 
                c.add_gate("XPhase", gate.qubit, phase = gate.phase / 4)
            #c.add_gate("HAD",gate.qubit )
        elif gate.type() == "CZ":
            c.add_gate("CZ", gate.qubit1, gate.qubit2)
    print('--------------- \nCurrently generate_graph_state, Below is JCZ conversion in pyZX graph')
    
    g = c.to_graph()
    zx.draw(g)
    #zx.to_rg(g)
    #zx.draw(g)
    #print("T count: " + str (zx.tcount(g)))
    
    #re_c = JCZ.pyZX_to_JCZ(c, 4) reinputting JCZ
    
    return


def add_undirected_edge(graph, node1, node2):
    graph.add_edge(node1, node2)
    graph.add_edge(node2, node1)
    return graph

def turn_to_graph(gates_list, qubits):
    """
    PURPOSE 
    
    USED was used in Main() but is commented out
    -----------------------------------------
    INPUT
    gates_list = 
    qubits =
    -----------------------------------------
    OUTPUT
    graph = networkx graph object
    """
    node_index = 1
    pos_x = 0
    pre_nodes = {}
    CZ_consecutive_path = []
    for q in range(qubits):
        pre_nodes[q] = -1

    graph = nx.DiGraph()
    for gate in gates_list: # Here gate is either a gate.tpye 
        # CZ_consecutive_path.clear()
        if gate.type() == "J":
            qubit = gate.qubit
            gate_name = gate.gate_name 
            if qubit in CZ_consecutive_path:
                CZ_consecutive_path.clear()
            if pre_nodes[gate.qubit] == -1:
                graph.add_node(node_index, node_val = "In", pos = (pos_x, - qubit), phase = gate.phase, gate_name = gate_name)
                graph.add_node(node_index + 1, node_val = "Out", pos  = (pos_x + 3, - qubit), phase = -1, gate_name = gate_name)
                # if gate.phase % 2 == 0:
                #     add_undirected_edge(graph, node_index, node_index + 1)
                # else:
                # print("non clifford")
                graph.add_edge(node_index, node_index + 1)
                qubit = gate.qubit
                pre_nodes[qubit] = node_index + 1
                pos_x += 6
                node_index += 2
            else:
                pre_node = pre_nodes[gate.qubit]
                if graph.nodes[pre_node]['node_val'] == "Out":
                    graph.nodes[pre_node]['node_val'] = "Aux"
                else:
                    graph.nodes[pre_node]['node_val'] = "In"
                qubit = gate.qubit
                graph.add_node(node_index, node_val = "Out", pos = (pos_x, - qubit), phase = -1 , gate_name = gate_name)
                # if gate.phase % 2 == 0:
                #     add_undirected_edge(graph, pre_node, node_index)
                # else:
                    # print("non clifford")
                graph.nodes[pre_node]['phase'] = gate.phase
                graph.add_edge(pre_node, node_index)
                pre_nodes[qubit] = node_index
                pos_x += 3
                node_index += 1
        else:
            qubit1 = gate.qubit1
            qubit2 = gate.qubit2
            if pre_nodes[qubit1] == -1:
                graph.add_node(node_index, node_val = "IO", pos = (pos_x, - qubit1), phase = -1, gate_name = gate_name)
                pre_nodes[qubit1] = node_index
                node_q1 = node_index
                pos_x += 3
                node_index += 1
            else:
                node_q1 = pre_nodes[qubit1]
            
            if pre_nodes[qubit2] == -1:
                graph.add_node(node_index, node_val = "IO", pos = (pos_x, - qubit2), phase = -1, gate_name = gate_name)
                pre_nodes[qubit2] = node_index
                node_q2 = node_index
                pos_x += 3
                node_index += 1
            else:
                node_q2 = pre_nodes[qubit2]
            

            graph = add_undirected_edge(graph, node_q1, node_q2)
            CZ_consecutive_path.clear()
            CZ_consecutive_path.append(node_q1)
            CZ_consecutive_path.append(node_q2)
            # print(CZ_consecutive_path)

    return graph

import matplotlib.pyplot as plt
def generate_graph_state(gates_list, qubits):
    show_circuit(qubits, gates_list)
    #show_circuit(4, re_c.gates)
    graph = turn_to_graph(gates_list, qubits)
    print('-------------- \nBelow is the JCZ pyZX in graph form')
    plt.figure()
    nx.draw(graph)
    plt.title('turnToGraph ---> generate graph state')
    plt.savefig(f"saved_files/turnToGraph")
    plt.show() 
    colors = []
    input_nodes = []
    output_nodes = []

    for node_id, attrs in graph.nodes(data=True):
        print(f'2.Node index: {node_id}, Node attribute {attrs}')

    for nnode in graph.nodes():
        if graph.nodes[nnode]['node_val'] == "Out":
            colors.append('blue')
            output_nodes.append(nnode)
        elif graph.nodes[nnode]['node_val'] == "In":
            colors.append('red')
            input_nodes.append(nnode)
        elif graph.nodes[nnode]['node_val'] == "IO":
            colors.append('green')
            input_nodes.append(nnode)
            output_nodes.append(nnode)
        else:
            colors.append('gray')
    #labels = {node: str(node) for node in graph.nodes()}
    labels = {node: f'{node}\n{attrs.get("gate_name", "")}' for node, attrs in graph.nodes(data=True)}
    print(f'Labels dict : {labels}')
    node_pos = nx.get_node_attributes(graph, 'pos')
    print('-------------- \nBelow is the JCZ pyZX after additional details have been assigned')
    plt.figure()
    nx.draw(graph, pos = node_pos, node_color = colors, node_size = 30, labels = labels,font_size = 6)
    plt.title('Generate graph state output')
    plt.show() 
    return graph, input_nodes, colors, labels