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
        self.qubit_gates = {}

    def qubits_init(self, qubits):
        self.qubits = qubits
        for q in qubits:
            self.qubit_gates[q] = []

    def add_H(self, qubit):
        self.qubit_gates[qubit].append(JGate(qubit, 0))
        self.gates.append(JGate(qubit, 0))

    def add_X(self, qubit):
        self.qubit_gates[qubit].append(JGate(qubit, 4))
        self.qubit_gates[qubit].append(JGate(qubit, 0))
        self.gates.append(JGate(qubit, 4))
        self.gates.append(JGate(qubit, 0))
    
    def add_Z(self, qubit):
        self.qubit_gates[qubit].append(JGate(qubit, 0))
        self.qubit_gates[qubit].append(JGate(qubit, 4))
        self.gates.append(JGate(qubit, 0))
        self.gates.append(JGate(qubit, 4))
