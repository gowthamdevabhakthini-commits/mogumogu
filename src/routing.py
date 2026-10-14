from qiskit import transpile
from qiskit.transpiler import CouplingMap

def transpile_for_processor(circuit, proc_config, optimization_level=1, seed=42):
    cmap = CouplingMap(proc_config['coupling_map'])
    compiled_circuit = transpile(
        circuit,
        coupling_map=cmap,
        basis_gates=proc_config['basis_gates'],
        optimization_level=optimization_level,
        seed_transpiler=seed
    )
    return compiled_circuit
