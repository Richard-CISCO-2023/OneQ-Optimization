# alpha = phase * 1/4 pi
class JGate:
    def __init__(self, qubit, phase):
        self.qubit = qubit
        self.phase = phase
    
    def type(self):
        return "J"
    
class CZGate:
    def __init__(self, qubit1, qubit2):
        self.qubit1 = qubit1
        self.qubit2 = qubit2
    
    def type(self):
        return "CZ"


class JCZCircuit:
    def __init__(self):
        self.qubits = []
        self.gates = []

    def qubits_init(self, qubits):
        self.qubits = qubits

    def add_J(self, qubit, phase):
        self.gates.append(JGate(qubit, phase))

    # uni 
    def add_H(self, qubit):
        self.gates.append(JGate(qubit, 0))

    # uni 
    def add_X(self, qubit):
        self.gates.append(JGate(qubit, 0))
        self.gates.append(JGate(qubit, 4))
    
    def add_Z(self, qubit):
        self.gates.append(JGate(qubit, 4))
        self.gates.append(JGate(qubit, 0))
    
    # uni 
    def add_T(self, qubit):
        self.gates.append(JGate(qubit, 1))
        self.gates.append(JGate(qubit, 0))
    
    # uni
    def add_S(self, qubit):
        self.gates.append(JGate(qubit, 2))
        self.gates.append(JGate(qubit, 0))
    
    def add_Rz(self, qubit, phase):
        self.gates.append(JGate(qubit, phase))
        self.gates.append(JGate(qubit, 0))

    def add_CZ(self, qubit1, qubit2):
        self.gates.append(CZGate(qubit1, qubit2))

    # uni
    def add_CNOT(self, qubit1, qubit2):
        self.add_H(qubit2)
        self.add_CZ(qubit1, qubit2)
        self.add_H(qubit2)
    
    def add_CRz(self, qubit1, qubit2, phase):
        self.add_Rz(qubit1, phase)
        self.add_Rz(qubit2, phase)
        self.add_CNOT(qubit1,qubit2)
        self.add_Rz(qubit2, phase)
        self.add_CNOT(qubit1,qubit2) 
    #-------------#
    #New additions#
    #-------------#
    def add_Rx(self, qubit, phase):
        self.add_H(qubit)
        self.add_Rz(qubit, phase)
        self.add_H(qubit)

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