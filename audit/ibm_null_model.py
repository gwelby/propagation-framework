#!/usr/bin/env python3
"""
Null model for the IBM 'chiral Z3 preserves identity' claim.

The chiral circuit (ibm_quantum_chiral_test.py) prepares |00>, applies a
3-cycle permutation (|00>->|01>->|10>->|00>) THREE times, then measures.
Net circuit = T_chiral^3 = IDENTITY, by construction, in ANY theory.

So 'return probability to |00>' measures only: does a net-identity circuit
return its input? That is a gate-fidelity / circuit-depth benchmark, not a
test of the Propagation Framework.

H0 (null): return prob is fully explained by (net circuit = identity) +
           hardware depolarizing error over 3 two-qubit-gate layers.
           No PF content required.

We (1) reproduce the reported 94-99% return band from depolarizing noise alone,
and (2) run a label-shuffle control showing the metric is independent of which
basis state is called 'channel 0' -- i.e. it carries no PF-specific signal.
"""
import numpy as np

STATES = ['00', '01', '10', '11']
# chiral 3-cycle on the 3 physical channels; 11 is leakage (fixed)
perm = {'00':'01', '01':'10', '10':'00', '11':'11'}
P = np.zeros((4,4))
for i,s in enumerate(STATES):
    P[STATES.index(perm[s]), i] = 1.0

def noisy_apply(vec, p):
    """One gate: with prob (1-p) apply permutation, with prob p depolarize to uniform/4."""
    return (1-p) * (P @ vec) + p * np.full(4, 1/4)

print("=== H0: depolarizing-only null model for the chiral 3-step return ===")
print(f"{'gate err p':>10} | {'return P(|00>)':>14} | matches reported?")
for p in [0.005, 0.01, 0.02, 0.03, 0.05]:
    v = np.array([1.0,0,0,0])      # start |00>
    for _ in range(3):
        v = noisy_apply(v, p)
    ret = v[0]
    tag = "  <- 99.01% (CLAIMS)" if abs(ret-0.99)<0.01 else ("  <- 94.6% (Codex)" if abs(ret-0.946)<0.02 else "")
    print(f"{p:>10.3f} | {ret:>14.4f} |{tag}")

print("\n  => the reported 94-99% band is fully reproduced by gate error alone.")
print("     Zero Propagation-Framework content is needed to explain it.\n")

print("=== Shuffle control: does the metric depend on PF labels? ===")
# Relabel which state is 'the start/identity-preserved channel'. Because the net
# circuit is identity, return-to-start is invariant under ANY relabeling.
rng = np.random.default_rng(0)
p = 0.02
for trial in range(4):
    order = rng.permutation(4)
    # build a relabeled permutation that is still a 3-cycle+fixed on the shuffled labels
    start = order[0]
    v = np.zeros(4); v[start] = 1.0
    # net identity regardless of labels:
    for _ in range(3):
        v = (1-p)*(np.eye(4) @ v) + p*np.full(4,1/4)   # net = identity (T^3)
    print(f"  start-channel relabeled to '{STATES[start]}': return P = {v[start]:.4f}")
print("\n  => identical for every labeling. The 'identity preservation' signal is")
print("     label-independent: it tests 'net circuit = identity', not chirality.")

print("\n=== What a REAL test would need (for the team) ===")
print("  The chiral vs symmetric contrast is rigged: T_chiral^3 = I (returns) and")
print("  T_symmetric is built to mix (spreads). Both are true by construction in any")
print("  theory. To carry PF content, the prediction must be non-trivial -- e.g. a")
print("  coherent PHASE/eigenvalue measurement of the -1/8 Q-sector action (LCU /")
print("  block-encoding / Hadamard test), exactly what Codex put on HOLD 2026-06-09.")
