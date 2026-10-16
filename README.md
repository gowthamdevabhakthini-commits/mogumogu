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
    │   ├── architecture_comparison.csv
    │   └── summary.json
    └── figures/
        ├── processor_A_graph.png
        ├── processor_B_graph.png
        ├── A_vs_B_performance.png
        ├── qaoa_convergence.png
        └── state_distribution.png
```

---

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
```

---

## 5. Empirical Benchmark Results Summary

### Exact Classical Reference Solution
* **Brute-Force Optimal Value:** `26`
* **Optimal Bitstring:** `11110` (Items 0, 1, 2, and 3 selected; total weight = $14 \le 15$)

### Hardware Execution Comparison ($p=1$ QAOA with Readout Mitigation)

| Metric | Processor A (5 Qubits) | Processor B (9 Qubits) | Delta / Impact |
| :--- | :---: | :---: | :--- |
| **Physical Qubits** | 5 | 9 (5 active) | Processor B maps onto a sub-graph of its 9-qubit lattice |
| **Transpiled Circuit Depth** | 60 | 41 | **31.7% depth reduction** on Processor B |
| **Two-Qubit (CX) Gates** | 32 | 26 | **18.75% fewer CNOTs** required on Processor B |
| **Total Gate Operations** | 87 | 81 | 6 fewer total physical gates |
| **Feasibility Rate** | 86.28% | 85.03% | $>85\%$ valid non-overflowing solution states |
| **Optimal Bitstring Prob** | 2.32% | 2.17% | Probability distribution across $2^5 = 32$ basis states |
| **Approximation Ratio** | 0.5906 | 0.5895 | Comparable quality with substantially lower gate overhead |

### Visual Benchmark Figures

| Processor Topologies | Hardware Metrics Comparison |
| :---: | :---: |
| ![Processor Topologies](results/figures/processor_A_graph.png) | ![A vs B Metrics](results/figures/A_vs_B_performance.png) |

| COBYLA Optimization Convergence | Mitigated State Distribution |
| :---: | :---: |
| ![QAOA Convergence](results/figures/qaoa_convergence.png) | ![State Distribution](results/figures/state_distribution.png) |

---

## 6. Key Architectural Insights
1. **Routing Cost Mitigation:** The $ZZ$ interaction terms in the QAOA cost layer require non-nearest-neighbor two-qubit operations. Processor B's heavy-hex-inspired topology permits layout paths with fewer routing operations, lowering the CX gate overhead from 32 to 26.
2. **Circuit Depth Reduction:** Transpiling to Processor B reduces circuit depth from 60 to 41, decreasing exposure to decoherence and gate noise during execution on noisy intermediate-scale quantum (NISQ) systems.
3. **Constraint Feasibility:** Both processor configurations maintain an overall feasibility rate above 85%, confirming the effectiveness of the penalty factor ($P = 12.0$) in constraining optimization within valid capacity bounds.

---

## 7. Team & Acknowledgments

This project was developed for **Qiskit Fall Fest 2026 (Phase 1)**

| Member Name | Institution |
| :--- | :--- | :--- |
| **Meghana Sai** | SRM University-AP |
| **Gowtham Devabhakthini** | IIIT Sri City |
| **Pallavi Bachina** | SRM University-AP |
| **Radhika** | SRM University-AP |
| **Pavan Sai** | SRM University-AP |
| **Likith** | SRM University-AP |