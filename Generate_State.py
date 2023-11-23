import networkx as nx
import matplotlib.pyplot as plt
import random

def generate_state(nqubit):
    G = nx.gnp_random_graph(nqubit, 0.5)
    
    return G


if __name__ == '__main__':

    nqubits = 10
    G = generate_state(nqubits)
    nx.draw(G,  pos=nx.fruchterman_reingold_layout(G))
    plt.title(f'{nqubits} Qubit generated state')
    plt.savefig(f"saved_files/{nqubits}_qubit_gs")