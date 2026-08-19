#!/usr/bin/env python3
"""
Route B CMI repair probe — consciousness metric `L_self = min(R_in, R_out)`.

Purpose:
  - Implement a valid bidirectional conditional-information estimator using
    ONE consistent covariance estimate (Ledoit-Wolf) for the full joint
    (X, M, conditioning variables), instead of separate shrinkage targets.
  - Compare it against the broken "separate-Ledoit-Wolf" CMI construction
    and the production `cpf/directed.py` linear Granger-gain proxy.
  - Test on Gaussian nulls with analytic reference CMIs and on a positive
    closed self-model loop.

Boundary:
  - This is an instrument-repair sandbox. It does NOT claim to detect or
    measure consciousness. The Fundamentals PUBLIC HOLD remains in effect.
  - No existing source files are modified.
"""

from __future__ import annotations

import json
import math
import os
import sys
from dataclasses import dataclass, field
from typing import Any

import numpy as np
from scipy.linalg import solve_discrete_lyapunov
from sklearn.covariance import LedoitWolf

# Reach the production `cpf.directed` proxy for comparison WITHOUT modifying it.
_CPF_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tools", "consciousness_metric"))
if _CPF_DIR not in sys.path:
    sys.path.insert(0, _CPF_DIR)
from cpf.directed import compute_prediction_gain
from cpf.nulls import generate_white_noise, generate_collapsed_synchrony

SEED = 20260820
RNG = np.random.default_rng(SEED)

# Shared dimensions and thresholds.
DIM = 3               # dX = dM = dE for the toy systems
T_LONG = 80_000       # long sample for reference / low-noise checks
T_SAMPLE = 8_000      # realistic sample size matching the current metric window
N_TRIALS = 12         # independent trials for the sample-size statistics
NOISE_FLOOR_NATS = 0.01
NULL_THRESHOLD = 0.08


# ---------------------------------------------------------------------------
# 1. Single-joint-covariance Gaussian CMI
# ---------------------------------------------------------------------------

def _ensure_pd_logdet(cov: np.ndarray, ridge: float = 1e-10) -> float:
    """Return logdet of `cov`, adding a small ridge if it is singular or
    indefinite.  The ridge is scaled by the average eigenvalue so it is
    dimensionally matched to the data."""
    sign, logdet = np.linalg.slogdet(cov)
    if sign > 0 and math.isfinite(logdet):
        return float(logdet)

    n = cov.shape[0]
    scale = np.trace(cov) / max(n, 1)
    cov_r = cov + ridge * scale * np.eye(n)
    sign, logdet = np.linalg.slogdet(cov_r)
    if sign > 0 and math.isfinite(logdet):
        return float(logdet)

    cov_r = cov + 1e-6 * scale * np.eye(n)
    sign, logdet = np.linalg.slogdet(cov_r)
    if sign > 0 and math.isfinite(logdet):
        return float(logdet)

    # Last resort: isotropic small ridge.
    cov_r = cov + 1e-4 * np.eye(n)
    sign, logdet = np.linalg.slogdet(cov_r)
    return float(logdet)


def fit_joint_cov(samples: np.ndarray, method: str = "ledoit_wolf") -> np.ndarray:
    """Fit ONE covariance for the full joint vector.

    The point of repair is that all block determinants are drawn from this
    single matrix, so the Gaussian entropy identity
        H(X|Y) = H(X,Y) - H(Y)
    holds at the *same* regularization level.  Using two independently
    shrunk covariances for (A,BC) and (A,C) is what breaks the CMI identity
    in the old code.
    """
    if method == "ledoit_wolf":
        cov = LedoitWolf().fit(samples).covariance_
    elif method == "sample":
        cov = np.cov(samples, rowvar=False)
    else:
        raise ValueError(f"Unknown covariance method: {method}")

    # Force positive definiteness for the slogdet calls below.
    sign, _ = np.linalg.slogdet(cov)
    if sign <= 0:
        n = cov.shape[0]
        scale = np.trace(cov) / max(n, 1)
        cov = cov + 1e-10 * scale * np.eye(n)
    return cov


def gaussian_cmi_from_cov(
    cov: np.ndarray,
    a_idx: list[int],
    b_idx: list[int],
    c_idx: list[int] | None = None,
) -> float:
    """Closed-form Gaussian CMI using determinants of sub-blocks of `cov`.

    Uses the entropy identity:
        I(A;B|C) = H(A,C) + H(B,C) - H(C) - H(A,B,C)
                = 0.5 * logdet(Σ_AC) * det(Σ_BC)
                        / (det(Σ_C) * det(Σ_ABC))
    """
    a_idx = list(a_idx)
    b_idx = list(b_idx)
    c_idx = list(c_idx) if c_idx else []

    def sub(*groups: list[int]) -> np.ndarray:
        idx: list[int] = []
        for g in groups:
            idx.extend(list(g))
        return cov[np.ix_(idx, idx)]

    if not c_idx:
        log_a = _ensure_pd_logdet(sub(a_idx))
        log_b = _ensure_pd_logdet(sub(b_idx))
        log_ab = _ensure_pd_logdet(sub(a_idx, b_idx))
        mi = 0.5 * (log_a + log_b - log_ab)
    else:
        log_ac = _ensure_pd_logdet(sub(a_idx, c_idx))
        log_bc = _ensure_pd_logdet(sub(b_idx, c_idx))
        log_c = _ensure_pd_logdet(sub(c_idx))
        log_abc = _ensure_pd_logdet(sub(a_idx, b_idx, c_idx))
        mi = 0.5 * (log_ac + log_bc - log_c - log_abc)

    return float(max(0.0, mi))


def single_cov_cmi(
    a: np.ndarray, b: np.ndarray, c: np.ndarray | None = None,
    method: str = "ledoit_wolf",
) -> float:
    """Estimate I(A;B|C) with a single joint Ledoit-Wolf covariance."""
    if c is not None and c.shape[1] > 0:
        joint = np.hstack([a, b, c])
        c_dim = c.shape[1]
    else:
        joint = np.hstack([a, b])
        c_dim = 0

    a_dim = a.shape[1]
    b_dim = b.shape[1]
    cov = fit_joint_cov(joint, method=method)

    a_idx = list(range(a_dim))
    b_idx = list(range(a_dim, a_dim + b_dim))
    c_idx = list(range(a_dim + b_dim, a_dim + b_dim + c_dim)) if c_dim else None

    return gaussian_cmi_from_cov(cov, a_idx, b_idx, c_idx)


def normalize_cmi(cmi_nats: float, floor: float = NOISE_FLOOR_NATS) -> float:
    """Map a non-negative CMI in nats to [0, 1) without dividing by a
    separately-estimated ceiling.

    We use the monotonic transform 1 - exp(-CMI).  It is stable near zero,
    does not require a second covariance estimate, and respects the
    min(R_in, R_out) gate: a true zero leg maps to exactly zero.
    """
    if cmi_nats < floor or not math.isfinite(cmi_nats):
        return 0.0
    return float(1.0 - math.exp(-cmi_nats))


def estimate_R_in_R_out(
    X: np.ndarray, M: np.ndarray, E: np.ndarray,
    method: str = "ledoit_wolf",
) -> dict[str, float]:
    """Estimate the two directed conditional-information legs.

    R_in  = I( X_{t-1} ; M_t | E_t )
    R_out = I( M_t ; X_{t+1} | X_t, E_t )
    L_self = min(R_in_norm, R_out_norm)
    """
    # Align: a = past internal state, b = current model, c = current env.
    r_in = single_cov_cmi(X[:-1], M[1:], E[1:], method=method)

    # Align: a = current model, b = future internal, c = [current internal, env].
    cond = np.hstack([X[:-1], E[:-1]])
    r_out = single_cov_cmi(M[:-1], X[1:], cond, method=method)

    return {
        "R_in_nats": r_in,
        "R_out_nats": r_out,
        "R_in_norm": normalize_cmi(r_in),
        "R_out_norm": normalize_cmi(r_out),
        "L_self": min(normalize_cmi(r_in), normalize_cmi(r_out)),
    }


# ---------------------------------------------------------------------------
# 2. Broken CMI construction (reproduces the old bug for comparison)
# ---------------------------------------------------------------------------

def _broken_shrunk_cov(joint: np.ndarray) -> np.ndarray:
    """Separate Ledoit-Wolf fit — this is what breaks the CMI identity."""
    return LedoitWolf().fit(joint).covariance_


def _broken_gaussian_mi(cov: np.ndarray, dim_a: int, dim_b: int) -> float:
    cov_a = cov[:dim_a, :dim_a]
    cov_b = cov[dim_a:dim_a + dim_b, dim_a:dim_a + dim_b]
    cov_ab = cov[:dim_a + dim_b, :dim_a + dim_b]
    sign_a, log_a = np.linalg.slogdet(cov_a)
    sign_b, log_b = np.linalg.slogdet(cov_b)
    sign_ab, log_ab = np.linalg.slogdet(cov_ab)
    if sign_a <= 0 or sign_b <= 0 or sign_ab <= 0:
        return 0.0
    mi = 0.5 * (log_a + log_b - log_ab)
    return float(max(0.0, mi))


def _broken_cmi(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> float:
    def mi_xy(x: np.ndarray, y: np.ndarray) -> float:
        joint = np.hstack([x, y])
        cov = _broken_shrunk_cov(joint)
        return _broken_gaussian_mi(cov, x.shape[1], y.shape[1])

    bc = np.hstack([b, c])
    return float(max(0.0, mi_xy(a, bc) - mi_xy(a, c)))


def broken_R_in_R_out(X: np.ndarray, M: np.ndarray, E: np.ndarray) -> dict[str, float]:
    """The old sandbox construction with two separate shrinkage targets."""
    r_in = _broken_cmi(X[:-1], M[1:], E[1:])
    cond = np.hstack([X[:-1], E[:-1]])
    r_out = _broken_cmi(M[:-1], X[1:], cond)

    def norm(v: float, a: np.ndarray, b: np.ndarray) -> float:
        joint = np.hstack([a, b])
        cov = _broken_shrunk_cov(joint)
        ceiling = _broken_gaussian_mi(cov, a.shape[1], b.shape[1])
        if ceiling < NOISE_FLOOR_NATS:
            return 0.0
        return float(min(1.0, v / ceiling))

    return {
        "R_in_nats": r_in,
        "R_out_nats": r_out,
        "R_in_norm": norm(r_in, X[:-1], M[1:]),
        "R_out_norm": norm(r_out, M[:-1], X[1:]),
        "L_self": min(
            norm(r_in, X[:-1], M[1:]),
            norm(r_out, M[:-1], X[1:]),
        ),
    }


# ---------------------------------------------------------------------------
# 3. Differentiation proxy (orthogonal to this repair, kept for context)
# ---------------------------------------------------------------------------

def effective_rank(features: np.ndarray) -> float:
    """Normalized participation ratio of the model-state covariance."""
    if features.shape[1] <= 1:
        return 0.0
    cov = np.cov(features, rowvar=False)
    eigvals = np.linalg.eigvalsh(cov)
    eigvals = np.clip(eigvals, 0.0, None)
    total = float(eigvals.sum())
    if total <= 1e-12:
        return 0.0
    pr = (total ** 2) / (float(np.sum(eigvals ** 2)) + 1e-12)
    return float(pr / features.shape[1])


# ---------------------------------------------------------------------------
# 4. Generative model machinery
# ---------------------------------------------------------------------------

@dataclass
class LinearGaussianModel:
    """State equation: Y_t = A Y_{t-1} + B E_t + W_t,
    where Y = [X; M] (column), E_t ~ N(0, Σ_E), W_t ~ N(0, Σ_W).
    """
    A: np.ndarray
    B: np.ndarray
    Sigma_W: np.ndarray
    Sigma_E: np.ndarray
    dX: int
    dM: int
    dE: int

    @property
    def dY(self) -> int:
        return self.dX + self.dM

    def stationary_cov(self) -> np.ndarray:
        Q = self.B @ self.Sigma_E @ self.B.T + self.Sigma_W
        return solve_discrete_lyapunov(self.A, Q)

    def sample(self, T: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        sigma_Y = self.stationary_cov()
        dY, dE = self.dY, self.dE
        Y = np.zeros((T, dY))
        Y[0] = RNG.multivariate_normal(mean=np.zeros(dY), cov=sigma_Y)

        E = RNG.multivariate_normal(
            mean=np.zeros(dE), cov=self.Sigma_E, size=T
        )
        W = RNG.multivariate_normal(
            mean=np.zeros(dY), cov=self.Sigma_W, size=T
        )

        for t in range(1, T):
            Y[t] = self.A @ Y[t - 1] + self.B @ E[t] + W[t]

        X = Y[:, :self.dX]
        M = Y[:, self.dX:]
        return X, M, E


def _scale_to_stable(A: np.ndarray, target: float = 0.92) -> np.ndarray:
    """Scale a matrix so its spectral radius is below `target`."""
    eigs = np.linalg.eigvals(A)
    rho = max(np.abs(eigs))
    if rho > target:
        A = A * (target / rho)
    return A


def model_white_noise() -> LinearGaussianModel:
    """All variables independent white noise."""
    return LinearGaussianModel(
        A=np.zeros((2 * DIM, 2 * DIM)),
        B=np.zeros((2 * DIM, DIM)),
        Sigma_W=np.eye(2 * DIM),
        Sigma_E=np.eye(DIM),
        dX=DIM, dM=DIM, dE=DIM,
    )


def model_class_i_exogenous(seed_shift: int = 0) -> LinearGaussianModel:
    """Class I: M_t depends only on E_t (plus tiny noise), never on X history.
    True R_in = 0, true R_out = 0."""
    rng = np.random.default_rng(SEED + seed_shift)
    Wm = rng.normal(size=(DIM, DIM)) * 0.5
    A = np.zeros((2 * DIM, 2 * DIM))
    B = np.zeros((2 * DIM, DIM))
    B[:DIM, :] = 0.2 * np.eye(DIM)          # X_t gets 0.2 * E_t
    B[DIM:, :] = Wm.T                       # M_t = E_t @ Wm
    Sigma_W = np.eye(2 * DIM)
    Sigma_W[:DIM, :DIM] *= 0.09             # X noise var
    Sigma_W[DIM:, DIM:] *= 0.01             # small M noise for regularity
    Sigma_E = 0.8 * np.eye(DIM)
    return LinearGaussianModel(A, B, Sigma_W, Sigma_E, DIM, DIM, DIM)


def model_class_ii_passive(seed_shift: int = 0) -> LinearGaussianModel:
    """Class II: M_t tracks X history but does NOT drive X future.
    True R_in > 0, true R_out = 0."""
    rng = np.random.default_rng(SEED + 100 + seed_shift)
    Wm = rng.normal(size=(DIM, DIM)) * 0.5
    A = np.zeros((2 * DIM, 2 * DIM))
    A[:DIM, :DIM] = 0.5 * np.eye(DIM)       # X AR
    A[DIM:, :DIM] = Wm.T                    # M reads X_{t-1}
    A[DIM:, DIM:] = 0.6 * np.eye(DIM)       # M AR
    A = _scale_to_stable(A, 0.92)
    B = np.zeros((2 * DIM, DIM))
    B[:DIM, :] = 0.3 * np.eye(DIM)          # X gets E_t
    Sigma_W = np.eye(2 * DIM)
    Sigma_W[:DIM, :DIM] *= 0.09
    Sigma_W[DIM:, DIM:] *= 0.09
    Sigma_E = np.eye(DIM)
    return LinearGaussianModel(A, B, Sigma_W, Sigma_E, DIM, DIM, DIM)


def model_positive_linear(seed_shift: int = 0) -> LinearGaussianModel:
    """Genuine closed self-model loop, linear-Gaussian.
    True R_in > 0 and true R_out > 0."""
    rng = np.random.default_rng(SEED + 200 + seed_shift)
    Wm = rng.normal(size=(DIM, DIM)) * 0.55  # X -> M
    Wx = rng.normal(size=(DIM, DIM)) * 0.55  # M -> X
    A = np.zeros((2 * DIM, 2 * DIM))
    A[:DIM, :DIM] = 0.3 * np.eye(DIM)
    A[:DIM, DIM:] = Wx.T                     # X_{t} reads M_{t-1}
    A[DIM:, :DIM] = Wm.T                     # M_{t} reads X_{t-1}
    A[DIM:, DIM:] = 0.4 * np.eye(DIM)
    A = _scale_to_stable(A, 0.92)
    B = np.zeros((2 * DIM, DIM))
    B[:DIM, :] = 0.2 * np.eye(DIM)           # X gets environment
    Sigma_W = np.eye(2 * DIM) * 0.09
    Sigma_E = np.eye(DIM)
    return LinearGaussianModel(A, B, Sigma_W, Sigma_E, DIM, DIM, DIM)


def model_feed_forward_chain(seed_shift: int = 0) -> LinearGaussianModel:
    """Acyclic temporal chain: E -> X2 -> X3 -> M -> X.
    Used to show that current `cpf/directed.py` falsely fires on a no-loop
    feed-forward structure.  True L_self = 0."""
    a = 0.85
    dY = 2 * DIM
    rng = np.random.default_rng(SEED + 300 + seed_shift)
    A = np.zeros((dY, dY))
    # Build a strict lower-diagonal chain along the state components.
    for i in range(1, dY):
        A[i, i - 1] = a
    # The first component is exogenous; B puts it into E, but here we treat
    # the first DIM components as environment and the rest as a chain.
    B = np.zeros((dY, DIM))
    B[:DIM, :] = 0.8 * np.eye(DIM)           # "E" drives the first DIM states
    A = _scale_to_stable(A, 0.92)
    Sigma_W = np.eye(dY) * 0.05
    Sigma_E = np.eye(DIM)
    return LinearGaussianModel(A, B, Sigma_W, Sigma_E, DIM, DIM, DIM)


def sample_positive_tanh(T: int, seed_shift: int = 0) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Non-linear positive loop from the July null-class test (bounded)."""
    rng = np.random.default_rng(SEED + 400 + seed_shift)
    Wm = rng.normal(size=(DIM, DIM)) * 0.9
    Wx = rng.normal(size=(DIM, DIM)) * 0.9
    E = rng.normal(size=(T, DIM))
    X = np.zeros((T, DIM))
    M = np.zeros((T, DIM))
    for t in range(1, T):
        M[t] = np.tanh(0.5 * M[t - 1] + X[t - 1] @ Wm)
        X[t] = np.tanh(0.3 * X[t - 1] + M[t - 1] @ Wx + 0.2 * E[t]) + rng.normal(size=DIM) * 0.2
    return X, M, E


def sample_synchronized(T: int, shift: int = 0) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Six-channel common-mode synchrony; split into arbitrary X/M/E groups."""
    data = generate_collapsed_synchrony(n_channels=6, n_samples=T, seed=SEED + shift)
    return data[:2, :].T, data[2:4, :].T, data[4:, :].T


# ---------------------------------------------------------------------------
# 5. Analytic reference CMI for linear-Gaussian models
# ---------------------------------------------------------------------------

def _sub_indices(*groups: list[int]) -> list[int]:
    idx: list[int] = []
    for g in groups:
        idx.extend(g)
    return idx


def population_R_in_R_out(model: LinearGaussianModel) -> dict[str, float]:
    """Compute the exact population CMIs from the stationary covariance."""
    dX, dM, dE = model.dX, model.dM, model.dE
    Sigma_Y = model.stationary_cov()
    Sigma_lag = Sigma_Y @ model.A.T          # Cov(Y_t, Y_{t+1})
    BE = model.B @ model.Sigma_E             # Cov(Y_t, E_t)

    # ----- R_in : I( X_{t-1} ; M_t | E_t ) -----
    dim_in = dX + dM + dE
    cov_in = np.zeros((dim_in, dim_in))
    cov_in[:dX, :dX] = Sigma_Y[:dX, :dX]
    cov_in[:dX, dX:dX + dM] = Sigma_lag[:dX, dX:]
    cov_in[dX:dX + dM, :dX] = cov_in[:dX, dX:dX + dM].T
    cov_in[dX:dX + dM, dX:dX + dM] = Sigma_Y[dX:, dX:]
    cov_in[dX:dX + dM, dX + dM:] = BE[dX:, :]
    cov_in[dX + dM:, dX:dX + dM] = BE[dX:, :].T
    cov_in[dX + dM:, dX + dM:] = model.Sigma_E

    a_in = list(range(dX))
    b_in = list(range(dX, dX + dM))
    c_in = list(range(dX + dM, dim_in))
    r_in = gaussian_cmi_from_cov(cov_in, a_in, b_in, c_in)

    # ----- R_out : I( M_t ; X_{t+1} | X_t, E_t ) -----
    # Order: [M_t, X_{t+1}, X_t, E_t]
    dim_out = dM + dX + dX + dE
    cov_out = np.zeros((dim_out, dim_out))
    ABE = model.A @ BE                       # Cov(Y_{t+1}, E_t)
    Sigma_fwd = model.A @ Sigma_Y            # Cov(Y_{t+1}, Y_t)

    iM = list(range(0, dM))
    iXp = list(range(dM, dM + dX))
    iX = list(range(dM + dX, dM + dX + dX))
    iE = list(range(dM + dX + dX, dim_out))

    cov_out[np.ix_(iM, iM)] = Sigma_Y[dX:, dX:]
    cov_out[np.ix_(iM, iXp)] = Sigma_lag[dX:, :dX]
    cov_out[np.ix_(iXp, iM)] = cov_out[np.ix_(iM, iXp)].T
    cov_out[np.ix_(iXp, iXp)] = Sigma_Y[:dX, :dX]

    cov_out[np.ix_(iM, iX)] = Sigma_Y[dX:, :dX]
    cov_out[np.ix_(iX, iM)] = Sigma_Y[:dX, dX:]
    cov_out[np.ix_(iXp, iX)] = Sigma_fwd[:dX, :dX]
    cov_out[np.ix_(iX, iXp)] = Sigma_fwd[:dX, :dX].T

    cov_out[np.ix_(iM, iE)] = BE[dX:, :]
    cov_out[np.ix_(iE, iM)] = BE[dX:, :].T
    cov_out[np.ix_(iXp, iE)] = ABE[:dX, :]
    cov_out[np.ix_(iE, iXp)] = ABE[:dX, :].T

    cov_out[np.ix_(iX, iX)] = Sigma_Y[:dX, :dX]
    cov_out[np.ix_(iX, iE)] = BE[:dX, :]
    cov_out[np.ix_(iE, iX)] = BE[:dX, :].T
    cov_out[np.ix_(iE, iE)] = model.Sigma_E

    r_out = gaussian_cmi_from_cov(cov_out, iM, iXp, iX + iE)

    return {
        "R_in_nats": r_in,
        "R_out_nats": r_out,
        "R_in_norm": normalize_cmi(r_in),
        "R_out_norm": normalize_cmi(r_out),
        "L_self": min(normalize_cmi(r_in), normalize_cmi(r_out)),
    }


# ---------------------------------------------------------------------------
# 6. Current production proxy for comparison
# ---------------------------------------------------------------------------

def directed_proxy_score(X: np.ndarray, M: np.ndarray, E: np.ndarray) -> float:
    """Run the production `cpf/directed.compute_prediction_gain` on a
    multivariate array [X; M; E].  This is the broken proxy that the
    current pipeline passes off as the self-loop gate."""
    data = np.vstack([X.T, M.T, E.T])        # shape (n_channels, n_samples)
    try:
        return float(compute_prediction_gain(data))
    except Exception:
        return float("nan")


# ---------------------------------------------------------------------------
# 7. Experiment harness
# ---------------------------------------------------------------------------

@dataclass
class Experiment:
    name: str
    description: str
    model: LinearGaussianModel | None = None
    sample_fn: Any | None = None
    is_positive: bool = False


EXPERIMENTS = [
    Experiment(
        "white_noise",
        "Independent white noise across all variables. True L_self = 0.",
        model=model_white_noise(),
    ),
    Experiment(
        "class_i_exogenous",
        "Class I: M is an exogenous-only controller. True R_in=0, R_out=0.",
        model=model_class_i_exogenous(),
    ),
    Experiment(
        "class_ii_passive",
        "Class II: M tracks X history but does not drive X future. True R_in>0, R_out=0.",
        model=model_class_ii_passive(),
    ),
    Experiment(
        "feed_forward_chain",
        "Acyclic temporal chain (no self-loop). True L_self = 0.",
        model=model_feed_forward_chain(),
    ),
    Experiment(
        "positive_linear",
        "Linear closed self-model loop. True R_in>0, R_out>0.",
        model=model_positive_linear(),
        is_positive=True,
    ),
    Experiment(
        "positive_tanh",
        "Bounded non-linear closed self-model loop (positive control).",
        sample_fn=sample_positive_tanh,
        is_positive=True,
    ),
    Experiment(
        "synchronized_no_loop",
        "Common-mode synchrony from cpf/nulls.py (no model, no loop).",
        sample_fn=sample_synchronized,
    ),
]


def sample_for_experiment(exp: Experiment, T: int, shift: int = 0) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if exp.sample_fn is not None:
        return exp.sample_fn(T, shift)
    if exp.model is not None:
        return exp.model.sample(T)
    raise ValueError(f"No sampling method for {exp.name}")


def run_experiment(exp: Experiment) -> dict[str, Any]:
    print(f"\n=== {exp.name}: {exp.description} ===")

    # 1. Population / analytic reference (where available).
    if exp.model is not None and exp.sample_fn is None:
        pop = population_R_in_R_out(exp.model)
        print(f"  Population (analytic): R_in={pop['R_in_nats']:.5f}, "
              f"R_out={pop['R_out_nats']:.5f}, L_self={pop['L_self']:.5f}")
    else:
        pop = None

    # 2. Sample-size statistics over independent trials.
    rows_new: list[dict[str, float]] = []
    rows_old: list[dict[str, float]] = []
    d_ints: list[float] = []
    proxies: list[float] = []

    for k in range(N_TRIALS):
        X, M, E = sample_for_experiment(exp, T_SAMPLE, shift=k)
        rows_new.append(estimate_R_in_R_out(X, M, E, method="ledoit_wolf"))
        rows_old.append(broken_R_in_R_out(X, M, E))
        d_ints.append(effective_rank(M))
        proxies.append(directed_proxy_score(X, M, E))

    def stats(key: str, rows: list[dict]) -> tuple[float, float]:
        vals = np.array([r[key] for r in rows])
        return float(vals.mean()), float(vals.std())

    # Aggregate sample-size statistics cleanly.
    keys = ["R_in_nats", "R_out_nats", "R_in_norm", "R_out_norm", "L_self"]
    sample_out: dict[str, float] = {}
    for k in keys:
        mean, std = stats(k, rows_new)
        sample_out[f"{k}_mean"] = mean
        sample_out[f"{k}_std"] = std

    old = {
        "broken_R_in_norm_mean": float(np.mean([r["R_in_norm"] for r in rows_old])),
        "broken_R_out_norm_mean": float(np.mean([r["R_out_norm"] for r in rows_old])),
        "broken_L_self_mean": float(np.mean([r["L_self"] for r in rows_old])),
    }

    d_int_mean = float(np.mean(d_ints))
    d_int_std = float(np.std(d_ints))
    proxy_mean = float(np.nanmean(proxies))
    proxy_std = float(np.nanstd(proxies))

    print(f"  New estimator (sample, T={T_SAMPLE}): "
          f"R_in={sample_out['R_in_nats_mean']:.5f}±{sample_out['R_in_nats_std']:.5f}, "
          f"R_out={sample_out['R_out_nats_mean']:.5f}±{sample_out['R_out_nats_std']:.5f}, "
          f"L_self={sample_out['L_self_mean']:.5f}±{sample_out['L_self_std']:.5f}")
    print(f"  Broken estimator: L_self={old['broken_L_self_mean']:.5f}, "
          f"R_out_norm={old['broken_R_out_norm_mean']:.5f}")
    print(f"  Production directed proxy (cpf/directed.py): {proxy_mean:.5f}±{proxy_std:.5f}")
    print(f"  D_int proxy (M manifold): {d_int_mean:.5f}±{d_int_std:.5f}")

    return {
        "name": exp.name,
        "description": exp.description,
        "is_positive": exp.is_positive,
        "population": pop,
        "sample": sample_out,
        "broken": old,
        "directed_proxy_mean": proxy_mean,
        "directed_proxy_std": proxy_std,
        "D_int_mean": d_int_mean,
        "D_int_std": d_int_std,
    }


def main() -> None:
    print("=" * 78)
    print("Route B: CMI repair probe — L_self = min(R_in, R_out)")
    print(f"Shared dimensions dX=dM=dE={DIM}; sample T={T_SAMPLE}; trials={N_TRIALS}")
    print("PUBLIC HOLD: This is an instrument repair, not a consciousness detector.")
    print("=" * 78)

    results: list[dict[str, Any]] = []
    for exp in EXPERIMENTS:
        results.append(run_experiment(exp))

    print("\n" + "=" * 78)
    print("SUMMARY TABLE")
    print("=" * 78)
    print(f"{'System':<22} {'R_in(nats)':>12} {'R_out(nats)':>13} {'L_self':>10} "
          f"{'D_proxy':>10} {'Broken_L':>10}")
    print("-" * 78)
    for r in results:
        s = r["sample"]
        pop = r.get("population") or {}
        if pop:
            ri = pop.get("R_in_nats", math.nan)
            ro = pop.get("R_out_nats", math.nan)
            ls = pop.get("L_self", math.nan)
        else:
            ri = s["R_in_nats_mean"]
            ro = s["R_out_nats_mean"]
            ls = s["L_self_mean"]
        print(
            f"{r['name']:<22} {ri:12.5f} {ro:13.5f} {ls:10.5f} "
            f"{r['directed_proxy_mean']:10.5f} {r['broken']['broken_L_self_mean']:10.5f}"
        )

    # Sanity verdict against the null threshold.
    print("\n" + "=" * 78)
    print(f"LEG-SPECIFIC NULL CHECKS (threshold L_self < {NULL_THRESHOLD}, positive > {NULL_THRESHOLD})")
    print("=" * 78)
    for r in results:
        s = r["sample"]
        name = r["name"]
        if r["is_positive"]:
            ok = s["L_self_mean"] > NULL_THRESHOLD
            label = "PASS" if ok else "FAIL (positive must fire)"
        else:
            ok = s["L_self_mean"] < NULL_THRESHOLD
            label = "PASS" if ok else "FAIL (null must stay near 0)"
        print(f"  [{label}] {name}: L_self={s['L_self_mean']:.5f} ± {s['L_self_std']:.5f}")

    # Persist results next to the script for the report.
    out_path = os.path.join(os.path.dirname(__file__), "consciousness_cmi_repair_probe_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nResults written to: {out_path}")


if __name__ == "__main__":
    main()
