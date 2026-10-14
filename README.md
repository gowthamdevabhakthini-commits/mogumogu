# mogumogu — Qiskit Fall Fest 2026 Phase 1 Submission

[![Qiskit](https://img.shields.io/badge/Qiskit-1.0%2B-blueviolet)](https://qiskit.org)
[![Track](https://img.shields.io/badge/Track-Quantum%20Optimization-blue)](#)
[![Problem](https://img.shields.io/badge/PS-O3%20Knapsack-green)](#)

## Overview
`mogumogu` is an end-to-end quantum optimization solver designed for **PS-O3: 0/1 Knapsack Optimization** as part of Qiskit Fall Fest 2026 Phase 1. The repository implements a QAOA algorithm, maps it targeting two physical hardware processor models (Processor A & Processor B), and systematically benchmarks routing overhead, circuit depth, gate counts, and solution accuracy under synthetic device noise.

## Repository Structure

mogumogu/
├── README.md                 # Project summary and setup instructions
├── main.py                   # Master execution and benchmarking script
├── main.ipynb                # Executable Jupyter notebook wrapper
├── requirements.txt          # Python dependencies
├── report.md                 # Detailed architectural analysis report
├── processors/               # Topology definitions for A and B
│   ├── processor_A.json
│   └── processor_B.json
├── src/                      # Modular source package
│   ├── problem.py            # Knapsack QUBO & QAOA ansatz builder
│   ├── processors.py         # Backend and synthetic noise configuration
│   ├── routing.py            # Transpilation and routing routines
│   ├── metrics.py            # Performance evaluation metrics
│   └── visualization.py      # Coupling graph and benchmark visualizers
└── results/                  # Exported tables and comparison figures
├── tables/
└── figures/

## Quick Start
1. **Clone the repository:**
   
   git clone [https://github.com/YOUR_USERNAME/mogumogu.git](https://github.com/YOUR_USERNAME/mogumogu.git)
   cd mogumogu
