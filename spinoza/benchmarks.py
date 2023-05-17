import pyperf
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


if __name__ == "__main__":
    setup="""
from spinoza_py import QuantumRegister, QuantumCircuit

def qcbm(n):
    pairs = [(i, (i + 1) % n) for i in range(n)]
    q = QuantumRegister(n)
    qc = QuantumCircuit(q)

    for i in range(n):
        qc.rx(1.0, i)
        qc.rz(1.0, i)

    for a, b in pairs:
        qc.cx(a, b)

    for d in range(9):
        for i in range(n):
            qc.rz(1.0, i)
            qc.rx(1.0, i)
            qc.rz(1.0, i)

        for a, b in pairs:
            qc.cx(a, b)

    for i in range(n):
        qc.rz(1.0, i)
        qc.rx(1.0, i)

    qc.execute();
"""
    nqubits_list = range(4, 27)
    runner = pyperf.Runner()

    for i in nqubits_list:
        runner.timeit(f"qcbm {i}", stmt='qcbm(n)', setup=setup+f"n = {i}")
