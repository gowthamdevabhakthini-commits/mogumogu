import json
from qiskit.transpiler import CouplingMap
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, ReadoutError

def load_processor_config(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def create_target_backend(proc_config, enable_noise=True):
    cmap = CouplingMap(proc_config['coupling_map'])
    if not enable_noise:
        return AerSimulator(coupling_map=cmap)

    noise_cfg = proc_config['noise']
    noise_model = NoiseModel()

    # Single-qubit gate error
    p1 = noise_cfg['1q_depolarizing']
    err_1q = depolarizing_error(p1, 1)
    noise_model.add_all_qubit_quantum_error(err_1q, ['rz', 'sx', 'x'])

    # Two-qubit gate error
    p2 = noise_cfg['2q_depolarizing']
    err_2q = depolarizing_error(p2, 2)
    noise_model.add_all_qubit_quantum_error(err_2q, ['cx'])

    # Readout error
    p_ro = noise_cfg['readout_error']
    readout_err = ReadoutError([[1 - p_ro, p_ro], [p_ro, 1 - p_ro]])
    noise_model.add_all_qubit_readout_error(readout_err)

    return AerSimulator(coupling_map=cmap, noise_model=noise_model)
