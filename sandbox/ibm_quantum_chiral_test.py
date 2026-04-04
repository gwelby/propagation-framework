"""
ibm_quantum_chiral_test.py
IBM submission helper for the chiral Z3 walk.

Test: 3-step CHIRAL walk (pure shift) vs 3-step SYMMETRIC walk (mixing).
Prediction: The Chiral walk restores the initial state perfectly (H=0),
while the Symmetric walk (from d71nqomqdfbc73d13fpg) maximizes mixing.

Physical basis:
  - 2 qubits encode 3 channels: |00>, |01>, |10>
  - Chiral shift: |00> -> |01>, |01> -> |10>, |10> -> |00>
  - After 3 steps, T_chiral^3 = I exactly.
"""
import os

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.quantum_info import Operator
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

def build_chiral_circuit():
    qr = QuantumRegister(2, 'q')
    cr = ClassicalRegister(2, 'c')
    qc = QuantumCircuit(qr, cr)

    # 1. Initialize in |00> (Channel 0)
    # 2. Apply Chiral Shift 3 times
    # A pure chiral shift is a permutation matrix
    P_chiral = np.array([
        [0, 0, 1, 0],
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1] # |11> stays |11>
    ])
    shift_gate = Operator(P_chiral)

    for _ in range(3):
        qc.unitary(shift_gate, qr, label='ChiralShift')

    qc.measure(qr, cr)
    return qc

def run_chiral_test():
    print("=======================================================")
    print("  EXPERIMENT 6: QUANTUM PROOF OF CHIRALITY")
    print("  Comparing Pure Shift to Symmetric Mixing")
    print("=======================================================\n")

    qc = build_chiral_circuit()
    print("Chiral Circuit Built:")
    print(qc.draw(output='text'))

    # Local exact check before any hardware submission.
    init = np.array([1.0, 0.0, 0.0, 0.0], dtype=complex)
    p_chiral = np.array([
        [0, 0, 1, 0],
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
    ], dtype=complex)
    final = np.linalg.matrix_power(p_chiral, 3) @ init
    probs = np.abs(final) ** 2
    print(f"\nLocal exact prediction: P(|00>)={probs[0]:.6f}, P(|01>)={probs[1]:.6f}, P(|10>)={probs[2]:.6f}, P(|11>)={probs[3]:.6f}")

    print("\nConnecting to IBM Quantum (ibm_fez 156q)...")
    try:
        token = os.environ.get("IBM_QUANTUM_TOKEN")
        if not token:
            raise RuntimeError("IBM_QUANTUM_TOKEN is not set")

        service = QiskitRuntimeService(channel="ibm_quantum_platform", token=token)
        backend_name = os.environ.get("IBM_BACKEND", "ibm_fez")
        backend = service.backend(backend_name)

        sampler = Sampler(backend)
        qc_transpiled = transpile(qc, backend=backend)

        job = sampler.run([qc_transpiled], shots=8192)
        print(f"  Chiral Job Submitted: {job.job_id()}")
        print(f"  Job d71nqomqdfbc73d13fpg (Symmetric) is already in queue.")
        print(f"  Backend: {backend_name}")
        print("\nPrediction: Chiral job should strongly favor |00> (identity preservation), modulo hardware noise and leakage.")
        print("Symmetric job should spread weight across |00>, |01>, |10| with much higher entropy.")
        print("Audit with: python sandbox/ibm_quantum_result_audit.py --mode chiral --counts '{...}'")

    except Exception as e:
        print(f"  IBM connection error: {e}")
        print("  Submission skipped. Local exact prediction above is still valid.")

if __name__ == "__main__":
    run_chiral_test()
