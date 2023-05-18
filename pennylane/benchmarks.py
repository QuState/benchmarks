import mkl
import pyperf

mkl.set_num_threads(1)


if __name__ == "__main__":
    setup="""
import pennylane as qml
import numpy as np


def first_rotation(circuit, nqubits):
    for k in range(nqubits):
        circuit.append(qml.RX(np.random.rand(), wires=k))
        circuit.append(qml.RZ(np.random.rand(), wires=k))


def mid_rotation(circuit, nqubits):
    for k in range(nqubits):
        circuit.append(qml.RZ(np.random.rand(), wires=k))
        circuit.append(qml.RX(np.random.rand(), wires=k))
        circuit.append(qml.RZ(np.random.rand(), wires=k))


def last_rotation(circuit, nqubits):
    for k in range(nqubits):
        circuit.append(qml.RZ(np.random.rand(), wires=k))
        circuit.append(qml.RX(np.random.rand(), wires=k))


def entangler(circuit, nqubits, pairs):
    for a, b in pairs:
        circuit.append(qml.CNOT(wires=[a, b]))


def build_circuit(nqubits, depth, pairs):
    circuit = []
    first_rotation(circuit, nqubits)
    entangler(circuit, nqubits, pairs)
    for k in range(depth):
        mid_rotation(circuit, nqubits)
        entangler(circuit, nqubits, pairs)

    last_rotation(circuit, nqubits)
    return circuit
"""

    runner = pyperf.Runner()

    for i in range(4, 27):
        runner.timeit(f"qcbm {i}", stmt='st.apply(circuit)', setup=setup+f"nqubits = {i}; pairs = [(i, (i + 1) % nqubits) for i in range(nqubits)]; circuit = build_circuit(nqubits, 9, pairs); st = qml.device('lightning.qubit', nqubits);")
