def extract_circuit_metrics(compiled_circuit):
    ops = compiled_circuit.count_ops()
    depth = compiled_circuit.depth()
    cx_count = ops.get('cx', 0)
    swap_count = ops.get('swap', 0)
    total_gates = sum(ops.values())
    num_qubits = compiled_circuit.num_qubits
    return {
        "depth": depth,
        "cx_count": cx_count,
        "swap_count": swap_count,
        "total_gates": total_gates,
        "physical_qubits": num_qubits
    }

def evaluate_execution_results(counts, qubo, shots=4096):
    total_valid_shots = 0
    total_weighted_value = 0.0
    optimal_shots = 0
    opt_bitstring = qubo.classical_opt_bitstring

    for bitstr, count in counts.items():
        rev_bitstr = bitstr[::-1]
        cost, value, is_valid = qubo.get_cost(rev_bitstr)

        if is_valid:
            total_valid_shots += count
            total_weighted_value += value * count

        if rev_bitstr == opt_bitstring:
            optimal_shots += count

    feasibility_rate = total_valid_shots / shots
    opt_probability = optimal_shots / shots
    expected_value = (total_weighted_value / total_valid_shots) if total_valid_shots > 0 else 0.0
    approximation_ratio = expected_value / qubo.classical_opt_val if qubo.classical_opt_val > 0 else 0.0

    return {
        "feasibility_rate": feasibility_rate,
        "optimal_bitstring_prob": opt_probability,
        "expected_value": expected_value,
        "approximation_ratio": approximation_ratio
    }