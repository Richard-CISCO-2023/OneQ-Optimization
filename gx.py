from graphix import Circuit
circuit = Circuit(4)
circuit.h(0)
pattern = circuit.transpile()
pattern.draw_graph()