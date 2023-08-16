import pyzx as zx
import random
from JCZCircuit import *

def generate_circuit(nqubit, depth):
    circuit = zx.generate.CNOT_HAD_PHASE_circuit(qubits=nqubit,depth=depth,clifford=False)
    # zx.draw(circuit)
    # circuit = zx.optimize.basic_optimization(circuit.to_basic_gates())
    # zx.draw(circuit)
    # print(circuit.gates)
    qubits = []
    for i in range(nqubit):
        qubits.append(i)
    jcz_circuit = JCZCircuit()
    jcz_circuit.qubits_init(qubits)
    for gate in circuit.gates:
        # print(gate)
        if gate.name == "HAD":
            jcz_circuit.add_H(int(str(gate)[4:-1]))
        elif gate.name == "CNOT":
            gate_split = str(gate).split(',')
            qubit1 = int(gate_split[0][5:])
            qubit2 = int(gate_split[1][0:-1])
            jcz_circuit.add_CNOT(qubit1, qubit2)
        elif gate.name == "T":
            jcz_circuit.add_T(int(str(gate)[2:-1]))

    # zx.draw(circuit)
    # gates_list = [CZGate(0, 2), JGate(0, 1), CZGate(0, 1), CZGate(0, 1), CZGate(0, 1), JGate(1, 3), JGate(1, 2)]

    return  jcz_circuit.gates, nqubit

def construct_qft(nqubit):
    jcz_circuit = JCZCircuit()
    for target in range(nqubit - 1):
        jcz_circuit.add_H(target)
        for control in range(target + 1, nqubit):
            phase = random.randint(0, 7)
            jcz_circuit.add_CRz(control, target, phase)
    jcz_circuit.add_H(nqubit - 1)
    return jcz_circuit.gates, nqubit