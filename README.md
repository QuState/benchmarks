# Quantum State Simulator Benchmarks

### Requirements

- [Miniconda](https://docs.conda.io/en/main/miniconda.html)

## Run
```bash
# Run pennylane benchmark
cd pennylane && rm -rf env && conda env create -f environment.yml --prefix env
conda activate ./env
python benchmarks.py -o results.json
conda deactivate

# Run spinoza benchmark
cd spinoza && rm -rf env && conda env create -f environment.yml --prefix env
conda activate ./env
python benchmarks.py -o results.json
```
