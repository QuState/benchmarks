import pyperf


if __name__ == "__main__":
    setup="""
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


def entangler(circuit, nqubits, pairs):
    for a, b in pairs:
        circuit.cx(a, b)


def build_circuit(nqubits, depth, pairs):
    q = QuantumRegister(nqubits)
    circuit = QuantumCircuit(q)
    first_rotation(circuit, nqubits)
    entangler(circuit, nqubits, pairs)
    for k in range(depth):
        mid_rotation(circuit, nqubits)
        entangler(circuit, nqubits, pairs)

    last_rotation(circuit, nqubits)
    return circuit
    """
    nqubits_list = range(4, 27)
    runner = pyperf.Runner()

    for i in nqubits_list:
        runner.timeit(f"qcbm {i}", stmt='circuit.execute()', setup=setup+f"nqubits = {i}; pairs = [(i, (i + 1) % nqubits) for i in range(nqubits)]; circuit = build_circuit(nqubits, 9, pairs);")
