import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

def plot_coupling_graph(proc_config, save_path):
    G = nx.Graph()
    G.add_nodes_from(range(proc_config['num_qubits']))
    G.add_edges_from(proc_config['coupling_map'])
    
    plt.figure(figsize=(6, 5))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_color='#4A90E2', node_size=700, font_color='white', font_weight='bold')
    plt.title(f"Coupling Map: {proc_config['name']}")
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()

def plot_optimization_convergence(history, save_path):
    plt.figure(figsize=(7, 4.5), layout="constrained")
    plt.plot(range(1, len(history) + 1), history, marker='o', color='#8E44AD', linewidth=2, markersize=4)
    plt.title("QAOA Classical Optimization Convergence (COBYLA)")
    plt.xlabel("Iteration")
    plt.ylabel("Expectation Cost <H>")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.savefig(save_path, dpi=300)
    plt.close()

def plot_results_comparison(df_summary, save_path):
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5), layout="constrained")

    axes[0].bar(df_summary['processor'], df_summary['depth'], color=['#3498db', '#2ecc71'])
    axes[0].set_title('Transpiled Circuit Depth')
    axes[0].set_ylabel('Depth')

    axes[1].bar(df_summary['processor'], df_summary['cx_count'], color=['#e74c3c', '#9b59b6'])
    axes[1].set_title('Two-Qubit Gate (CX) Count')
    axes[1].set_ylabel('CX Count')

    axes[2].bar(df_summary['processor'], df_summary['approximation_ratio'], color=['#f1c40f', '#e67e22'])
    axes[2].set_title('Approximation Ratio')
    axes[2].set_ylabel('Ratio')
    axes[2].set_ylim([0, 1.1])

    plt.savefig(save_path, dpi=300)
    plt.close()

def plot_state_distribution(counts_raw, counts_mitigated, opt_bitstr, save_path):
    plt.figure(figsize=(10, 5), layout="constrained")
    
    top_states = sorted(counts_raw.keys(), key=lambda x: counts_raw[x], reverse=True)[:10]
    if opt_bitstr[::-1] not in top_states:
        top_states.append(opt_bitstr[::-1])

    raw_probs = [counts_raw.get(s, 0) / 4096 for s in top_states]
    mit_probs = [counts_mitigated.get(s, 0) / 4096 for s in top_states]

    x = np.arange(len(top_states))
    width = 0.35

    plt.bar(x - width/2, raw_probs, width, label='Noisy Raw', color='#E74C3C')
    plt.bar(x + width/2, mit_probs, width, label='Readout Mitigated', color='#2ECC71')

    plt.xlabel('Measured State (Reversed Bitstring)')
    plt.ylabel('Probability')
    plt.title(f'State Probability Distribution (Optimal State: {opt_bitstr[::-1]})')
    plt.xticks(x, top_states, rotation=45)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.savefig(save_path, dpi=300)
    plt.close()