import matplotlib.pyplot as plt
import networkx as nx

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

def plot_results_comparison(df_summary, save_path):
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

    # Circuit Depth
    axes[0].bar(df_summary['processor'], df_summary['depth'], color=['#3498db', '#2ecc71'])
    axes[0].set_title('Transpiled Circuit Depth')
    axes[0].set_ylabel('Depth')

    # CX Count
    axes[1].bar(df_summary['processor'], df_summary['cx_count'], color=['#e74c3c', '#9b59b6'])
    axes[1].set_title('Two-Qubit Gate (CX) Count')
    axes[1].set_ylabel('CX Count')

    # Approximation Ratio
    axes[2].bar(df_summary['processor'], df_summary['approximation_ratio'], color=['#f1c40f', '#e67e22'])
    axes[2].set_title('Approximation Ratio')
    axes[2].set_ylabel('Ratio')
    axes[2].set_ylim([0, 1.1])

    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()
