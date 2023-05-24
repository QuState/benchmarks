import mkl
import pennylane as qml
import numpy as np
import pyperf

mkl.set_num_threads(1)


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


if __name__ == "__main__":
    import time

    start = time.time()
    nqubits = 4
    pairs = [(i, (i + 1) % nqubits) for i in range(nqubits)]
    circuit = build_circuit(nqubits, 9, pairs)
    st = qml.device('lightning.qubit', nqubits)
    st.apply(circuit)
    end = time.time()
    print(end - start)

