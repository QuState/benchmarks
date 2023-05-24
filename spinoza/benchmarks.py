import numpy as np
from spinoza_py import QuantumRegister, QuantumCircuit


def first_rotation(circuit, nqubits):
    for k in range(nqubits):
        circuit.rx(np.random.rand(), k)
        circuit.rz(np.random.rand(), k)


def mid_rotation(circuit, nqubits):
    for k in range(nqubits):
        circuit.rz(np.random.rand(), k)
        circuit.rx(np.random.rand(), k)
        circuit.rz(np.random.rand(), k)


def last_rotation(circuit, nqubits):
    for k in range(nqubits):
        circuit.rz(np.random.rand(), k)
        circuit.rx(np.random.rand(), k)


def entangler(circuit, pairs):
    for a, b in pairs:
        circuit.cx(a, b)


def build_circuit(nqubits, depth, pairs):
    q = QuantumRegister(nqubits)
    circuit = QuantumCircuit(q)
    first_rotation(circuit, nqubits)
    entangler(circuit, pairs)
    for k in range(depth):
        mid_rotation(circuit, nqubits)
        entangler(circuit, pairs)

    last_rotation(circuit, nqubits)
    return circuit


if __name__ == "__main__":
    import time

    for nqubits in range(4, 20):
        start = time.time()
        pairs = [(i, (i + 1) % nqubits) for i in range(nqubits)]
        circuit = build_circuit(nqubits, 9, pairs)
        circuit.execute()
        end = time.time()
        print(end - start)
