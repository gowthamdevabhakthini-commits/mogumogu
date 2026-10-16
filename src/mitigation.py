import numpy as np

class ReadoutMitigator:
    def __init__(self, readout_error_rate=0.01, num_qubits=5):
        self.p_ro = readout_error_rate
        self.n = num_qubits
        self.cal_matrix = self._build_calibration_matrix()
        self.inv_matrix = np.linalg.inv(self.cal_matrix)

    def _build_calibration_matrix(self):
        # 1-qubit response matrix
        A1 = np.array([[1 - self.p_ro, self.p_ro],
                       [self.p_ro, 1 - self.p_ro]])
        
        # Tensor product for n-qubit matrix
        A = A1
        for _ in range(self.n - 1):
            A = np.kron(A, A1)
        return A

    def mitigate_counts(self, raw_counts, shots=4096):
        num_states = 2**self.n
        raw_vec = np.zeros(num_states)

        for bitstr, count in raw_counts.items():
            idx = int(bitstr, 2)
            raw_vec[idx] = count / shots

        mitigated_vec = np.dot(self.inv_matrix, raw_vec)
        # Clip negative probabilities and re-normalize
        mitigated_vec = np.clip(mitigated_vec, 0, None)
        if np.sum(mitigated_vec) > 0:
            mitigated_vec /= np.sum(mitigated_vec)

        mitigated_counts = {}
        for idx, prob in enumerate(mitigated_vec):
            if prob > 1e-4:
                bitstr = format(idx, f'0{self.n}b')
                mitigated_counts[bitstr] = int(round(prob * shots))

        return mitigated_counts