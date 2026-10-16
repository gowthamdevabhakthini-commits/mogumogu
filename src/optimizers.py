import numpy as np
from scipy.optimize import minimize
from qiskit_aer import AerSimulator
from src.problem import KnapsackQUBO, build_qaoa_circuit

class QAOAVariationalOptimizer:
    def __init__(self, qubo: KnapsackQUBO, p=1, shots=2048):
        self.qubo = qubo
        self.p = p
        self.shots = shots
        self.simulator = AerSimulator()
        self.history = []

    def _cost_function(self, params):
        gamma = params[:self.p]
        beta = params[self.p:]
        
        qc = build_qaoa_circuit(self.qubo, gamma, beta)
        result = self.simulator.run(qc, shots=self.shots, seed_simulator=42).result()
        counts = result.get_counts()

        total_cost = 0.0
        for bitstr, count in counts.items():
            rev_bitstr = bitstr[::-1]
            cost, _, _ = self.qubo.get_cost(rev_bitstr)
            total_cost += cost * count

        avg_cost = total_cost / self.shots
        self.history.append(avg_cost)
        return avg_cost

    def optimize(self, maxiter=60):
        # Initial guess for gamma and beta
        init_params = np.random.uniform(0, np.pi, 2 * self.p)
        
        res = minimize(
            self._cost_function,
            init_params,
            method='COBYLA',
            options={'maxiter': maxiter, 'rhobeg': 0.5}
        )
        
        opt_gamma = res.x[:self.p].tolist()
        opt_beta = res.x[self.p:].tolist()
        return opt_gamma, opt_beta, self.history