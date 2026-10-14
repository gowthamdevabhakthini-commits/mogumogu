# Phase 1 Architectural Analysis Report
**Project Name:** mogumogu  
**Track:** Quantum Optimization  
**Problem Statement:** PS-O3: 0/1 Knapsack Problem  

## 1. Executive Summary
This report evaluates the algorithmic performance and hardware mapping trade-offs for solving a 5-item 0/1 Knapsack Problem using QAOA ($p=1$) across two distinct quantum architectures: Processor A (5-qubit linear/tree reference) and Processor B (9-qubit heavy-hex baseline).

## 2. Problem & QUBO Formulation
Given item values $V = [10, 4, 7, 5, 8]$, weights $W = [5, 3, 4, 2, 6]$, and capacity $C = 15$, the objective is mapped into an Ising Hamiltonian:
$$H = - \sum_{i=0}^4 v_i x_i + P \cdot \max\left(0, \sum_{i=0}^4 w_i x_i - C\right)^2$$
Brute-force classical verification confirms the exact optimum selection as items $\{0, 1, 2, 3\}$ (`11110` bitstring) yielding a maximum value of **26** with total weight **14**.

## 3. Comparative Architecture Analysis

| Metric | Processor A (5 Qubits) | Processor B (9 Qubits) | Difference / Impact |
| :--- | :--- | :--- | :--- |
| **Physical Qubits Used** | 5 | 9 (5 active) | Processor B utilizes a sub-graph of its 9-qubit lattice |
| **Circuit Depth** | 60 | 41 | Processor B achieves 31.7% lower circuit depth |
| **CX Gate Count** | 32 | 26 | Processor B requires 18.75% fewer CNOT gates |
| **Total Gates** | 87 | 81 | Processor B reduces total gate count by 6 |
| **Feasibility Rate** | 86.28% | 85.03% | Both architectures enforce constraint bounds effectively |
| **Optimal Bitstring Prob** | 2.32% | 2.17% | Output probability distribution across $2^5 = 32$ states |
| **Approximation Ratio** | 0.5906 | 0.5895 | Comparable solution quality with lower gate depth on B |

## 4. Key Architectural Insights
1. **Routing Overhead:** Processor A's branching tree topology forces additional routing operations to implement non-nearest-neighbor quadratic interaction terms $Z_i Z_j$.
2. **Noise Accumulation:** Under the synthetic noise model ($p_{CX} = 0.5\%$), the extra 6 CNOT gates on Processor A increase depth and decoherence exposure.
3. **Heavy-Hex Advantage:** Processor B's sparse heavy-hex lattice provides shorter effective path lengths for all-to-all logical QUBO interactions, reducing transpiled circuit depth from 60 to 41.