from qiskit import Aer, QuantumCircuit, execute
from qiskit.compiler import transpile, assemble
import numpy as np

import mkl
mkl.set_num_threads(1)


def run(circuit):
    backend_options = {
        "method": "statevector",
        "precision": "double",
        "max_parallel_threads": 1,
    }

    backend = Aer.get_backend("statevector_simulator")
    backend.set_options(**backend_options)
    job = execute(circuit, backend)
    return job.result()


def first_rotation(circuit, nqubits, angles):
    for k in range(nqubits):
        circuit.rx(angles.pop(), k)
        circuit.rz(angles.pop(), k)


def mid_rotation(circuit, nqubits, angles):
    for k in range(nqubits):
        circuit.rz(angles.pop(), k)
        circuit.rx(angles.pop(), k)
        circuit.rz(angles.pop(), k)


def last_rotation(circuit, nqubits, angles):
    for k in range(nqubits):
        circuit.rz(angles.pop(), k)
        circuit.rx(angles.pop(), k)


def entangler(circuit, pairs):
    for a, b in pairs:
        circuit.cx(a, b)


def build_circuit(nqubits, depth, pairs):
    np.random.seed(42)
    angles = [np.random.rand() for _ in range(1000)]

    circuit = QuantumCircuit(nqubits)
    first_rotation(circuit, nqubits, angles)
    entangler(circuit, pairs)
    for _ in range(depth):
        mid_rotation(circuit, nqubits, angles)
        entangler(circuit, pairs)

    last_rotation(circuit, nqubits, angles)
    return circuit


if __name__ == "__main__":
    import time

    for nqubits in range(4, 26):
        start = time.time()
        pairs = [(i, (i + 1) % nqubits) for i in range(nqubits)]
        circuit = build_circuit(nqubits, 9, pairs)
        res = run(circuit)
        # print(res.get_statevector())
        end = time.time()
        print(f"{nqubits} qubits ... {end - start} elapsed")
