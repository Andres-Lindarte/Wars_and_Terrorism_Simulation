# Wars and Terrorism Simulation
### Guerrilla Warfare Simulation & Statistical Analysis Pipeline

An automated computational framework designed to simulate force fragmentation and combination dynamics in guerrilla warfare and terrorism models. The pipeline executes C++ simulations, parses time-series state data, calculates the steady-state mean ($\mu$) and unbiased sample standard deviation ($\sigma$) of the power-law exponent ($\alpha$), and generates visualization figures using Python.


## Project Overview

This repository models the dynamics of insurgent and guerrilla force sizes governed by two primary competing stochastic mechanisms:

1. **Fragmentation ($\nu$):** An attack unit breaks down into basic constituent force units ($S_i = 1$).
2. **Combination ($1 - \nu$):** Two distinct attack units merge their force strengths ($S_i + S_j$).

The system reaches a stationary state where the size distribution follows a power-law behavior. The main objective of this automated pipeline is to:

* Execute dynamic simulations over a parameter space of probabilities ($\nu$), total iterations ($T$), and random seeds.
* Calculate the steady-state average of $\alpha$ in C++ during the final 10% of the simulation run and output it directly to the terminal.
* Measure the aggregate statistical exponent $\alpha = \mu \pm \sigma$ across multiple seeds in Python.
* Generate time-series and log-log cumulative distribution plots saved as vector PDFs.

---

## Repository Structure

```text
.
├── code/
│   ├── simulation.cpp              # C++ Monte Carlo simulation engine (calculates alpha & prints state/terminal summary)
│   ├── simulation.x                # Compiled C++ executable binary
│   ├── protocole_of_simulation.py  # Python launcher script (compiles & loops over parameter protocol)
│   ├── protocole_parallelized.py   # Python launcher script (compiles & loops over parameter protocol) parallelized over the cores of the CPU.
│   └── plotting.py                 # Multi-panel analysis script (calculates µ ± σ and plots Figure 1 & 2)
├── data/                           # Generated simulation data files (master_data_v_T_seed.txt)
├── results/                        # Exported plot PDFs (ALPHA.pdf, LOG_DISTRIBUTION.pdf)
└── README.md                       # Project documentation
```

---

## Requirements & Dependencies

### C++ Compiler
* **Standard:** C++20 or later
* **Compiler:** `g++` or `clang++` with optimization flags (`-O3`)

### Python Environment
* Python 3.8+
* Required libraries:
  ```bash
  pip install numpy matplotlib scikit-learn scipy
  ```
* Or use requirements.txt to install all in one go:
  ```bash
  pip install -r requirements.txt
  ```
---

## Execution & Pipeline Workflow

### 1. Manual C++ Execution
You can compile and run a single simulation run directly from the terminal (from the main folder):

```bash
# Compilation
g++ -std=c++20 code/simulation.cpp -o code/simulation.x -O3

# Execution syntax: ./simulation.x [N] [v] [T] [SEED]
./simulation.x 10000 0.01 5000000 42
```

* **Terminal Output:** Displays a progress bar, run time, and the **Average value of alpha (in the last 10%)** for that specific run.
* **Data Output:** Writes step data every 1000 iterations to `data/master_data_v_T_seed.txt`.

### 2. Full Protocol Execution
To compile C++, run all parameter combinations ($\nu \in \{0.01, 0.069, 0.1\}$, $T \in \{1000000, 2500000, 5000000\}$, seeds $\in \{42, 69, 911\}$), and generate final graphics automatically:

```bash
python3 code/protocole_of_simulation.py
```
Or it can be run independentlly over the cores of the CPU, for a faster excecution of the protocole:
```bash
python3 code/protocole_parallelized.py
```

### 3. Isolated Plotting Scripts
* **`code/plotting.py`:** Reads all files in `data/`, groups by parameter combinations ($\nu, T$), calculates $\mu \pm \sigma$ over the last 10% of steps across seeds, and generates multi-panel figures saved in `results/`.

---

## Output Visualizations

The main script `plotting.py` generates two primary figures saved in `results/`:

1. **`ALPHA.pdf` (Time Evolution):** Plots the trajectory of exponent $\alpha(t)$ at maximum time ($T$) across different fragmentation probabilities ($\nu$). Subplot titles explicitly show $\nu$, $T$, and $\alpha = \mu \pm \sigma$.
2. **`LOG_DISTRIBUTION.pdf` (Log-Log Distribution):** Plots $\ln(\text{Cumulative Frequency})$ vs. $\ln(S)$ for different $T$ values with linear regression fits and statistics formatted in the subplot headers.

---

## Mathematical Methodology

### Power-Law Exponent ($\alpha$)
The cumulative probability distribution $P(X \ge S)$ follows:

$$P(X \ge S) \propto S^{1 - \alpha}$$

Taking the natural logarithm:

$$\ln(P(X \ge S)) = (1 - \alpha) \ln(S) + C$$

The power-law exponent $\alpha$ is derived from the slope $m$ of the linear regression fit on the cumulative distribution:

$$\alpha = 1 - m$$

### Steady-State Statistics ($\mu \pm \sigma$)
For each combination of parameters $(\nu, T)$ across $N_s$ random seeds, taking the last 10 samples per run yields a sample set of size $N = 10 \times N_s$. The sample mean ($\mu$) and unbiased sample standard deviation ($\sigma$) are calculated as:

$$\mu = \frac{1}{N} \sum_{i=1}^{N} \alpha_i, \qquad \sigma = \sqrt{\frac{1}{N - 1} \sum_{i=1}^{N} (\alpha_i - \mu)^2}$$

---

## Contact & Attribution
Developed for computational physics research, complex systems analysis, and statistical modeling of guerrilla warfare dynamics.
