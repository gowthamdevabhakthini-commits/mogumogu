import json
import pandas as pd
import nbformat as nbf
from src.problem import KnapsackQUBO, build_qaoa_circuit
from src.optimizers import QAOAVariationalOptimizer
from src.mitigation import ReadoutMitigator
from src.processors import load_processor_config, create_target_backend
from src.routing import transpile_for_processor
from src.metrics import extract_circuit_metrics, evaluate_execution_results
from src.visualization import (
    plot_coupling_graph, 
    plot_optimization_convergence, 
    plot_results_comparison, 
    plot_state_distribution
)

def run_pipeline():
    print("=== [1/6] Initializing PS-O3 0/1 Knapsack Instance ===")
    values = [10, 4, 7, 5, 8]
    weights = [5, 3, 4, 2, 6]
    capacity = 15
    qubo = KnapsackQUBO(values, weights, capacity, penalty_factor=12.0)
    
    print(f"Classical Exact Optimum Value: {qubo.classical_opt_val}")
    print(f"Classical Exact Optimum Bitstring: {qubo.classical_opt_bitstring}")

    print("\n=== [2/6] Running Classical Outer-Loop QAOA Optimization (COBYLA) ===")
    optimizer = QAOAVariationalOptimizer(qubo, p=1, shots=2048)
    opt_gamma, opt_beta, history = optimizer.optimize(maxiter=50)
    print(f"Optimized Gamma: {opt_gamma}")
    print(f"Optimized Beta:  {opt_beta}")

    plot_optimization_convergence(history, "results/figures/qaoa_convergence.png")

    print("\n=== [3/6] Building Optimized QAOA Circuit ===")
    logical_circuit = build_qaoa_circuit(qubo, gamma=opt_gamma, beta=opt_beta)

    print("\n=== [4/6] Benchmarking Target Processors & Applying Readout Mitigation ===")
    proc_A_cfg = load_processor_config("processors/processor_A.json")
    proc_B_cfg = load_processor_config("processors/processor_B.json")

    plot_coupling_graph(proc_A_cfg, "results/figures/processor_A_graph.png")
    plot_coupling_graph(proc_B_cfg, "results/figures/processor_B_graph.png")

    mitigator = ReadoutMitigator(readout_error_rate=0.01, num_qubits=5)
    results_list = []

    for proc_cfg in [proc_A_cfg, proc_B_cfg]:
        name = proc_cfg['name']
        print(f"\n--- Benchmarking on {name} ---")

        compiled_qc = transpile_for_processor(logical_circuit, proc_cfg, optimization_level=1, seed=42)
        c_metrics = extract_circuit_metrics(compiled_qc)

        backend = create_target_backend(proc_cfg, enable_noise=True)
        job = backend.run(compiled_qc, shots=4096, seed_simulator=42)
        counts_raw = job.result().get_counts()

        # Apply Readout Error Mitigation
        counts_mitigated = mitigator.mitigate_counts(counts_raw, shots=4096)
        e_metrics = evaluate_execution_results(counts_mitigated, qubo, shots=4096)

        combined = {"processor": name, **c_metrics, **e_metrics}
        results_list.append(combined)

        if name == "Processor_B":
            plot_state_distribution(
                counts_raw, 
                counts_mitigated, 
                qubo.classical_opt_bitstring, 
                "results/figures/state_distribution.png"
            )

    print("\n=== [5/6] Exporting Final Summary Tables & Figures ===")
    df_results = pd.DataFrame(results_list)
    df_results.to_csv("results/tables/architecture_comparison.csv", index=False)
    
    with open("results/tables/summary.json", "w") as f:
        json.dump(results_list, f, indent=2)

    plot_results_comparison(df_results, "results/figures/A_vs_B_performance.png")
    print("\nEmpirical Summary Table:")
    print(df_results.to_string(index=False))

    print("\n=== [6/6] Regenerating main.ipynb Notebook ===")
    create_notebook()
    print("Pipeline execution complete! All artifacts saved to results/")

def create_notebook():
    nb = nbf.v4.new_notebook()
    nb.cells = [
        nbf.v4.new_markdown_cell("# Qiskit Fall Fest 2026 - Phase 1 Solution: PS-O3 Knapsack Optimization"),
        nbf.v4.new_code_cell("""
from src.problem import KnapsackQUBO, build_qaoa_circuit
from src.optimizers import QAOAVariationalOptimizer
from src.processors import load_processor_config
from src.routing import transpile_for_processor

qubo = KnapsackQUBO(values=[10, 4, 7, 5, 8], weights=[5, 3, 4, 2, 6], capacity=15)
optimizer = QAOAVariationalOptimizer(qubo, p=1)
opt_gamma, opt_beta, _ = optimizer.optimize(maxiter=30)

logical_qc = build_qaoa_circuit(qubo, gamma=opt_gamma, beta=opt_beta)

proc_A = load_processor_config("processors/processor_A.json")
proc_B = load_processor_config("processors/processor_B.json")

qc_A = transpile_for_processor(logical_qc, proc_A)
qc_B = transpile_for_processor(logical_qc, proc_B)

print("Processor A Depth:", qc_A.depth(), "| CX Count:", qc_A.count_ops().get('cx', 0))
print("Processor B Depth:", qc_B.depth(), "| CX Count:", qc_B.count_ops().get('cx', 0))
""")
    ]
    with open("main.ipynb", "w") as f:
        nbf.write(nb, f)

if __name__ == "__main__":
    run_pipeline()