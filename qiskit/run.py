import mkl
import pyperf

mkl.set_num_threads(1)


if __name__ == "__main__":
    setup = """from benchmarks import build_circuit, run
import numpy as np
np.random.seed(42)
"""
    nqubits_list = range(4, 27)
    runner = pyperf.Runner()

    for i in nqubits_list:
        runner.timeit(
            f"qcbm {i}",
            stmt="run(circuit)",
            setup=setup
            + f"\nnqubits = {i}; pairs = [(i, (i + 1) % nqubits) for i in range(nqubits)]; circuit = build_circuit(nqubits, 9, pairs);",
        )
