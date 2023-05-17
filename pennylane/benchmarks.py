import mkl
import pyperf

mkl.set_num_threads(1)


if __name__ == "__main__":
    setup="""
import pennylane as qml
import numpy as np

class QCBM:
    def __init__(self, n, nlayers, dev="lightning.qubit"):
        self.n = n
        self.nlayers = nlayers
        self.neighbors = [(i, (i + 1) % n) for i in range(n)]
        self.dev = qml.device(dev, wires=n)
        self.operations = []

    def __call__(self, vars):
        def apply_qcbm_circuit(vars):
            self.first_layer(vars[1])
            for each in vars[2:-2]:
                self.entangler()
                self.mid_layer(each)

            self.entangler()
            self.last_layer(vars[-1])

            self.dev.apply(self.operations)

        return apply_qcbm_circuit(vars)

    def generate_random_vars(self):
        vars = [np.random.rand(self.n, 2)]
        vars += [np.random.rand(self.n, 3) for _ in range(self.n - 2)]
        vars += [np.random.rand(self.n, 2)]
        return vars

    def first_rotation(self, alpha, beta, wires=1):
        self.operations.append(qml.RX(alpha, wires=wires))
        self.operations.append(qml.RZ(beta, wires=wires))

    def mid_rotation(self, alpha, beta, gamma, wires=1):
        self.operations.append(qml.RZ(alpha, wires=wires))
        self.operations.append(qml.RX(beta, wires=wires))
        self.operations.append(qml.RZ(gamma, wires=wires))

    def last_rotation(self, alpha, beta, wires=1):
        self.operations.append(qml.RX(alpha, wires=wires))
        self.operations.append(qml.RZ(beta, wires=wires))

    def first_layer(self, vars):
        for each in vars:
            self.first_rotation(each[0], each[1])

    def mid_layer(self, vars):
        for each in vars:
            self.mid_rotation(each[0], each[1], each[2])

    def last_layer(self, vars):
        for each in vars:
            self.last_rotation(each[0], each[1])

    def entangler(self):
        for i, j in self.neighbors:
            self.operations.append(qml.CNOT(wires=[i, j]))
"""

    runner = pyperf.Runner()

    for i in range(4, 26):
        runner.timeit(f"qcbm {i}", stmt='qcbm(vars)', setup=setup+f"n = {i}; qcbm = QCBM(n, 9); vars = qcbm.generate_random_vars();")
