# Quantum State Simulator Benchmarks

We benchmark several popular quantum computation
softwares/frameworks/simulators to test their performance in practical daily
research.

## Results

### Requirements

- [Conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html?highlight=conda)

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
