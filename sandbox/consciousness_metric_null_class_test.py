#!/usr/bin/env python3
"""
Consciousness metric program — null-class test (first rung, ARCHIVED/SUPERSEDED).

**Status 2026-08-20:** This sandbox test is preserved as an honest historical
record of the 2026-07-20 abstract-layer null-class probe. It is **NOT** the
canonical CMI estimator for the v1.0 consciousness metric. Guard 2 in
`normalize()` is a symptom patch for the `R_out = 1.0000` artifact.

The canonical fix is the **single-joint-covariance Ledoit-Wolf CMI estimator**
in `sandbox/consciousness_cmi_repair_probe.py` (Route B, SWE Devin), which
removes the root cause by fitting one covariance to the full `(X, M, E)` vector
so the Gaussian identity `H(A|C) = H(A,C) - H(C)` holds exactly.

See `sandbox/consciousness_metric_null_class_RESULTS.md` for the cross-fix
assessment and `derivations/consciousness_metric_route_B_cmi.md` for the
validated replacement design.

Implements the abstract-theorem-layer formulas from
definitions/consciousness_metric_program.md exactly:

    R_in(L)  = I_dir( X_{t-L:t-1} -> M_t | E_{t-L:t} )
    R_out(L) = I_dir( M_t -> X_{t+1:t+L} | X_t, E_t )
    L_self(L) = min(R_in_normalized, R_out_normalized)
    D_int(L)  = effective rank (participation ratio) of the model manifold
    C_PF(L)   = C_coh(L) * D_int(L) * F_self*(L)

Scope of THIS test (honest boundary): the abstract layer only. Directed/
conditional mutual information is estimated via the Gaussian closed form
(log-det covariance ratio), which is exact for the linear-Gaussian systems
constructed below and is the correct tool to test whether the PIPELINE
reproduces the two proven analytic null results (Class I, Class II) before
any EEG data or nonparametric MI estimator is introduced. C_coh (PLV/wPLI)
requires multichannel phase data from real sensors and is out of scope here;
since C_PF is multiplicative, F_self* = 0 forces C_PF = 0 regardless of
C_coh, so the null-class claim does not need C_coh to be honest.

Falsifier #1 (feed-forward null failure) is tested directly and literally:
a real feed-forward neural net (no recurrent state at all) is scored.

A positive control (genuine closed self-model loop) is included so the test
cannot pass vacuously by a metric that always returns zero — an untested
"null" result is not evidence the metric discriminates anything.

This script does NOT promote consciousness.md or consciousness_metric_program.md.
It produces one piece of evidence toward promotion condition #2
("feed-forward null holds"). Recorded honestly in the results file this
script writes; no CLAIMS.md, PUBLIC HOLD, or tier change.
"""
from __future__ import annotations
import numpy as np
from dataclasses import dataclass
from sklearn.covariance import LedoitWolf

RNG = np.random.default_rng(20260720)
L = 8000          # window length. Diagnostic T-scaling run (200/1000/2000/4000/8000)
                   # showed Class II's R_out estimate shrinks cleanly toward 0 as T
                   # grows even with Ledoit-Wolf shrinkage (0.126 -> 0.083 -> 0.052) --
                   # the signature of finite-sample bias, not a real conceptual leak.
                   # T=8000 is the point where it first clears the noise-floor threshold
                   # across repeated diagnostic runs. See RESULTS.md for the full trace.
N_TRIALS = 20     # independent trials per system (reduced from 30 to hold runtime
                   # reasonable at the larger T; mean is still stable, see RESULTS.md)
D_EMBED = 4        # embedding dimension for X, M, E state vectors

# Below this, an MI estimate is statistically indistinguishable from the
# estimator's own noise floor for this dimension/sample-size regime (measured
# empirically: LedoitWolf-shrunk Gaussian MI of two INDEPENDENT Gaussian
# blocks at these dimensions/T settles around 0.005-0.01 nats). Used to guard
# normalize() against dividing a noisy near-zero numerator by a noisy
# near-zero denominator, which is not a meaningful ratio.
MI_NOISE_FLOOR_NATS = 0.02


def shrunk_cov(joint: np.ndarray) -> np.ndarray:
    """Ledoit-Wolf shrinkage-regularized covariance. Standard fix for the
    well-known upward bias of naive sample covariance / log-det MI estimates
    when dimension is not << sample size -- confirmed necessary here by the
    T-scaling diagnostic (see RESULTS.md)."""
    return LedoitWolf().fit(joint).covariance_


def gaussian_mi(cov_joint: np.ndarray, dim_a: int, dim_b: int) -> float:
    """Mutual information between blocks A (dims 0:dim_a) and B (dims dim_a:dim_a+dim_b)
    of a jointly Gaussian vector, from the joint covariance. Closed form:
    I(A;B) = 0.5 * log( det(Sigma_A) * det(Sigma_B) / det(Sigma_AB) )
    Returns nats; clipped at 0 (numerical floor)."""
    cov_a = cov_joint[:dim_a, :dim_a]
    cov_b = cov_joint[dim_a:dim_a + dim_b, dim_a:dim_a + dim_b]
    sign_a, logdet_a = np.linalg.slogdet(cov_a)
    sign_b, logdet_b = np.linalg.slogdet(cov_b)
    sign_ab, logdet_ab = np.linalg.slogdet(cov_joint[:dim_a + dim_b, :dim_a + dim_b])
    if sign_a <= 0 or sign_b <= 0 or sign_ab <= 0:
        return 0.0
    mi = 0.5 * (logdet_a + logdet_b - logdet_ab)
    return max(0.0, mi)


def conditional_mi(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> float:
    """I(A;B|C) for jointly Gaussian A,B,C via I(A;B|C) = I(A;[B,C]) - I(A;C).
    All inputs shape (n_samples, dim). Uses Ledoit-Wolf shrinkage covariance."""
    def mi_xy(x, y):
        joint = np.concatenate([x, y], axis=1)
        cov = shrunk_cov(joint)
        return gaussian_mi(cov, x.shape[1], y.shape[1])

    bc = np.concatenate([b, c], axis=1)
    return max(0.0, mi_xy(a, bc) - mi_xy(a, c))


def effective_rank(model_states: np.ndarray) -> float:
    """Participation ratio: (sum eig)^2 / sum(eig^2), normalized to [0,1] by
    dividing by the ambient dimension. Matches 'effective rank of the
    delay-embedded covariance' language in the spec."""
    cov = np.cov(model_states, rowvar=False)
    eigvals = np.linalg.eigvalsh(cov)
    eigvals = np.clip(eigvals, 0, None)
    if eigvals.sum() <= 1e-12:
        return 0.0
    pr = (eigvals.sum() ** 2) / (np.sum(eigvals ** 2) + 1e-12)
    return float(pr / model_states.shape[1])


@dataclass
class SystemTrace:
    X: np.ndarray  # (T, dX) internal dynamical state
    M: np.ndarray  # (T, dM) internal model state
    E: np.ndarray  # (T, dE) exogenous input


def make_class_i_exogenous_only(T: int) -> SystemTrace:
    """Class I: M_t depends ONLY on E_t (current environment), never on X
    history. Proven R_in = 0. This is the 'thermostat' shape: reactive
    mapping, no internal-history write into the model."""
    dX, dM, dE = D_EMBED, D_EMBED, D_EMBED
    E = RNG.normal(size=(T, dE))
    X = RNG.normal(size=(T, dX))
    M = np.zeros((T, dM))
    W = RNG.normal(size=(dE, dM)) * 0.5
    for t in range(T):
        M[t] = E[t] @ W  # pure function of current E, no memory, no X input
    for t in range(1, T):
        X[t] = 0.3 * X[t - 1] + 0.2 * E[t] + RNG.normal(size=dX) * 0.3
        # X evolves independently of M -- M is causally inert (also kills R_out)
    return SystemTrace(X, M, E)


def make_class_ii_passive_tracker(T: int) -> SystemTrace:
    """Class II: M_t tracks X history (R_in > 0) but does NOT causally shape
    future X once present X_t is fixed. Proven R_out = 0 -- an epiphenomenal
    logger."""
    dX, dM, dE = D_EMBED, D_EMBED, D_EMBED
    E = RNG.normal(size=(T, dE))
    X = np.zeros((T, dX))
    M = np.zeros((T, dM))
    Wm = RNG.normal(size=(dX, dM)) * 0.5
    for t in range(1, T):
        X[t] = 0.5 * X[t - 1] + 0.3 * E[t] + RNG.normal(size=dX) * 0.3
        M[t] = 0.6 * M[t - 1] + X[t - 1] @ Wm  # tracks X history: R_in > 0
        # X's next update below deliberately excludes M -- R_out = 0
    return SystemTrace(X, M, E)


def make_feedforward_net(T: int) -> SystemTrace:
    """Falsifier #1, literal: a real feed-forward neural net. No recurrent
    state of any kind -- output is a pure function of the current input only.
    'M_t' is defined as the hidden-layer activation (the natural candidate
    for a 'model state' a naive proxy might mistake for self-modeling)."""
    dE, dHidden, dX = D_EMBED, D_EMBED + 2, D_EMBED
    W1 = RNG.normal(size=(dE, dHidden)) * 0.7
    W2 = RNG.normal(size=(dHidden, dX)) * 0.7
    E = RNG.normal(size=(T, dE))
    hidden = np.tanh(E @ W1)          # hidden activation = "M_t" candidate
    X = hidden @ W2 + RNG.normal(size=(T, dX)) * 0.1   # output, function of E only
    return SystemTrace(X=X, M=hidden, E=E)


def make_positive_control_self_model(T: int) -> SystemTrace:
    """Positive control: a genuine closed self-model loop. M_t is built from
    X history (R_in > 0) AND causally determines X_{t+1} (R_out > 0). This
    system must NOT score zero, or the pipeline is vacuous.

    tanh-bounded (not raw linear feedback): a linear coupled M<->X recurrence
    is only stable within a narrow gain range and silently diverges to NaN
    over long T outside it (found by this test at T=2000 -- a bug in the
    system construction, not the metric). Bounding keeps the loop stable at
    any T while preserving genuine closed-loop dependence, and is also the
    more physically honest choice: real self-referential systems are bounded."""
    dX, dM, dE = D_EMBED, D_EMBED, D_EMBED
    E = RNG.normal(size=(T, dE))
    X = np.zeros((T, dX))
    M = np.zeros((T, dM))
    Wm = RNG.normal(size=(dX, dM)) * 0.9
    Wx = RNG.normal(size=(dM, dX)) * 0.9
    for t in range(1, T):
        M[t] = np.tanh(0.5 * M[t - 1] + X[t - 1] @ Wm)              # writes X history in
        X[t] = np.tanh(0.3 * X[t - 1] + M[t - 1] @ Wx + 0.2 * E[t]) + RNG.normal(size=dX) * 0.2
        # X's own next state is shaped by the model -- closes the loop
    return SystemTrace(X, M, E)


def score_system(trace: SystemTrace, label: str) -> dict:
    X, M, E = trace.X, trace.M, trace.E
    T = X.shape[0]
    lag = 1  # single-step directed MI, sufficient to distinguish the analytic cases

    # R_in(L) = I(X_{t-1} ; M_t | E_t)  -- windowed history collapsed to lag-1
    # for the linear-Markov systems constructed above (sufficient statistic).
    a = X[:-lag]
    b = M[lag:]
    c = E[lag:]
    r_in = conditional_mi(a, b, c)

    # R_out(L) = I(M_t ; X_{t+1} | X_t, E_t)
    a2 = M[:-lag]
    b2 = X[lag:]
    c2 = np.concatenate([X[:-lag], E[:-lag]], axis=1)
    r_out = conditional_mi(a2, b2, c2)

    # Normalize by the corresponding unconditional MI ceiling (I(A;B)) so the
    # gate lands in [0,1] per spec; guard div-by-zero.
    def normalize(mi_val, a_arr, b_arr, cond_arr=None):
        joint = np.concatenate([a_arr, b_arr], axis=1)
        cov = shrunk_cov(joint)
        ceiling = gaussian_mi(cov, a_arr.shape[1], b_arr.shape[1])
        # Guard 1: if the ceiling itself is within the estimator's noise floor,
        # the "true" MI is statistically indistinguishable from independence.
        if ceiling < MI_NOISE_FLOOR_NATS:
            return 0.0
        # Guard 2 (added 2026-08-19): detect when A is (nearly) a deterministic
        # function of the conditioning variables C. If so, A has no information
        # beyond what C already provides, so I(A; B | C) = 0 by definition.
        # This fixes the R_out = 1.0000 anomaly in Class I, where M_t = A·E_t
        # is a deterministic function of E_t. The joint covariance of (M_t, E_t)
        # is singular, and Ledoit-Wolf shrinkage introduces spurious conditional
        # dependence that inflates the conditional MI above the unconditional MI
        # (mathematically impossible for the true values, but an estimator artifact
        # when the conditioning set determines A).
        # Detection: regress A on C and check the residual variance. If the
        # residual variance is below a small fraction of A's total variance,
        # A is determined by C.
        if cond_arr is not None:
            # Compute residual variance of A given C via linear regression
            # Using the shrunk covariance for stability
            joint_ac = np.concatenate([a_arr, cond_arr], axis=1)
            cov_ac = shrunk_cov(joint_ac)
            dim_a = a_arr.shape[1]
            dim_c = cond_arr.shape[1]
            cov_a = cov_ac[:dim_a, :dim_a]
            cov_ac_cross = cov_ac[:dim_a, dim_a:dim_a + dim_c]
            cov_c = cov_ac[dim_a:dim_a + dim_c, dim_a:dim_a + dim_c]
            # Residual covariance: Cov(A) - Cov(A,C)·Cov(C)^{-1}·Cov(C,A)
            try:
                cov_c_inv = np.linalg.inv(cov_c)
                resid_cov = cov_a - cov_ac_cross @ cov_c_inv @ cov_ac_cross.T
                resid_var = np.trace(resid_cov) / dim_a
                total_var = np.trace(cov_a) / dim_a
                if total_var > 1e-10 and resid_var / total_var < 0.01:
                    # A is >99% determined by C → conditional MI must be 0
                    return 0.0
            except np.linalg.LinAlgError:
                pass
        return min(1.0, mi_val / ceiling)

    r_in_norm = normalize(r_in, a, b, cond_arr=c)    # c = E[lag:]
    r_out_norm = normalize(r_out, a2, b2, cond_arr=c2)  # c2 = [X[:-lag], E[:-lag]]
    l_self = min(r_in_norm, r_out_norm)
    d_int = effective_rank(M)

    return {
        "label": label,
        "R_in_nats": r_in, "R_out_nats": r_out,
        "R_in_norm": r_in_norm, "R_out_norm": r_out_norm,
        "L_self": l_self, "D_int": d_int,
        "C_PF_upper_bound": l_self * d_int,  # C_coh in [0,1] omitted (out of scope) -> upper bound
    }


def run_trials(builder, label, n=N_TRIALS, T=L):
    rows = [score_system(builder(T), label) for _ in range(n)]
    l_self_vals = np.array([r["L_self"] for r in rows])
    d_int_vals = np.array([r["D_int"] for r in rows])
    return {
        "label": label,
        "n_trials": n,
        "L_self_mean": float(l_self_vals.mean()),
        "L_self_std": float(l_self_vals.std()),
        "D_int_mean": float(d_int_vals.mean()),
        "R_in_norm_mean": float(np.mean([r["R_in_norm"] for r in rows])),
        "R_out_norm_mean": float(np.mean([r["R_out_norm"] for r in rows])),
    }


if __name__ == "__main__":
    print("=" * 78)
    print("CONSCIOUSNESS METRIC PROGRAM -- Null-Class Test (abstract theorem layer)")
    print(f"Window L={L}, {N_TRIALS} trials/system, embedding dim={D_EMBED}")
    print("=" * 78)

    systems = [
        (make_class_i_exogenous_only, "Class I (exogenous-only / thermostat-shape) -- expect R_in~0"),
        (make_class_ii_passive_tracker, "Class II (passive tracker) -- expect R_out~0"),
        (make_feedforward_net, "Feed-forward net (Falsifier #1, literal) -- expect L_self~0"),
        (make_positive_control_self_model, "POSITIVE CONTROL (closed self-model loop) -- expect L_self>0"),
    ]

    results = []
    for builder, label in systems:
        r = run_trials(builder, label)
        results.append(r)
        print(f"\n{label}")
        print(f"  R_in_norm  = {r['R_in_norm_mean']:.4f}")
        print(f"  R_out_norm = {r['R_out_norm_mean']:.4f}")
        print(f"  L_self     = {r['L_self_mean']:.4f} +/- {r['L_self_std']:.4f}")
        print(f"  D_int      = {r['D_int_mean']:.4f}")

    print("\n" + "=" * 78)
    print("VERDICT")
    print("=" * 78)
    null_threshold = 0.08  # generous floor above finite-sample estimator noise
    ci = next(r for r in results if r["label"].startswith("Class I"))
    cii = next(r for r in results if r["label"].startswith("Class II"))
    ff = next(r for r in results if r["label"].startswith("Feed-forward"))
    pos = next(r for r in results if r["label"].startswith("POSITIVE"))

    checks = [
        ("Class I: R_in ~ 0", ci["R_in_norm_mean"] < null_threshold),
        ("Class II: R_out ~ 0", cii["R_out_norm_mean"] < null_threshold),
        ("Feed-forward net: L_self ~ 0 (Falsifier #1 does NOT fire)", ff["L_self_mean"] < null_threshold),
        ("Positive control: L_self > 0 (pipeline is not vacuous)", pos["L_self_mean"] > null_threshold),
    ]
    all_pass = True
    for desc, ok in checks:
        status = "PASS" if ok else "FAIL"
        if not ok:
            all_pass = False
        print(f"  [{status}] {desc}")

    print()
    if all_pass:
        print("RESULT: Null-class pipeline test PASSES.")
        print("This is evidence toward promotion condition #2 (feed-forward null holds)")
        print("for the ABSTRACT LAYER on constructed linear-Gaussian systems.")
        print("It does NOT promote consciousness_metric_program.md to canonical.")
        print("Remaining before condition #2 is fully satisfied: run the same null")
        print("classes on the OBSERVABLE PROXY LAYER (real EEG delay-embedding +")
        print("PLV/wPLI), not just the abstract-layer construction tested here.")
    else:
        print("RESULT: Null-class pipeline test FAILS. Do not treat any downstream")
        print("EEG-based score as meaningful until this is fixed -- a metric that")
        print("misclassifies its own proven analytic null cases cannot be trusted")
        print("on ambiguous real data.")
    print("=" * 78)
