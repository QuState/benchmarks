# Quantum State Simulator Benchmarks

### Requirements

- [Miniconda](https://docs.conda.io/en/main/miniconda.html)


## Run
```bash
# Run pennylane benchmark
cd pennylane && rm -rf env && conda env create -f environment.yml --prefix env
conda activate ./env
python run.py -o results.json
conda deactivate

# Run spinoza benchmark
cd spinoza && rm -rf env && conda env create -f environment.yml --prefix env
conda activate ./env
python run.py -o results.json
conda deactivate

# Run qiskit benchmark
cd qiskit && rm -rf env && conda env create -f environment.yml --prefix env
conda activate ./env
python run.py -o results.json
conda deactivate
```

## Visualize results
To plot the results run the plot.py script.
Ensure that the libraries you would like to include are listed on line 16.


## Additional notes
If you are unable to install the `mkl` package on your machine (M2 mac), you can set the single-thread limit single-thread environment variables by adding the following code to the beginning of the respective Python script:

```python
import os
nthreads = 1
os.environ["OMP_NUM_THREADS"] = str(nthreads)
os.environ["OPENBLAS_NUM_THREADS"] = str(nthreads)
os.environ["MKL_NUM_THREADS"] = str(nthreads)
```
