import qiskit
from graphix import Circuit
import math
import pyzx as zx
import os


def qasm_to_gate_list(path_to_qasm_file=None):
    """
    for gate in qasm_circuit.data:
        # Gate name
        gate[0].name
        # Gate qubits
        gate[1]
        # Gate parameters, angles
        gate[0].params
    """
    if path_to_qasm_file == None:
        path_to_qasm_file = "qasm_files/2_cnot_test.qasm"    

    qiskit_circuit = qiskit.QuantumCircuit.from_qasm_file(path_to_qasm_file).decompose(reps=3)
    print(qiskit_circuit)
    gate_list = qiskit_circuit.data

    return gate_list
    
def gate_list_to_graphix(qiskit_circuit):
    
    # Initialising the graphix circuit
    nqubit = qiskit_circuit.num_qubits
    graphix_circuit = Circuit(nqubit)
    gate_list = qiskit_circuit.data

    # Going through gate list and adding to equivalent to graphix circuit 
    for gate in gate_list:
        
        if gate[0].name == "rx":
            # Gate qubits
            qubit_reg = gate[1]
            qubit = qiskit_circuit.find_bit(qubit_reg).index
            # Gate parameters, angles
            angle = gate[0].params
            graphix_circuit.rx(qubit, angle)

        elif gate[0].name == "ry":
            # Gate qubits
            qubit_reg = gate[1]
            qubit = qiskit_circuit.find_bit(qubit_reg).index
            # Gate parameters, angles
            angle = gate[0].params
            graphix_circuit.ry(qubit, angle)

        elif gate[0].name == "rz":
            # Gate qubits
            qubit_reg = gate[1]
            qubit = qiskit_circuit.find_bit(qubit_reg).index
            # Gate parameters, angles
            angle = gate[0].params
            graphix_circuit.rz(qubit, angle)

        elif gate[0].name == "h":
            # Gate qubits
            qubit_reg = gate[1]
            qubit = qiskit_circuit.find_bit(qubit_reg).index

            graphix_circuit.h(qubit)
        
        elif gate[0].name == "i":
            # Gate qubits
            qubit_reg = gate[1]
            qubit = qiskit_circuit.find_bit(qubit_reg).index

            graphix_circuit.i(qubit)

        elif gate[0].name == "s":
            # Gate qubits
            qubit_reg = gate[1]
            qubit = qiskit_circuit.find_bit(qubit_reg).index

            graphix_circuit.s(qubit)  
     
        elif gate[0].name == "cx":
            # Extracting the control and target qubits from the gate
            control_reg = gate[1][0]
            target_reg = gate[1][1]

            # Using find_bit to get the indices of the control and target qubits in the circuit
            control = qiskit_circuit.find_bit(control_reg).index
            target = qiskit_circuit.find_bit(target_reg).index

            graphix_circuit.cnot(control, target)

            print(gate)
            print(control_reg,control)
        elif gate[0].name == "ccx":
            # Extracting the control and target qubits from the gate
            control1_reg = gate[1][0]
            control2_reg = gate[1][1]
            target_reg = gate[1][2]

            # Using find_bit to get the indices of the control and target qubits in the circuit
            control1 = qiskit_circuit.find_bit(control1_reg).index
            control2  = qiskit_circuit.find_bit(control2_reg).index
            target = qiskit_circuit.find_bit(target_reg).index

            graphix_circuit.ccx(control1, control2, target)
        
        elif gate[0].name == "u" or "u3":
            """CircuitInstruction(
            operation=Instruction(name='u'
            , num_qubits=1, num_clbits=0
            , params=[3.141592653589793, 0, 3.141592653589793])
            
            , qubits=(Qubit(QuantumRegister(4, 'q'), 0),), clbits=()
            )
            """
            # Gate qubits
            qubit_reg = gate.qubits[0]
            
            qubit = qiskit_circuit.find_bit(qubit_reg).index
            print(qubit_reg, qubit)
            # Decompose U gate into RZ, RY, RZ (ignoring global phase)
            print(gate[0].params)
            
            params = gate[0].params
            if params == []:
                break

            theta = params[0]
            phi = params[1]
            lam = params[2]  # Assuming the first three parameters are theta, phi, lambda
            graphix_circuit.rz(qubit, phi)
            graphix_circuit.ry(qubit, theta)
            graphix_circuit.rz(qubit, lam)


        else:
            gate = gate[0].name 
            # print(f"WARNING missing gate:[{gate}] graphix objet equivalence. Graphix does not have this native gate.")
   
    return graphix_circuit      

    ## rx, rz, ry, h, i, CNOT, s, CCX

'''
path_to_qasm_file = "qasm_files/2_cnot_test.qasm"    
path_to_qasm_file = "qasm_files/debug_circuit_variational_n4_transpiled.qasm"
qiskit_circuit = qiskit.QuantumCircuit.from_qasm_file(path_to_qasm_file).decompose(reps=3)
print(qiskit_circuit)
circuit = gate_list_to_graphix(qiskit_circuit)
pattern = circuit.transpile()
pattern.draw_graph()
'''
"""
    # Going through supported gate types
    for gate in pyZX_circuit.gates:
        if gate.name == "HAD":
            qubit = int(str(gate)[4:-1])
            circuit.h(qubit)

        elif gate.name == "CNOT":
            gate_split = str(gate).split(',')
            qubit1 = int(gate_split[0][5:])
            qubit2 = int(gate_split[1][0:-1])
            # CNOT(0,5)
            circuit.cnot(qubit1, qubit2)

        elif gate.name == "T":
            return print("Encountered T gate, graphix not accurate")
        
        elif gate.name == "S":
            qubit = int(str(gate)[2:-1])
            circuit.s(qubit)

        elif gate.name == "ZPhase":
            qubit, phase_str = str(gate).split(',')
            qubit = int(qubit.split('(')[1])
            phase = eval(phase_str.split('=')[1].strip(')'))
            circuit.rz(qubit, phase)

        elif gate.name == "CZ": # CZ(6,7) analysing 
            return print("Encountered T gate, graphix not accurate")
    
        elif gate.name == "XPhase":
            qubit, phase_str = str(gate).split(',')
            qubit = int(qubit.split('(')[1])
            phase = eval(phase_str.split('=')[1].strip(')'))
            circuit.rx(qubit, phase)
    
        elif gate.name == "YPhase":
            qubit, phase_str = str(gate).split(',')
            qubit = int(qubit.split('(')[1])
            phase = eval(phase_str.split('=')[1].strip(')'))
            circuit.ry(qubit, phase)

        elif gate.name == "ZPhase":
            qubit, phase_str = str(gate).split(',')
            qubit = int(qubit.split('(')[1])
            phase = eval(phase_str.split('=')[1].strip(')'))
            circuit.rz(qubit, phase)

            
        else:
            print(f"Following gate is missing: {gate}")

"""


def qasm_to_graphix(file_path):
    # Initialising the graphix circuit

    with open(file_path, 'w') as new_file:
            for line in lines:
                # Replace 'sx' with 'rx(pi/2)'
                if line.strip().startswith('sx'):
                    line = line.replace('sx', 'rx(pi/2)', 1)
                new_file.write(line)
    file_path = new_file

    # Open the original file
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            print(line)
            if line.strip().startswith('qreg'):
                rhs = line.split('[')[1]
                nqubit = int(rhs.split(']')[0])
                graphix_circuit = Circuit(nqubit)
                break
        else:  
            print("Error: No 'qreg' found in qasm file")
            return
            
        for line in lines: 
            line = line.strip()

            if line.startswith('rx'):
                # Extract angle and qubit number
                angle_part, qubit_part = line.split(' ')[1].split(')')
                angle = eval(angle_part.split('(')[1], {"pi": math.pi})
                qubit = int(qubit_part.split('[')[1].split(']')[0])
                graphix_circuit.rx(qubit, angle)

            elif line.startswith('ry'):
                # Extract angle and qubit number
                angle_part, qubit_part = line.split(' ')[1].split(')')
                angle = eval(angle_part.split('(')[1], {"pi": math.pi})
                qubit = int(qubit_part.split('[')[1].split(']')[0])
                graphix_circuit.ry(qubit, angle)

            elif line.startswith('rz'):
                # Extract angle and qubit number
                angle_part, qubit_part = line.split(' ')[1].split(')')
                angle = eval(angle_part.split('(')[1], {"pi": math.pi})
                qubit = int(qubit_part.split('[')[1].split(']')[0])
                graphix_circuit.rz(qubit, angle)

            elif line.startswith('cx'):
                # cx q[0],q[1];
                qubit1_c = line.split(',')[0] # cx q[0]
                qubit1_b = qubit1_c.split('[')[1] # 0]
                qubit1_a = qubit1_b.split(']')[0] # 0
                control = int(qubit1_a)

                qubit2_c = line.split(',')[1] # q[1]
                qubit2_b = qubit2_c.split('[')[1] # 1]
                qubit2_a =  qubit2_b.split(']')[0] # 1
                target = int(qubit2_a)
                graphix_circuit.cnot(control, target)


    return graphix_circuit

def pyZX_to_graphix(pyZX_circuit, nqubit):
    # Initalise the graphix circuit
    circuit = Circuit(nqubit)

    # Going through supported gate types
    for gate in pyZX_circuit.gates:
        if gate.name == "HAD":
            qubit = int(str(gate)[4:-1])
            circuit.h(qubit)

        elif gate.name == "CNOT":
            gate_split = str(gate).split(',')
            qubit1 = int(gate_split[0][5:])
            qubit2 = int(gate_split[1][0:-1])
            # CNOT(0,5)
            circuit.cnot(qubit1, qubit2)

        elif gate.name == "T":
            return print("Encountered T gate, graphix not accurate")
        
        elif gate.name == "S":
            qubit = int(str(gate)[2:-1])
            circuit.s(qubit)

        elif gate.name == "ZPhase":
            qubit, phase_str = str(gate).split(',')
            qubit = int(qubit.split('(')[1])
            phase = eval(phase_str.split('=')[1].strip(')'))
            circuit.rz(qubit, phase)

        elif gate.name == "CZ": # CZ(6,7) analysing 
            return print("Encountered T gate, graphix not accurate")
    
        elif gate.name == "XPhase":
            qubit, phase_str = str(gate).split(',')
            qubit = int(qubit.split('(')[1])
            phase = eval(phase_str.split('=')[1].strip(')'))
            circuit.rx(qubit, phase)
    
        elif gate.name == "YPhase":
            qubit, phase_str = str(gate).split(',')
            qubit = int(qubit.split('(')[1])
            phase = eval(phase_str.split('=')[1].strip(')'))
            circuit.ry(qubit, phase)

        elif gate.name == "ZPhase":
            qubit, phase_str = str(gate).split(',')
            qubit = int(qubit.split('(')[1])
            phase = eval(phase_str.split('=')[1].strip(')'))
            circuit.rz(qubit, phase)
            
        elif gate.name == "ZPhase":
            qubit, phase_str = str(gate).split(',')
            qubit = int(qubit.split('(')[1])
            phase = eval(phase_str.split('=')[1].strip(')'))
            circuit.rz(qubit, phase)

            
        else:
            print(f"Following gate is missing: {gate}")

    return circuit




path_to_qasm_file = "qasm_files/2_cnot_test.qasm"
path_to_qasm_file = "qasm_files/debug_circuit_variational_n4_transpiled.qasm"

"""
TODO:
Find equivalent for
sx q[1]
tdg q[1]
"""




def process_files_in_folder(folder_path):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"The folder {folder_path} does not exist.")
        return

    print(len(os.listdir(folder_path)))
    # List all files in the folder
    count = 0
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Check if it's a file and not a directory
        if os.path.isfile(file_path):
            try:
                # Try to load the QASM file into a PyZX circuit
                pyzx_circuit = zx.Circuit.from_qasm_file(file_path)
                print(f"Successfully loaded: {filename}")
                # Further processing of the circuit can be done here

            except TypeError as e:
                # Handle the TypeError
                print(f"TypeError occurred for file {filename}: {e}")
        count += 1 
    return print(count)

# Example usage
folder_path = 'qasm_files/QASM_files_from_Qubit'
process_files_in_folder(folder_path)

path_to_qasm_file = "qasm_files/2_cnot_test.qasm"
path_to_qasm_file = "qasm_files/debug_circuit_variational_n4_transpiled.qasm"

pyzx_circuit= zx.Circuit.from_qasm_file(path_to_qasm_file)
nqubits = pyzx_circuit.qubits

graphix_circ = pyZX_to_graphix(pyzx_circuit, nqubits) 
pattern = graphix_circ.transpile()
pattern.draw_graph()