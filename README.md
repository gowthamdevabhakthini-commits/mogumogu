# mogumogu — Qiskit Fall Fest 2026 Phase 1 Submission

[![Qiskit](https://img.shields.io/badge/Qiskit-1.0%2B-blueviolet)](https://qiskit.org)
[![Track](https://img.shields.io/badge/Track-Quantum%20Optimization-blue)](#)
[![Problem](https://img.shields.io/badge/PS-O3%20Knapsack-green)](#)

## 1. Overview
`mogumogu` is an end-to-end quantum optimization solver designed for **PS-O3: 0/1 Knapsack Optimization** as part of Qiskit Fall Fest 2026 Phase 1. The repository implements a Quantum Approximate Optimization Algorithm (QAOA) framework, maps the circuit to two target physical hardware topology models (**Processor A** with 5 qubits and **Processor B** with 9 qubits), and systematically evaluates routing overhead, circuit depth, gate counts, and solution accuracy under synthetic device noise.

---

## 2. Problem Statement & Mathematical Formulation
The 0/1 Knapsack Problem seeks to select a subset of items to maximize total value while remaining within a maximum capacity constraint.

### Problem Instance Details
* **Item Values ($V$):** $[10, 4, 7, 5, 8]$
* **Item Weights ($W$):** $[5, 3, 4, 2, 6]$
* **Capacity ($C$):** $15$
* **Number of Items ($n$):** $5$

### QUBO Mapping
The constrained optimization problem is mapped into an unconstrained Ising cost Hamiltonian $H$:

$$H = - \sum_{i=0}^{n-1} v_i x_i + P \cdot \max\left(0, \sum_{i=0}^{n-1} w_i x_i - C\right)^2$$

Where $x_i \in \{0, 1\}$ indicates item selection, and $P = 12.0$ serves as the quadratic penalty weight enforcing weight boundary compliance. Converting binary variables via $x_i = \frac{1 - Z_i}{2}$ yields single-body $Z_i$ linear terms and two-body $Z_i Z_j$ interaction pairs.

---

## 3. Repository Structure
```text
mogumogu/
├── README.md                 # Project documentation and reproduction guide
├── main.py                   # Master execution and benchmarking pipeline
├── main.ipynb                # Executable Jupyter notebook wrapper
├── requirements.txt          # Pinned Python dependencies
├── report.md                 # Technical architectural analysis report
├── processors/               # Participant-defined processor graph definitions
│   ├── processor_A.json      # 5-qubit reference topology
│   └── processor_B.json      # 9-qubit heavy-hex baseline topology
├── src/                      # Modular python source package
│   ├── problem.py            # Knapsack QUBO & QAOA circuit builder
│   ├── processors.py         # Processor configuration & Aer noise loader
│   ├── routing.py            # Transpilation and routing engine
│   ├── metrics.py            # Quantitative metrics extraction
│   └── visualization.py      # Coupling visualizer & comparison plotting
└── results/                  # Generated benchmark tables and figures
    ├── tables/
    │   ├── architecture_comparison.csv
    │   └── summary.json
    └── figures/
        ├── processor_A_graph.png
        ├── processor_B_graph.png
        └── A_vs_B_performance.png

4. Setup & ReproducibilityPrerequisitesPython 3.9+Recommended: Virtual environment (venv)Installation & ExecutionBash# Clone the repository
git clone [https://github.com/YOUR_USERNAME/mogumogu.git](https://github.com/YOUR_USERNAME/mogumogu.git)
cd mogumogu

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required dependencies
pip install -r requirements.txt

# Execute the complete automated benchmark pipeline
python main.py
5. Empirical Benchmark Results
Exact Classical Solution
Brute-Force Optimal Value: 26
Optimal Bitstring: 11110 (Items 0, 1, 2, and 3 selected; total weight = $14 \le 15$)
Hardware Execution Comparison ($p=1$ QAOA under Synthetic Noise)

Metric                  | Processor A (5 Qubits) | Processor B (9 Qubits) | Delta / Impact
Physical Qubits         | 5                      | 9 (5 active)           | Processor B utilizes a sub-graph of its 9-qubit lattice
Transpiled Circuit Depth| 60                     | 41                     | 31.7% depth reduction on Processor B
Two-Qubit (CX) Gates    | 32                     | 26                     | 18.75% fewer CNOTs required on Processor B
Total Gate Operations   | 87                     | 81                     | 6 fewer total physical gates
Feasibility Rate        | 86.28%                 | 85.03%                 | >85\% valid non-overflowing solution states
Optimal Bitstring Prob  | 2.32%                  | 2.17%                  | Probability distribution across $2^5 = 32$ basis states
Approximation Ratio     | 0.5906                 | 0.5895                 | Comparable quality with substantially lower gate overhead

6. Key Architectural Insights

Routing Cost Mitigation: The $ZZ$ interaction terms in the QAOA cost layer require non-nearest-neighbor two-qubit operations. Processor B's heavy-hex-inspired topology permits layout paths with fewer routing operations, lowering the CX gate overhead from 32 to 26.

Circuit Depth Reduction: Transpiling to Processor B reduces circuit depth from 60 to 41, decreasing exposure to decoherence and gate noise during execution on noisy intermediate-scale quantum (NISQ) systems.

Constraint Feasibility: Both processor configurations maintain an overall feasibility rate above 85%, confirming the effectiveness of the penalty factor ($P = 12.0$) in constraining optimization within valid capacity bounds.