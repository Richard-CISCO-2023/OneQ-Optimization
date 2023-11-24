# alpha = phase * 1/4 pi
class JGate:
    def __init__(self, qubit, phase, gate_name):
        self.qubit = qubit
        self.phase = phase
        self.gate_name = gate_name 
    def type(self):
        return "J"
        
    
class CZGate:
    def __init__(self, qubit1, qubit2, gate_name):
        self.qubit1 = qubit1
        self.qubit2 = qubit2
        self.gate_name = gate_name 
    
    def type(self):
        return "CZ"


class JCZCircuit:
    def __init__(self):
        self.qubits = []
        self.gates = []

    def qubits_init(self, qubits):
        self.qubits = qubits

    def add_J(self, qubit, phase):
        gate_name = 'J'
        self.gates.append(JGate(qubit, phase, gate_name=gate_name))

    # uni 
    def add_H(self, qubit):
        gate_name = 'H'
        self.gates.append(JGate(qubit, 0, gate_name=gate_name))

    # uni 
    def add_X(self, qubit):
        gate_name = 'X'
        self.gates.append(JGate(qubit, 0, gate_name=gate_name))
        self.gates.append(JGate(qubit, 4, gate_name=gate_name))
    
    def add_Z(self, qubit):
        gate_name = 'Z'
        self.gates.append(JGate(qubit, 4, gate_name=gate_name))
        self.gates.append(JGate(qubit, 0, gate_name=gate_name))
    
    # uni 
    def add_T(self, qubit):
        gate_name = 'T'
        self.gates.append(JGate(qubit, 1, gate_name=gate_name))
        self.gates.append(JGate(qubit, 0, gate_name=gate_name))
    
    # uni
    def add_S(self, qubit):
        gate_name = 'S'
        self.gates.append(JGate(qubit, 2, gate_name=gate_name))
        self.gates.append(JGate(qubit, 0, gate_name=gate_name))
    
    def add_Rz(self, qubit, phase):
        gate_name = 'Rz'
        self.gates.append(JGate(qubit, phase, gate_name=gate_name))
        self.gates.append(JGate(qubit, 0, gate_name=gate_name))

    def add_CZ(self, qubit1, qubit2):
        gate_name = 'CZ'
        self.gates.append(CZGate(qubit1, qubit2, gate_name=gate_name))

    # uni
    def add_CNOT(self, qubit1, qubit2):
        gate_name = 'CNOT'
        # Assumption that CNOT = H + CZ + H 
        # Adding H Gate manually
        self.gates.append(JGate(qubit2, 0, gate_name=gate_name))
        # Adding CZ Gate manually
        self.gates.append(CZGate(qubit1, qubit2, gate_name=gate_name))
        # Adding H Gate manually
        self.gates.append(JGate(qubit2, 0, gate_name=gate_name))
    
    def add_CRz(self, qubit1, qubit2, phase):
        # Assumption that CRz = Rz + Rz + CNOT + Rz + CNOT gates
        gate_name = 'CRz'
        # Adding Rz Gate manually
        self.gates.append(JGate(qubit1, phase, gate_name=gate_name))
        self.gates.append(JGate(qubit1, 0, gate_name=gate_name))
        self.gates.append(JGate(qubit2, phase, gate_name=gate_name))
        self.gates.append(JGate(qubit2, 0, gate_name=gate_name))
        # Adding CNOT Gate manually
        self.gates.append(JGate(qubit2, 0, gate_name=gate_name))
        # Adding CZ Gate manually
        self.gates.append(CZGate(qubit1, qubit2, gate_name=gate_name))
        # Adding H Gate manually
        self.gates.append(JGate(qubit2, 0, gate_name=gate_name))

        # Adding Rz Gate manually 
        self.gates.append(JGate(qubit2, phase, gate_name=gate_name))
        self.gates.append(JGate(qubit2, 0, gate_name=gate_name))

        # Adding CNOT gate manually 
        self.gates.append(JGate(qubit2, 0, gate_name=gate_name))
        # Adding CZ Gate manually
        self.gates.append(CZGate(qubit1, qubit2, gate_name=gate_name))
        # Adding H Gate manually
        self.gates.append(JGate(qubit2, 0, gate_name=gate_name))
    #-------------#
    #New additions#
    #-------------#
    def add_Rx(self, qubit, phase):
        gate_name = 'Rx'
        self.gates.append(JGate(qubit, 0, gate_name=gate_name))
        # Adding Rz Gate manually
        self.gates.append(JGate(qubit, phase, gate_name=gate_name))
        self.gates.append(JGate(qubit, 0, gate_name=gate_name))
        # Adding H Gate manually
        self.gates.append(JGate(qubit, 0, gate_name=gate_name))


import pyzx as zx
def pyZX_to_JCZ(pyZX_circuit, nqubit):
    # Initalise the JCZ circuit
    qubits = []
    for i in range(nqubit):
        qubits.append(i)
    jcz_circuit = JCZCircuit()
    jcz_circuit.qubits_init(qubits)

    # Going through supported gate types
    for gate in pyZX_circuit.gates:
        if gate.name == "HAD":
            jcz_circuit.add_H(int(str(gate)[4:-1]))

        elif gate.name == "CNOT":
            gate_split = str(gate).split(',')
            qubit1 = int(gate_split[0][5:])
            qubit2 = int(gate_split[1][0:-1])
            jcz_circuit.add_CNOT(qubit1, qubit2)

        elif gate.name == "T":
            jcz_circuit.add_T(int(str(gate)[2:-1]))

        elif gate.name == "ZPhase":
            qubit, phase_str = str(gate).split(',')
            qubit = int(qubit.split('(')[1])
            phase = eval(phase_str.split('=')[1].strip(')'))
            jcz_circuit.add_Rz(qubit, phase) 

        elif gate.name == "XPhase":
            qubit, phase_str = str(gate).split(',')
            qubit = int(qubit.split('(')[1])
            phase = eval(phase_str.split('=')[1].strip(')'))
            jcz_circuit.add_Rx(qubit, phase) 
    return jcz_circuit
'''
add_H(qubit)
add_CNOT(qubit1, qubit2)
add_T(qubit)
----------------
add_J(qubit, phase)
add_X(qubit)
add_Z(qubit)
add_S(qubit)
add_Rz(qubit, phase)
add_CZ(qubit1, qubit2)
add_CRz(qubit1, qubit2, phase)


add_J(qubit, phase)
add_H(qubit)
add_X(qubit)
add_Z(qubit)
add_T(qubit)
add_S(qubit)
add_Rz(qubit, phase)
add_CZ(qubit1, qubit2)
add_CNOT(qubit1, qubit2)
add_CRz(qubit1, qubit2, phase)
'''