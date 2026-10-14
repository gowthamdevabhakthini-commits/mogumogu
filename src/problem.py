import numpy as np
from qiskit import QuantumCircuit

class KnapsackQUBO:
    def __init__(self, values, weights, capacity, penalty_factor=10.0):
        self.values = np.array(values)
        self.weights = np.array(weights)
        self.capacity = capacity
        self.penalty = penalty_factor
        self.num_items = len(values)
        self.classical_opt_val, self.classical_opt_bitstring = self._brute_force_solve()

    def _brute_force_solve(self):
        best_val = -1
        best_bitstring = ""
        for i in range(2**self.num_items):
            bitstr = format(i, f'0{self.num_items}b')
            x = np.array([int(b) for b in bitstr])
            w_total = np.dot(self.weights, x)
            v_total = np.dot(self.values, x)
            if w_total <= self.capacity and v_total > best_val:
                best_val = v_total
                best_bitstring = bitstr
        return best_val, best_bitstring

    def get_cost(self, bitstring):
        x = np.array([int(b) for b in bitstring])
        w_total = np.dot(self.weights, x)
        v_total = np.dot(self.values, x)
        overflow = max(0, w_total - self.capacity)
        cost = -v_total + self.penalty * (overflow ** 2)
        return cost, v_total, w_total <= self.capacity

    def qubo_parameters(self):
        # Convert x_i -> (1 - Z_i) / 2
        h = np.zeros(self.num_items)
        J = np.zeros((self.num_items, self.num_items))
        
        # Linear terms from value: - v_i * (1 - Z_i)/2
        for i in range(self.num_items):
            h[i] += 0.5 * self.values[i]
            
        # Quadratic penalty: P * (sum w_i (1-Z_i)/2 - Capacity)^2
        # = P * [ (sum w_i/2 - C) - sum (w_i/2) Z_i ]^2
        const_offset = np.sum(self.weights) / 2.0 - self.capacity
        for i in range(self.num_items):
            h[i] += self.penalty * const_offset * self.weights[i]
            for j in range(i + 1, self.num_items):
                J[i, j] += 0.5 * self.penalty * self.weights[i] * self.weights[j]
        return h, J

def build_qaoa_circuit(qubo: KnapsackQUBO, gamma: float, beta: float) -> QuantumCircuit:
    n = qubo.num_items
    qc = QuantumCircuit(n, n)
    h, J = qubo.qubo_parameters()

    # Initial state preparation: equal superposition
    qc.h(range(n))

    # Phase Separator (Cost Hamiltonian U_C)
    for i in range(n):
        if abs(h[i]) > 1e-6:
            qc.rz(2 * gamma * h[i], i)

    for i in range(n):
        for j in range(i + 1, n):
            if abs(J[i, j]) > 1e-6:
                qc.cx(i, j)
                qc.rz(2 * gamma * J[i, j], j)
                qc.cx(i, j)

    # Mixer Hamiltonian (U_B)
    for i in range(n):
        qc.rx(2 * beta, i)

    qc.measure(range(n), range(n))
    return qc
