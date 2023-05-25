import mkl
import pennylane as qml
import numpy as np
import pyperf

mkl.set_num_threads(1)


def first_rotation(circuit, nqubits, angles):
    for k in range(nqubits):
        circuit.append(qml.RX(angles.pop(), wires=k))
        circuit.append(qml.RZ(angles.pop(), wires=k))


def mid_rotation(circuit, nqubits, angles):
    for k in range(nqubits):
        circuit.append(qml.RZ(angles.pop(), wires=k))
        circuit.append(qml.RX(angles.pop(), wires=k))
        circuit.append(qml.RZ(angles.pop(), wires=k))


def last_rotation(circuit, nqubits, angles):
    for k in range(nqubits):
        circuit.append(qml.RZ(angles.pop(), wires=k))
        circuit.append(qml.RX(angles.pop(), wires=k))


def entangler(circuit, nqubits, pairs):
    for a, b in pairs:
        circuit.append(qml.CNOT(wires=[a, b]))


def build_circuit(nqubits, depth, pairs):
    np.random.seed(42)
    angles = [np.random.rand() for _ in range(1000)]

    circuit = []
    first_rotation(circuit, nqubits, angles)
    entangler(circuit, nqubits, pairs)
    for _ in range(depth):
        mid_rotation(circuit, nqubits, angles)
        entangler(circuit, nqubits, pairs)

    last_rotation(circuit, nqubits, angles)
    return circuit


if __name__ == "__main__":
    import time

    for nqubits in range(4, 26):
        start = time.time()
        pairs = [(i, (i + 1) % nqubits) for i in range(nqubits)]
        circuit = build_circuit(nqubits, 9, pairs)
        st = qml.device('lightning.qubit', nqubits)
        st.apply(circuit)
        end = time.time()
        print(f"{nqubits} qubits ... {end - start} elapsed")
