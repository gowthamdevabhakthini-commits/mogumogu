# mogumogu — Qiskit Fall Fest 2026 Phase 1 Submission

[![Qiskit](https://img.shields.io/badge/Qiskit-1.0%2B-blueviolet)](https://qiskit.org)
[![Track](https://img.shields.io/badge/Track-Quantum%20Optimization-blue)](#)
[![Problem](https://img.shields.io/badge/PS-O3%20Knapsack-green)](#)

## 1. Overview
`mogumogu` is an advanced variational quantum optimization solver for **PS-O3: 0/1 Knapsack Optimization** developed for Qiskit Fall Fest 2026 Phase 1. It implements a complete variational QAOA framework with classical outer-loop optimization (COBYLA), readout error mitigation, hardware mapping onto **Processor A** (5-qubit reference) and **Processor B** (9-qubit heavy-hex baseline), and comparative routing/depth benchmarking.

---

## 2. Mathematical Formulation
The 0/1 Knapsack Problem is mapped into an unconstrained Ising cost Hamiltonian $H$:

$$H = - \sum_{i=0}^{n-1} v_i x_i + P \cdot \max\left(0, \sum_{i=0}^{n-1} w_i x_i - C\right)^2$$

Where $V = [10, 4, 7, 5, 8]$, $W = [5, 3, 4, 2, 6]$, capacity $C = 15$, and penalty weight $P = 12.0$.

---

## 3. Repository Structure
```text
mogumogu/
├── README.md                 # Project documentation and setup guide
├── main.py                   # Master execution and optimization pipeline
├── main.ipynb                # Executable Jupyter notebook wrapper
├── requirements.txt          # Dependencies
├── report.md                 # Technical architectural analysis report
├── processors/               # Processor graph configurations
│   ├── processor_A.json
│   └── processor_B.json
├── src/                      # Source modules
│   ├── problem.py            # Knapsack QUBO & QAOA ansatz builder
│   ├── optimizers.py         # Classical outer-loop COBYLA optimizer
│   ├── mitigation.py         # Readout error matrix mitigator
│   ├── processors.py         # Aer noise simulator builder
│   ├── routing.py            # Transpilation and SABRE routing
│   ├── metrics.py            # Quantitative metrics engine
│   └── visualization.py      # Plotting engine
└── results/                  # Figures and benchmark tables
    ├── tables/
    └── figures/

## 4. Setup & Reproducibility

### Prerequisites
* Python 3.9+
* macOS / Linux / Windows terminal

### Installation & Execution
```bash
# 1. Clone the repository
git clone [https://github.com/gowthamdevabhakthini-commits/mogumogu.git](https://github.com/gowthamdevabhakthini-commits/mogumogu.git)
cd mogumogu

# 2. Setup virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install required dependencies
pip install -r requirements.txt

# 4. Execute the complete automated benchmark pipeline
python main.py