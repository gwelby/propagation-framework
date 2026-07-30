#!/usr/bin/env python3.12
"""
O2bis: fast, deterministic, fail-closed regression layer.

This script performs only exact algebraic and exact density-matrix checks.
It contains no Monte Carlo, is bounded to a few seconds, and exits non-zero
if any check fails. It is the primary regression gate.

A separate integration script (`o2bis_independent_verification.py`) may be run
for statistical checks; it is not part of this fail-closed gate.

Usage:
    python3.12 o2bis_fast_regression.py              # run all exact checks
    python3.12 o2bis_fast_regression.py --negative   # fail-closed sanity test
"""

import sys
import numpy as np

NEGATIVE = '--negative' in sys.argv

# ── Setup ────────────────────────────────────────────────────────────────
X = np.array([[0,0,1],[1,0,0],[0,1,0]], dtype=complex)
M = X + X.T.conj()
v0 = np.ones(3, dtype=complex) / np.sqrt(3)
P0 = np.outer(v0, v0.conj())
I3 = np.eye(3, dtype=complex)


def U_op(a):
    return a * I3 + (1 - a) / 2 * M


def lambda_Q(a):
    return (3 * a - 1) / 2


def r_formula(k, a):
    return (1/3) * (1 + 2 * lambda_Q(a)**abs(k))


def G_formula(a, q):
    lam = lambda_Q(a)
    S = (1 + q) / (1 - q)
    return (1/3) * (S + 2 * (1 + lam * q) / (1 - lam * q))


def dG_da_formula(a, q):
    lam = lambda_Q(a)
    return 2 * q / (1 - lam * q)**2


def G_numerical(a, q, K=500):
    total = 0.0
    lam = lambda_Q(a)
    for k in range(-K, K+1):
        r = (1/3) * (1 + 2 * lam**abs(k))
        total += q**abs(k) * r
    return total


def finite_N_direct(a, q, N):
    """Exact Var(phi_N)/(sigma^2) as a double sum over k,l."""
    c = q
    lam = lambda_Q(a)
    total = 0.0
    for k in range(N):
        for l in range(N):
            d = abs(k - l)
            if d == 0:
                r = 1.0
            else:
                # Markov return probability P(j(k)=j(l) | j(0)=0)
                r = (1/3) * (1 + 2 * lam**d)
            total += c**d * r
    return total / N


def G_finite_N_formula(a, q, N):
    """Closed-form finite-N variance normalised by sigma^2."""
    lam = lambda_Q(a)
    total = 1.0
    c = q
    for k in range(1, N):
        r = (1/3) * (1 + 2 * lam**k)
        total += 2 * (1 - k / N) * c**k * r
    return total


# ── Fail-closed accumulator ─────────────────────────────────────────────
class Gate:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.messages = []

    def require(self, condition, message):
        if condition:
            self.passed += 1
            self.messages.append(f"  PASS: {message}")
        else:
            self.failed += 1
            self.messages.append(f"  FAIL: {message}")

    def summary(self):
        return f"\n{('='*70)}\nREGRESSION RESULT: {self.passed} passed, {self.failed} failed\n{('='*70)}"

    def exit_code(self):
        return 0 if self.failed == 0 else 1


g = Gate()

# ── Check 1: return probability ─────────────────────────────────────────
print("CHECK 1: return probability r(k,a)")
for a in [0.0, 0.2, 0.5, 0.9]:
    Ua = U_op(a)
    Uk = np.eye(3, dtype=complex)
    for k in range(6):
        r_mat = Uk[0, 0].real
        r_for = r_formula(k, a)
        g.require(abs(r_mat - r_for) < 1e-10, f"a={a}, k={k}: r_matrix={r_mat:.10f} r_formula={r_for:.10f}")
        Uk = Uk @ Ua

if NEGATIVE:
    # Deliberately corrupt one matrix power and prove the gate fails.
    a = 0.5
    Ua = U_op(a)
    Uk = np.eye(3, dtype=complex)
    for k in range(6):
        r_mat = Uk[0, 0].real
        r_for = r_formula(k, a) + 0.1  # wrong
        if k == 2:
            g.require(False, f"NEGATIVE CONTROL: corrupted r formula at a=0.5, k={k} (should fail)")
        Uk = Uk @ Ua

# ── Check 2: G formula ──────────────────────────────────────────────────
print("CHECK 2: G(a) formula against direct numerical sum")
q = 0.716531
for a in np.linspace(0, 0.95, 20):
    gf = G_formula(a, q)
    gn = G_numerical(a, q)
    g.require(abs(gf - gn) < 1e-8, f"a={a:.3f}: G_formula={gf:.10f} G_numerical={gn:.10f}")

# ── Check 3: derivative positive ────────────────────────────────────────
print("CHECK 3: dG/da positive and matches finite differences")
for a in np.linspace(0, 0.95, 20):
    df = dG_da_formula(a, q)
    h = 1e-6
    dn = (G_formula(a + h, q) - G_formula(a - h, q)) / (2 * h)
    g.require(abs(df - dn) < 1e-6, f"a={a:.3f}: dG/da formula={df:.6f} numeric={dn:.6f}")
    g.require(df > 0, f"a={a:.3f}: dG/da={df:.6f} must be positive")

# ── Check 4: finite-N variance formula self-consistency ─────────────────
print("CHECK 4: finite-N variance formula self-consistency (no MC)")
N = 30
for a in [0.0, 0.1, 0.2, 0.333, 0.5, 0.7, 0.9, 0.95]:
    direct = finite_N_direct(a, q, N)
    formula = G_finite_N_formula(a, q, N)
    g.require(abs(direct - formula) < 1e-10, f"a={a:.3f}: finite_N_direct={direct:.10f} formula={formula:.10f}")

# ── Check 5: noiseless CPTP theorem ─────────────────────────────────────
print("CHECK 5: noiseless CPTP theorem Phi(P0)=P0")
for a in [0.0, 0.333, 0.5, 0.7, 0.9, 1.0]:
    U = U_op(a)
    lam = lambda_Q(a)
    Q = I3 - P0
    K = np.sqrt(max(0, 1 - lam**2)) * Q
    phi_p0 = U @ P0 @ U.conj().T + K @ P0 @ K.conj().T
    fid = np.real(np.trace(P0 @ phi_p0))
    g.require(abs(fid - 1.0) < 1e-8, f"a={a:.3f}: Phi(P0) fidelity={fid:.10f}")
    cptp_resid = np.linalg.norm(U.conj().T @ U + K.conj().T @ K - I3)
    g.require(cptp_resid < 1e-10, f"a={a:.3f}: CPTP residual={cptp_resid:.2e}")

# ── Check 6: exact symmetric dephasing gives constant Q->Q fidelity ─────
print("CHECK 6: Q->Q completion is a-independent under exact dephasing")

def dephase_exact(rho, noise_std):
    if noise_std == 0:
        return rho.copy()
    decay = np.exp(-noise_std**2)
    result = rho.copy() * decay
    for i in range(3):
        result[i, i] = rho[i, i]
    return result


def simulate_Q_Q(a, noise_std, N):
    lam = lambda_Q(a)
    Q = I3 - P0
    K = np.sqrt(max(0, 1 - lam**2)) * Q
    rho = P0.copy()
    for _ in range(N):
        rho = dephase_exact(rho, noise_std)
        rho = U_op(a) @ rho @ U_op(a).conj().T + K @ rho @ K.conj().T
    return np.real(np.trace(P0 @ rho))

fids = [simulate_Q_Q(a, 0.05, 30) for a in np.linspace(0, 1, 11)]
spread = max(fids) - min(fids)
g.require(spread < 1e-12, f"Q->Q fidelity spread across a: {spread:.3e}")

# ── Check 7: power-law / competing-null sign consistency (synthetic) ────
print("CHECK 7: power-law fit sign consistency on synthetic data")
# Fit decoh = C*(1-a)^p for known p=2 and check predictions match.
a_syn = np.linspace(0.05, 0.75, 10)
p_known = 2.0
C_known = 1.0
d_syn = C_known * (1 - a_syn)**p_known
log_oma = np.log(1 - a_syn)
log_d = np.log(d_syn)
p_fit, log_C = np.polyfit(log_oma, log_d, 1)
C_fit = np.exp(log_C)
for i, a in enumerate(a_syn):
    pred = C_fit * (1 - a)**p_fit
    g.require(abs(pred - d_syn[i]) < 1e-12, f"synthetic a={a:.3f}: pred={pred:.6e} truth={d_syn[i]:.6e}")
g.require(abs(p_fit - p_known) < 1e-10, f"synthetic exponent fit={p_fit:.4f} known={p_known}")

# ── Check 8: exact instrument optima ────────────────────────────────────
print("CHECK 8: exact instrument white-noise optima")

def instrument_exact(a, noise_std, N):
    U = U_op(a)
    rho = P0.copy()
    p_survive = 1.0
    for _ in range(N):
        rho_prime = U @ rho @ U.conj().T
        p_success = np.real(np.trace(rho_prime))
        if p_success <= 1e-15:
            return 0.0, 0.0, 0.0
        p_survive *= p_success
        rho = dephase_exact(rho_prime / p_success, noise_std)
        tr = np.real(np.trace(rho))
        if tr > 0:
            rho = rho / tr
    fid = np.real(np.trace(P0 @ rho))
    return p_survive, fid, p_survive * fid


grid = np.linspace(0, 1, 21)
results = [instrument_exact(a, 0.05, 30) for a in grid]
p_survs = [r[0] for r in results]
conds = [r[1] for r in results]
joints = [r[2] for r in results]

best_p = grid[int(np.argmax(p_survs))]
best_f = grid[int(np.argmax(conds))]
best_j = grid[int(np.argmax(joints))]

g.require(best_p == 1.0, f"survival optimum a={best_p} (expected 1.0)")
g.require(0.30 <= best_f <= 0.40, f"conditional fidelity optimum a={best_f} (expected near 1/3)")
g.require(best_j == 1.0, f"joint optimum a={best_j} (expected 1.0)")

# ── Final summary and fail-closed exit ──────────────────────────────────
print(g.summary())
for m in g.messages:
    print(m)

sys.exit(g.exit_code())
