"""
Plotting module based on qulacs benchmark

Based on: https://github.com/qulacs/benchmark-qulacs
"""
import json
from collections import defaultdict
import pyperf

import matplotlib
import matplotlib.pyplot as plt
import numpy as np


nqubits_list = range(4, 27)
liblist = ["pennylane", "spinoza"]


def load() -> defaultdict:
    res = defaultdict(dict)

    for lib in liblist:
        suite = pyperf.BenchmarkSuite.load(f"./{lib}/results.json")

        for n in nqubits_list:
            bench = suite.get_benchmark(f"qcbm {n}")
            res[lib][n] = bench.median()

    return res


def plot(data: defaultdict) -> None:

    for lib in liblist:
        x, y = zip(*data[lib].items())
        plt.plot(x, y, label=lib)

    plt.xlabel("qubits")
    plt.ylabel("time")
    plt.yscale("log")
    plt.legend()
    plt.tight_layout()
    plt.savefig("images/plot.png", dpi=600)


if __name__ == "__main__":
    plot(load())
